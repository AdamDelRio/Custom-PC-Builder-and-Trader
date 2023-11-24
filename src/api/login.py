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
            id = connection.execute(
                sqlalchemy.text(
                    "INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"
                ),
                {"username": username, "email": email}
            )
            id = id.first()[0]
        return {"message": "User signed up successfully",
                "id":id}
    except IntegrityError as e:
        # Make db.engine return an error
        return {"error": "Username or email already taken"}
    

@router.post("/login")
def login(identifier: str):
    """
    Log in for the site using either username or email.
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT * FROM users WHERE username = :identifier OR email = :identifier"
            ),
            {"identifier": identifier}
        ).fetchone()

        if result is None:
            return {"message": "Invalid username or email"}
        else:
            return {"message": "Login successful", "id": result[0]}
