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
    user_id: int
    name: str
    address:str
    phone:str


@router.post("/")
def create_cart(new_cart: NewCart):
    """ """
    with db.engine.begin() as connection:   
        cust_id = connection.execute(
            sqlalchemy.text("SELECT id FROM customers WHERE "
                            "name = :name AND address = :address AND "
                            "phone = :phone")
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
                                           "VALUES (:cust_id) "
                                           "RETURNING cart_id "), parameters = dict(cust_id = cust_id)).scalar()

    return {"cart_id": cart_id}


class CartItem(BaseModel):
    quantity: int
    user_item: bool


@router.post("/{cart_id}/items/{part_id}")
def set_item_quantity(cart_id: int, part_id: int, cart_item: CartItem):
    """
    For a user_item, make sure to use the id instead of the part_id
    """

    with db.engine.begin() as connection:
        inventory_table = "user_parts" if cart_item.user_item else "part_inventory"
        inventory_id_column = "id" if cart_item.user_item else "part_id"

        inventory_item = connection.execute(
            sqlalchemy.text(
                f"SELECT quantity FROM {inventory_table} WHERE {inventory_id_column} = :part_id"
            ).params(part_id=part_id)
        ).fetchone()

        if inventory_item and inventory_item.quantity >= cart_item.quantity:
            connection.execute(sqlalchemy.text("INSERT INTO cart_items (cart_id, quantity, part_id, user_item) " 
                                            "VALUES (:cart_id, :quantity, :part_id, :user_item)"),
                                            parameters= dict(cart_id = cart_id,
                                                            part_id = part_id,
                                                            quantity = cart_item.quantity,
                                                            user_item = cart_item.user_item))

            return "OK"
        else:
            return "Item not found or insufficient quantity"



@router.post("/{cart_id}/checkout")
def checkout(cart_id: int):
    """ """
    with db.engine.begin() as connection:
        cart_items = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    cart_items.part_id,
                    cart_items.quantity,
                    CASE
                        WHEN cart_items.user_item THEN user_parts.dollars + user_parts.cents / 100.0
                        ELSE part_inventory.dollars + part_inventory.cents / 100.0
                    END as price,
                    cart_items.user_item
                FROM
                    cart_items
                LEFT JOIN
                    part_inventory ON cart_items.part_id = part_inventory.part_id
                LEFT JOIN
                    user_parts ON cart_items.part_id = user_parts.id
                WHERE
                    cart_items.cart_id = :cart_id AND
                    cart_items.checked_out = false
                 """
                )
            .params(cart_id=cart_id)
        ).fetchall()

        total_item_bought = 0
        total_dollars_paid = 0
        for item in cart_items:
            if item.user_item:
                connection.execute(
                    sqlalchemy.text(
                        "UPDATE user_parts "
                        "SET quantity = quantity - :quantity "
                        "WHERE id = :part_id")
                    .params(part_id=item.part_id, quantity=item.quantity)
                )
            else:
                connection.execute(
                    sqlalchemy.text("UPDATE part_inventory "
                                    "SET quantity = quantity - :quantity "
                                    "WHERE part_id = :part_id")
                    .params(part_id=item.part_id, quantity=item.quantity)
                )

            cost = item.price * item.quantity
            dollars = int(cost)
            cents = (cost - dollars) * 100

            connection.execute(
                sqlalchemy.text(
                    "INSERT INTO purchase_history (user_id, part_id, user_item, dollars, cents) "
                    "VALUES ((SELECT user_id FROM carts WHERE cart_id = :cart_id), :part_id, :user_item, :dollars, :cents)")
                .params(cart_id=cart_id, part_id=item.part_id, user_item = item.user_item, dollars=dollars, cents=cents)
            )

            total_item_bought += item.quantity
            total_dollars_paid += item.price * item.quantity

        connection.execute(
            sqlalchemy.text("UPDATE cart_items SET checked_out = true WHERE cart_id = :cart_id")
            .params(cart_id=cart_id)
        )

        return {
            "total_items_bought": total_item_bought,
            "total_dollars_paid": total_dollars_paid
        }
