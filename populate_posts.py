import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np


def database_connection_url():
    dotenv.load_dotenv('passwords.env')
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


def randomize_quantity():
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    #iterate through all items in part_inventory and update quantity to a random number between 0 and 100
    with engine.begin() as conn:
        parts = conn.execute(sqlalchemy.text("""
        SELECT * FROM part_inventory;
        """)).fetchall()

        for part in parts:
            quantity = np.random.randint(0, 100)
            conn.execute(sqlalchemy.text("""
            UPDATE part_inventory SET quantity = :quantity WHERE part_id = :part_id;
            """), {"quantity": quantity, "part_id": part[0]})

def add_users(num_users):
    # Create a new DB engine based on our connection string
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    fake = Faker()

    # create fake posters with fake names and birthdays
    with engine.begin() as conn:
        posts = []
        for i in range(num_users):
            if (i % 10 == 0):
                print(i)
            

            email = fake.unique.email()
            username = email.split('@')[0]
            # check if username exists. Return bool true/false
            while True:
                username_exists = conn.execute(sqlalchemy.text("""
                SELECT * FROM users WHERE username = :username;
                """), {"username": username}).fetchone()
                if username_exists:
                    email = fake.unique.email()
                    username = email.split('@')[0]
                else:
                    break

            # if username exists, skip this iteration of the loop
            conn.execute(sqlalchemy.text("""
            INSERT INTO users (username, email) VALUES (:username, :email);
            """), {"username": username, "email": email, })

if __name__ == "__main__":
    randomize_quantity()