import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
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
    """
    Create a new custom PC Template
    """
    with db.engine.begin() as connection:
        temp_id = connection.execute(sqlalchemy.text("INSERT INTO PC_TEMPLATES (user_id) "
                                                     "VALUES (:user_id) "
                                                     "RETURNING id"),
                                                     parameters= {"user_id": int(new_template.user_id)}).scalar()
        
        return {"Template_Id": temp_id}
    
class TemplatePart(BaseModel):
    quantity:int
    user_item : bool

@router.post('/{user_id}/{template_id}/items/{part_id}')
def add_item_to_template(user_id, template_id, part_id, template_part: TemplatePart):
    """
    Add a PC template part to an existing template
    """
    with db.engine.begin() as connection:
        temp_part_id = connection.execute(statement=sqlalchemy.text("INSERT INTO pc_template_parts (template_id, user_id, part_id, quantity, user_part) "
                                           "VALUES (:template_id, :user_id, :part_id, :quantity, :user_part) "),
                                           parameters= {
                                               "template_id": template_id,
                                               "user_id": user_id,
                                               "part_id" :part_id,
                                               "quantity" :template_part.quantity,
                                               "user_part": template_part.user_item
                                           })
        return temp_part_id
        
@router.post('/{template_id}/removeitem/{part_id}')
def remove_item_from_template(template_id, part_id, template_part:TemplatePart):
    """
    Remove a specific item from a template
    """
    with db.engine.begin() as connection:
        row = connection.execute(sqlalchemy.text("SELECT quantity "
                                 "FROM pc_template_parts "
                                 "WHERE template_id = :template_id and part_id = :part_id and user_part = :user_part"), 
                                 parameters= {"template_id":template_id,
                                        "part_id":part_id,
                                        "quantity": template_part.quantity,
                                        "user_part":template_part.user_item}).fetchone()
        if row is not None:
            if template_part.quantity >= row[0]:
                connection.execute(sqlalchemy.text("DELETE FROM pc_template_parts WHERE template_id = :template_id and part_id = :part_id and quantity = :quantity and user_part = :user_part"), 
                                parameters= {"template_id":template_id,
                                                "part_id":part_id,
                                                "quantity": template_part.quantity,
                                                "user_part":template_part.user_item})
            else: 
                connection.execute(sqlalchemy.text("UPDATE pc_template_parts quantity SET quantity = quantity - :quantity "  
                                                   "WHERE template_id = :template_id and part_id = :part_id and user_part = :user_part"), 
                                parameters= {"template_id":template_id,
                                                "part_id":part_id,
                                                "quantity": template_part.quantity,
                                                "user_part":template_part.user_item})
            return "Item removed from template"
        
        return "Item never existed in template. Double check part_id and template_id"
                                                                                                                                              


class NewCart(BaseModel):
    user_id: int
    name: str
    address:str
    phone:str
    


@router.post('/{template_id}/cart/new')
def create_cart_from_template(template_id, new_cart:NewCart):
    """
    Convert a PC template into a cart to purchase all items in the template
    """
    with db.engine.begin() as connection:
        cust_id = connection.execute(
            sqlalchemy.text("SELECT id FROM customers WHERE "
                            "name = :name AND address = :address AND "
                            "phone = :phone ")
            .params(name=new_cart.name, address=new_cart.address, 
                    phone=new_cart.phone)
        ).scalar()

        if not cust_id:
            cust_id = connection.execute(sqlalchemy.text("INSERT INTO customers (user_id, name, address, phone) "
                                            "VALUES (:user_id, :name, :address, :phone) "
                                            "RETURNING id "), parameters = dict(user_id = new_cart.user_id,
                                                                                name = new_cart.name,
                                                                                address = new_cart.address,
                                                                                phone = new_cart.phone)).scalar()
        
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
    
@router.get('/{template_id}/view_template')
def view_template(template_id: int):
    """
    View details of a specific PC template
    """
    with db.engine.begin() as connection:
        parts_data = connection.execute(
            sqlalchemy.text("""
                SELECT t.part_id,
                       p.name,
                       p.type,
                       t.quantity,
                       CASE
                           WHEN t.user_part THEN up.dollars + up.cents / 100.0
                           ELSE p.dollars + p.cents / 100.0
                       END AS price
                FROM pc_template_parts t
                JOIN part_inventory p ON t.part_id = p.part_id
                LEFT JOIN user_parts up ON t.part_id = up.part_id AND t.user_part
                WHERE t.template_id = :template_id
            """),
            {"template_id": template_id}
        ).mappings().all()

        if not parts_data:
            raise HTTPException(status_code=404, detail="Template not found or no parts in template")

        parts_info_list = []
        for part_data in parts_data:
            part_info = dict(part_data)
            parts_info_list.append(part_info)

        return {"template_id": template_id, "parts": parts_info_list}
