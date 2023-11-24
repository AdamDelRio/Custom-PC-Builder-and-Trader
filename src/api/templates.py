import sqlalchemy
from fastapi import APIRouter, Depends
from src.api import auth
from pydantic import BaseModel
from src import database as db
from fastapi import APIRouter
router = APIRouter(
    prefix="/templates",
    tags=["templates"],
    dependencies=[Depends(auth.get_api_key)],
)

class NewTemplate(BaseModel):
    user_id:int



@router.post('/template/new')
def create_template(new_template:NewTemplate):
    with db.engine.begin() as connection:
        temp_id = connection.execute(sqlalchemy.text("INSERT INTO PC_TEMPLATES (user_id) "
                                                     "VALUES (:user_id) "
                                                     "RETURNING id"),
                                                     parameters= {"user_id": int(new_template.user_id)}).scalar()
        
        return temp_id
    
class TemplatePart(BaseModel):
    quantity:int
    user_item : bool

@router.post('/{user_id}/{template_id}/items/{part_id}')
def add_item_to_template(user_id, template_id, part_id, template_part: TemplatePart):
    with db.engine.begin() as connection:
        connection.execute(statement=sqlalchemy.text("INSERT INTO pc_template_parts (template_id, user_id, part_id, quantity, user_part) "
                                           "VALUES (:template_id, :user_id, :part_id, :quantity, :user_part) "),
                                           parameters= {
                                               "template_id": template_id,
                                               "user_id": user_id,
                                               "part_id" :part_id,
                                               "quantity" :template_part.quantity,
                                               "user_part": template_part.user_item
                                           })
        return "OK"
        
class NewCart(BaseModel):
    user_id: int
    name: str
    address:str
    phone:str
    email:str


@router.post('/{template_id}/cart/new')
def create_cart_from_template(template_id, new_cart:NewCart):
    with db.engine.begin() as connection:
        cust_id = connection.execute(
            sqlalchemy.text("SELECT id FROM customers WHERE "
                            "name = :name AND address = :address AND "
                            "phone = :phone AND email = :email")
            .params(name=new_cart.name, address=new_cart.address, 
                    phone=new_cart.phone, email=new_cart.email)
        ).scalar()

        if not cust_id:
            cust_id = connection.execute(sqlalchemy.text("INSERT INTO customers (user_id, name, address, phone, email) "
                                            "VALUES (:user_id, :name, :address, :phone, :email) "
                                            "RETURNING id "), parameters = dict(user_id = new_cart.user_id,
                                                                                name = new_cart.name,
                                                                                address = new_cart.address,
                                                                                phone = new_cart.phone,
                                                                                email = new_cart.email)).scalar()
        
        cart_id = connection.execute(sqlalchemy.text("INSERT INTO carts (user_id) "
                                                     "SELECT customers.id "
                                                     "FROM pc_templates "
                                                     "JOIN customers ON customers.user_id = pc_templates.user_id "
                                                     "WHERE pc_templates.id = :template_id "
                                                     "RETURNING cart_id"),
                                                     parameters= dict(template_id = template_id)).scalar()
        connection.execute(sqlalchemy.text("INSERT INTO cart_items (cart_id, part_id, quantity, user_item)"
                                           "SELECT :cart_id, pc_template_parts.part_id, pc_template_parts.quantity, pc_template_parts.user_part "
                                           "FROM pc_template_parts "
                                           "WHERE pc_template_parts.template_id = :template_id "),
                                            parameters= dict(cart_id = cart_id,
                                                             template_id = template_id))
        return {"cart_id": cart_id}