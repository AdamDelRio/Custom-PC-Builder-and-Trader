from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy
router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)



class NewCart(BaseModel):
    name: str
    address:str
    phone:str
    email:str


@router.post("/")
def create_cart(new_cart: NewCart):
    """ """
    with db.engine.begin() as connection:   
        cust_id = connection.execute(
            sqlalchemy.text("SELECT id FROM users WHERE "
                            "name = :name AND address = :address AND "
                            "phone = :phone AND email = :email")
            .params(name=new_cart.name, address=new_cart.address, 
                    phone=new_cart.phone, email=new_cart.email)
        ).scalar()

        if not cust_id:
            cust_id = connection.execute(sqlalchemy.text("INSERT INTO users (name, address, phone, email) "
                                            "VALUES (:name, :address, :phone, :email) "
                                            "RETURNING ID "), parameters = dict(name = new_cart.name,
                                                                                address = new_cart.address,
                                                                                phone = new_cart.phone,
                                                                                email = new_cart.email)).scalar()

        cart_id = connection.execute(sqlalchemy.text("INSERT INTO carts (user_id) "
                                           "VALUES (:cust_id) "
                                           "RETURNING cart_id "), parameters = dict(cust_id = cust_id)).scalar()

    return {"cart_id": cart_id}


@router.get("/{cart_id}")
def get_cart(cart_id: int):
    """ """
    with db.engine.begin() as connection:
        cust_name = connection.execute(sqlalchemy.text("SELECT name FROM users WHERE id = :cart_id"),
        {'cart_id': cart_id}).scalar()

    return {cust_name}


class CartItem(BaseModel):
    quantity: int


@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):
    """ """

    return "OK"


class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    """ """

    return {"total_potions_bought": 1, "total_gold_paid": 50}
