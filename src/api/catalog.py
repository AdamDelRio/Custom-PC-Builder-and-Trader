from pydantic import BaseModel
import sqlalchemy
from src import database as db
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from typing import List
from enum import Enum

router = APIRouter()


class SearchPart(BaseModel):
    name: str

class PartType(str, Enum):
    case = "case"
    cpu = "cpu"
    monitor = "monitor"
    motherboard = "motherboard"
    power_supply = "power_supply"
    video_card = "video_card"
    internal_hard_drive = "internal_hard_drive"

@router.post("/catalog/search", tags=["catalog"])
def search_catalog(
    search_part: SearchPart,
    part_type: PartType = Query(None, title="Part Type", description="Filter by part type"),
    search_page: int = Query(1, title="Search Page", description="Page number for search results"),
    sort_order: str = Query("name", title="Sort Order", description="Order results by 'name' or 'price'"),
    ):
    if not part_type:
        part_type = ""
    with db.engine.begin() as connection:
        page_size = 5
        offset = (search_page - 1) * page_size

        join_conditions = ""
        specs_columns = ""

        if sort_order not in ["name", "price"]:
            return "Invalid sort order"

        order_clause = "part_inventory.name" if sort_order == "name" else "(part_inventory.dollars + part_inventory.cents / 100.0)"

        if part_type == "case":
            join_conditions = "LEFT JOIN case_specs ON part_inventory.part_id = case_specs.part_id"
            specs_columns = ", " + """
                case_specs.name AS case_name,
                case_specs.color,
                case_specs.psu,
                case_specs.side_panel,
                case_specs.external_volume,
                case_specs.internal_35_bays
            """
        elif part_type == "cpu":
            join_conditions = "LEFT JOIN cpu_specs ON part_inventory.part_id = cpu_specs.part_id"
            specs_columns = ", " + """
                cpu_specs.core_count,
                cpu_specs.core_clock,
                cpu_specs.boost_clock,
                cpu_specs.tdp
            """
        elif part_type == "monitor":
            join_conditions = "LEFT JOIN monitor_specs ON part_inventory.part_id = monitor_specs.part_id"
            specs_columns = ", " + """
                monitor_specs.screen_size,
                monitor_specs.resolution,
                monitor_specs.refresh_rate,
                monitor_specs.response_time
            """
        elif part_type == "motherboard":
            join_conditions = "LEFT JOIN motherboard_specs ON part_inventory.part_id = motherboard_specs.part_id"
            specs_columns = ", " + """
                motherboard_specs.socket,
                motherboard_specs.form_factor,
                motherboard_specs.max_memory,
                motherboard_specs.memory_slots
            """
        elif part_type == "power_supply":
            join_conditions = "LEFT JOIN power_supply_specs ON part_inventory.part_id = power_supply_specs.part_id"
            specs_columns = ", " + """
                power_supply_specs.type AS psu_type,
                power_supply_specs.efficiency,
                power_supply_specs.wattage
            """
        elif part_type == "video_card":
            join_conditions = "LEFT JOIN video_card_specs ON part_inventory.part_id = video_card_specs.part_id"
            specs_columns = ", " + """
                video_card_specs.chipset,
                video_card_specs.memory,
                video_card_specs.core_clock AS gpu_core_clock,
                video_card_specs.boost_clock AS gpu_boost_clock
            """
        elif part_type == "internal_hard_drive":
            join_conditions = "LEFT JOIN internal_hard_drive_specs ON part_inventory.part_id = internal_hard_drive_specs.part_id"
            specs_columns = ", " + """
                internal_hard_drive_specs.capacity,
                internal_hard_drive_specs.price_per_gb,
                internal_hard_drive_specs.type AS storage_type,
                internal_hard_drive_specs.cache,
                internal_hard_drive_specs.form_factor AS storage_form_factor,
                internal_hard_drive_specs.interface AS storage_interface
            """


        sql = sqlalchemy.text(f"""
            SELECT
                part_inventory.part_id,
                part_inventory.name,
                part_inventory.type,
                part_inventory.quantity,
                part_inventory.dollars + part_inventory.cents / 100.0 AS price
                {specs_columns}
            FROM part_inventory
            {join_conditions}
            WHERE LOWER(part_inventory.name) ILIKE LOWER(:name) AND LOWER(part_inventory.type) ILIKE LOWER(:part_type) AND quantity > 0
            ORDER BY {order_clause}
            LIMIT :page_size OFFSET :offset
        """)

        result = connection.execute(sql, {'name': '%' + search_part.name + '%', 'part_type': '%' + part_type + '%', 'page_size': page_size, 'offset': offset})
        rows = result.mappings().all()

        part_info_list = []
        for row_dict in rows:
            part_info = dict(row_dict)
            part_info_list.append(part_info)

        response = {"results": part_info_list}

        if search_page > 1:
            response["previous"] = search_page - 1

        if len(rows) == page_size:
            next_offset = offset + page_size
            next_query = f"""
                SELECT
                    part_inventory.part_id,
                    part_inventory.name,
                    part_inventory.type,
                    part_inventory.quantity,
                    part_inventory.dollars + part_inventory.cents / 100.0 AS price
                    {specs_columns}
                FROM part_inventory
                {join_conditions}
                WHERE LOWER(part_inventory.name) ILIKE LOWER(:name) AND 
                LOWER(part_inventory.type) ILIKE LOWER(:part_type) AND quantity > 0
                ORDER BY {order_clause}
                LIMIT :page_size OFFSET :offset
                """

            next_result = connection.execute(sqlalchemy.text(next_query), {'name': '%' + search_part.name + '%', 'part_type': '%' + part_type + '%', 'page_size': page_size, 'offset': next_offset})
            next_rows = next_result.fetchone()

            if next_rows not in (None, "null"):
                response["next"] = search_page + 1

        if not part_info_list:
            return "No items found in catalog"

        return response

