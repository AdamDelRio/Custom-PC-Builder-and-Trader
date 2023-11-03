from pydantic import BaseModel
import sqlalchemy
from src import database as db
from fastapi import APIRouter
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """
    sql = "SELECT part_inventory.price as price, part_inventory.name as name, part_inventory.type as type, part_inventory.quantity as quantity, part_inventory.part_id as part_id from part_inventory where quantity > 0"
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(sql))
        available_parts = []
        parts = result.all()
    for part in parts:
            potion_info = {
                
                "name": part.name,
                "type":part.type,
                "part_id":part.part_id,
                "quantity": part.quantity,
                "price": part.price,

            }
            available_parts.append(potion_info)


    #TODO: return max of 20 items. 

    # Can return a max of 20 items.
    return available_parts

@router.get("/user_catalog/{user_id}", tags=["catalog"])
def get_user_catalog(user_id: int):
    """
    Fetch the catalog for a specific user based on their user_id.
    Only consider the quantity and price from user_parts, not from part_inventory.
    """
    
    sql = """
    SELECT
        up.price AS price,
        pi.name AS name,
        pi.type AS type,
        up.quantity AS quantity,
        up.part_id AS part_id
    FROM user_parts up
    JOIN part_inventory pi ON up.part_id = pi.part_id
    WHERE up.user_id = :user_id
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(sql), user_id=user_id)
        user_parts = []
        for row in result:
            part_info = {
                "name": row.name,
                "type": row.type,
                "part_id": row.part_id,
                "quantity": row.quantity,
                "price": row.price,
                "user_id": user_id
            }
            user_parts.append(part_info)

    return user_parts

@router.get("/user_catalog", tags=["catalog"])
def get_user_catalog(user_id: int):
    """
    Fetch the catalog for a specific user based on their user_id.
    Only consider the quantity and price from user_parts, not from part_inventory.
    """
    
    sql = """
    SELECT
        up.price AS price,
        pi.name AS name,
        pi.type AS type,
        up.quantity AS quantity,
        up.part_id AS part_id
    FROM user_parts up
    JOIN part_inventory pi ON up.part_id = pi.part_id
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(sql), user_id=user_id)
        user_parts = []
        for row in result:
            part_info = {
                "name": row.name,
                "type": row.type,
                "part_id": row.part_id,
                "quantity": row.quantity,
                "price": row.price,
                "user_id": user_id
            }
            user_parts.append(part_info)

    return user_parts

class Parts(BaseModel):
    user_id: int
    part_ids: List[int]
    quantity: int
    price: int

@router.post("/user_catalog/add", tags=["catalog"])
def add_to_user_catalog(parts: Parts):
    """
    Allow a user to add items to their catalog.
    """

    for part_id in parts.part_ids:
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(
                "SELECT 1 FROM part_inventory WHERE part_id = :part_id"
            ).params(part_id=part_id)).fetchone()
            if not result:
                raise HTTPException(status_code=404, detail=f"Part ID {part_id} not found in inventory")

        with db.engine.begin() as connection:
            existing_quantity = connection.execute(sqlalchemy.text(
                """
                SELECT quantity FROM user_parts 
                WHERE user_id = :user_id AND part_id = :part_id
                """
            ).params(user_id=parts.user_id, part_id=part_id)).fetchone()

        if existing_quantity:
            with db.engine.begin() as connection:
                connection.execute(sqlalchemy.text(
                    """
                    UPDATE user_parts 
                    SET quantity = quantity + :quantity, price = :price
                    WHERE user_id = :user_id AND part_id = :part_id
                    """
                ).params(user_id=parts.user_id, 
                         part_id=part_id, 
                         quantity=parts.quantity, 
                         price=parts.price))
        else:
            with db.engine.begin() as connection:
                connection.execute(sqlalchemy.text(
                    """
                    INSERT INTO user_parts (user_id, part_id, quantity, price)
                    VALUES (:user_id, :part_id, :quantity, :price)
                    """
                ).params(user_id=parts.user_id, 
                         part_id=part_id, 
                         quantity=parts.quantity, 
                         price=parts.price))

    return {"status": "success", "message": "Items added/updated in user's catalog"}