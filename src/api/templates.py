import sqlalchemy
from pydantic import BaseModel
from src import database as db
from fastapi import APIRouter

router = APIRouter()

class NewTemplate(BaseModel):
    user_id:int



@router.post('/template/new')
def create_template(new_template:NewTemplate):
    with db.engine.begin() as connection:
        temp_id = connection.execute(sqlalchemy.text("INSERT INTO PC_TEMPLATES (user_id) "
                                                     "VALUES :user_id "
                                                     "RETURNING id"),
                                                     parameters= dict(user_id = new_template.user_id)).scalar()
        
        return temp_id
    
class TemplatePart(BaseModel):
    quantity:int

@router.post('{user_id}/{template_id}/items/{part_id}')
def add_item_to_template(user_id, template_id, part_id, template_part: TemplatePart):
    with db.engine.begin() as connection:
        connection.execute(statement=sqlalchemy.text("INSERT INTO pc_template_parts (template_id, user_id, part_id, quantity) "
                                           "VALUES (:template_id, :user_id, :part_id, :quantity) "),
                                           parameters= {
                                               "template_id": template_id,
                                               "user_id": user_id,
                                               "part_id" :part_id,
                                               "quantity" :template_part.quantity
                                           })
        

# @router.post('{template_id}/cart/new')
# def create_cart_from_template(template_id):
    