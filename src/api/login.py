from fastapi import APIRouter, Depends
from src.api import auth
from sqlalchemy.exc import IntegrityError
from src import database as db

import sqlalchemy
router = APIRouter(
    prefix="/account",
    tags=["account"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/create")
def sign_up(username: str, email: str):
    """
    Sign up for the site.
    """
    try:
        with db.engine.begin() as connection:
            connection.execute(
                sqlalchemy.text(
                    "INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"
                ),
                {"username": username, "email": email}
            )
        return {"message": "User signed up successfully"}
    except IntegrityError as e:
        # Make db.engine return an error
        return {"error": "Username or email already taken"}
    

@router.post("/login")
def login(username: str):
    """
    Log in for the site.
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT * FROM users WHERE username = :username"
            ),
            {"username": username}
        ).fetchone()

        if result is None:
            return {"message": "Invalid username"}
        else:
            return {"message": "Login successful"}
