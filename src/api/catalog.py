import sqlalchemy
from src import database as db
from fastapi import APIRouter

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