class Parts(BaseModel):
    user_id: int
    part_id: int
    quantity: int
    price: int

@router.post("/user_catalog/add", tags=["catalog"])
def add_to_user_catalog(parts: Parts):
    """
    Allow a user to add items to their catalog.
    """
    try:
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(
                "SELECT 1 FROM part_inventory WHERE part_id = :part_id"
            ).params(part_id=parts.part_id)).fetchone()

            if not result:
                raise HTTPException(status_code=404, detail=f"Part ID {parts.part_id} not found in inventory")

            existing_quantity = connection.execute(sqlalchemy.text(
                """
                SELECT quantity FROM user_parts 
                WHERE user_id = :user_id AND part_id = :part_id
                """
            ).params(user_id=parts.user_id, part_id=parts.part_id)).fetchone()

            if existing_quantity:
                connection.execute(sqlalchemy.text(
                    """
                    UPDATE user_parts 
                    SET quantity = quantity + :quantity, price = :price
                    WHERE user_id = :user_id AND part_id = :part_id
                    """
                ).params(user_id=parts.user_id, 
                            part_id=parts.part_id, 
                            quantity=parts.quantity, 
                            price=parts.price))
            else:
                connection.execute(sqlalchemy.text(
                    """
                    INSERT INTO user_parts (user_id, part_id, quantity, price)
                    VALUES (:user_id, :part_id, :quantity, :price)
                    """
                ).params(user_id=parts.user_id, 
                            part_id=parts.part_id, 
                            quantity=parts.quantity, 
                            price=parts.price))

            return {"status": "success", "message": "Items added/updated in user's catalog"}
    except Exception as e:
        return {"status": "error", "message": "An error occurred: " + str(e)}
    
