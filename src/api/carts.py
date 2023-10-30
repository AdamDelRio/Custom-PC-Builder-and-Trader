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
        cust_id = connection.execute(sqlalchemy.text("INSERT INTO customers (name, address, phone, email) "
                                           "VALUES (:name, :address, :phone, :email) "
                                           "RETURNING ID "), parameters = dict(name = new_cart.name,
                                                                               address = new_cart.address,
                                                                               phone = new_cart.phone,
                                                                               email = new_cart.email))
        cust_id = cust_id.scaler()

        cart_id = connection.execute(sqlalchemy.text("INSERT INTO carts (customer_id) "
                                           "VALUES (:cust_id) "
                                           "RETURNING ID "), parameters = dict(cust_id = cust_id))
        cart_id = cart_id.scaler()

    return {"cart_id": cart_id}


@router.get("/{cart_id}")
def get_cart(cart_id: int):
    """ """

    return {}


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
