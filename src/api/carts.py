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


class CartItem(BaseModel):
    quantity: int


@router.post("/{cart_id}/items/{part_id}")
def set_item_quantity(cart_id: int, part_id: int, cart_item: CartItem):
    """ """

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO cart_items (cart_id, quantity, part_id) " 
                                        "SELECT :cart_id, :quantity, part_inventory.part_id "
                                        "FROM part_inventory WHERE part_inventory.part_id = :part_id"),
                                        parameters= dict(cart_id = cart_id,
                                                         part_id = part_id,
                                                         quantity = cart_item.quantity))

    return "OK"


class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    """ """
    with db.engine.begin() as connection:
        cart_items = connection.execute(
            sqlalchemy.text("SELECT cart_items.part_id, cart_items.quantity, part_inventory.price "
                            "FROM cart_items "
                            "JOIN part_inventory ON cart_items.part_id = part_inventory.part_id "
                            "WHERE cart_items.cart_id = :cart_id")
            .params(cart_id=cart_id)
        ).fetchall()

        total_item_bought = 0
        total_gold_paid = 0
        for item in cart_items:
            connection.execute(
                sqlalchemy.text("UPDATE part_inventory "
                                "SET quantity = quantity - :quantity "
                                "WHERE part_id = :part_id")
                .params(part_id=item.part_id, quantity=item.quantity)
            )

            connection.execute(
                sqlalchemy.text(
                    "INSERT INTO purchase_history (user_id, part_id, payment) "
                    "VALUES ((SELECT user_id FROM carts WHERE cart_id = :cart_id), :part_id, :payment)")
                .params(cart_id=cart_id, part_id=item.part_id, payment=item.price * item.quantity)
            )

            total_item_bought += item.quantity
            total_gold_paid += item.price * item.quantity

        connection.execute(
                sqlalchemy.text("DELETE FROM cart_items WHERE cart_id = :cart_id")
                .params(cart_id=cart_id)
            )

    return {
        "total_items_bought": total_item_bought,
        "total_gold_paid": total_gold_paid
    }