@router.post("/catalog/search_user_catalog", tags=["catalog"])
def search_user_catalog(
    search_part: SearchPart,
    part_type: PartType = Query(None, title="Part Type", description="Filter by part type"),
    search_page: int = Query(1, title="Search Page", description="Page number for search results"),
    sort_order: str = Query("name", title="Sort Order", description="Order results by 'name' or 'price"),
):
    if not part_type:
        part_type = ""

    with db.engine.begin() as connection:
        page_size = 5
        offset = (search_page - 1) * page_size

        join_conditions = ""
        specs_columns = ""

        if sort_order not in ["name", "price"]:
            return "Invalid sort order"

        order_clause = "pi.name" if sort_order == "name" else "(up.dollars + up.cents / 100.0)"

        if part_type == "case":
            join_conditions = "LEFT JOIN case_specs AS specs ON up.part_id = specs.part_id"
            specs_columns = ", " + """
                specs.name AS case_name,
                specs.color,
                specs.psu,
                specs.side_panel,
                specs.external_volume,
                specs.internal_35_bays
            """
        elif part_type == "cpu":
            join_conditions = "LEFT JOIN cpu_specs AS specs ON up.part_id = specs.part_id"
            specs_columns = ", " + """
                specs.core_count,
                specs.core_clock,
                specs.boost_clock,
                specs.tdp
            """
        elif part_type == "monitor":
            join_conditions = "LEFT JOIN monitor_specs AS specs ON up.part_id = specs.part_id"
            specs_columns = ", " + """
                specs.screen_size,
                specs.resolution,
                specs.refresh_rate,
                specs.response_time
            """
        elif part_type == "motherboard":
            join_conditions = "LEFT JOIN motherboard_specs AS specs ON up.part_id = specs.part_id"
            specs_columns = ", " + """
                specs.socket,
                specs.form_factor,
                specs.max_memory,
                specs.memory_slots
            """
        elif part_type == "power_supply":
            join_conditions = "LEFT JOIN power_supply_specs AS specs ON up.part_id = specs.part_id"
            specs_columns = ", " + """
                specs.type AS psu_type,
                specs.efficiency,
                specs.wattage
            """
        elif part_type == "video_card":
            join_conditions = "LEFT JOIN video_card_specs AS specs ON up.part_id = specs.part_id"
            specs_columns = ", " + """
                specs.chipset,
                specs.memory,
                specs.core_clock AS gpu_core_clock,
                specs.boost_clock AS gpu_boost_clock
            """
        elif part_type == "internal_hard_drive":
            join_conditions = "LEFT JOIN internal_hard_drive_specs AS specs ON up.part_id = specs.part_id"
            specs_columns = ", " + """
                specs.capacity,
                specs.price_per_gb,
                specs.type AS storage_type,
                specs.cache,
                specs.form_factor AS storage_form_factor,
                specs.interface AS storage_interface
            """

        sql_user_catalog = sqlalchemy.text(f"""
            SELECT
                up.id,
                up.user_id,
                up.part_id,
                pi.name,
                pi.type,
                up.quantity,
                up.dollars + up.cents / 100.0 AS price
                {specs_columns}
            FROM user_parts up
            JOIN part_inventory pi ON up.part_id = pi.part_id
            {join_conditions}
            WHERE LOWER(pi.name) ILIKE LOWER(:name) AND 
            LOWER(pi.type) ILIKE LOWER(:part_type) AND up.quantity > 0
            ORDER BY {order_clause}
            LIMIT :page_size OFFSET :offset
        """)

        result_user_catalog = connection.execute(sql_user_catalog, {
            'name': '%' + search_part.name + '%',
            'part_type': '%' + part_type + '%',
            'page_size': page_size,
            'offset': offset
        })

        rows_user_catalog = result_user_catalog.mappings().all()
        part_info_list = []

        for row_dict in rows_user_catalog:
            part_info = dict(row_dict)
            part_info_list.append(part_info)

        response = {"user_catalog": part_info_list}

        if search_page > 1:
            response["previous"] = search_page - 1

        if len(rows_user_catalog) == page_size:
            next_offset = offset + page_size

            next_query = f"""
                SELECT
                    up.part_id,
                    pi.name,
                    pi.type,
                    up.quantity,
                    up.dollars + up.cents / 100.0 AS price
                    {specs_columns}
                FROM user_parts up
                JOIN part_inventory pi ON up.part_id = pi.part_id
                {join_conditions}
                WHERE LOWER(pi.name) ILIKE LOWER(:name) AND 
                LOWER(pi.type) ILIKE LOWER(:part_type) AND up.quantity > 0
                ORDER BY {order_clause}
                LIMIT :page_size OFFSET :offset
            """

            next_result = connection.execute(sqlalchemy.text(next_query), {
                'name': '%' + search_part.name + '%',
                'part_type': '%' + part_type + '%',
                'page_size': page_size,
                'offset': next_offset
            })

            next_rows = next_result.mappings().all()

            if next_rows:
                response["next"] = search_page + 1

        if not part_info_list:
            return "No items found in user catalog"

        return response
