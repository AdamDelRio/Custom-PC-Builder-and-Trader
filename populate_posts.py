import sqlalchemy
import os
from json import load
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


def edit_prices():
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

    with engine.begin() as connection:
        sql = 'SELECT part_id, price from internal_hard_drive_specs'
        result = connection.execute(statement=sqlalchemy.text(sql))
        result = result.all()

        part_dict = {row[0]: (int(str(round(row[1], 2)).split(".")[0]), int(str(round(row[1], 2)).split(".")[1])) for row in result}
        
        for value in part_dict:
            sql = f"UPDATE part_inventory SET dollars = :dollars, cents = :cents WHERE part_id = :part_id"
            parameters = {
                "part_id": value,
                "dollars": part_dict[value][0] if part_dict[value][0] else 0,
                "cents": part_dict[value][1] if part_dict[value][1] else 0
            }
            result = connection.execute(statement=sqlalchemy.text(sql),parameters=parameters)


def add_rows():
    filename = 'internal_hard_drive.json'

    path = f"./src/data/json/{filename}"
    with open(path, "r") as f:
        data = load(f)
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)
    
    with engine.begin() as conn:
        part_type = filename.split(".")[0]
        schemas = [key for key in data[0].keys()]
        for value in data:
            sql = f"INSERT into part_inventory (name, type, quantity) VALUES (:name, :type, :quantity) RETURNING part_id"
            parameters = {
                "name":str(value["name"]),
                "type":str(part_type),
                "quantity":0
            }
            result = conn.execute(statement=sqlalchemy.text(sql),parameters=parameters)
            part_id = result.first()[0]
            #if price = null, skip this iteration of the loop
            if value["price"] == None:
                continue 
            sql = f"INSERT into {part_type}_specs (part_id, {', '.join(schemas)}) VALUES (:part_id,{', '.join([f':{column_name}' for column_name in schemas])})"
            parameters = {
                "part_id": part_id,
            }
            for schema in schemas:
                parameters[schema] = value[schema]
            
            result = conn.execute(statement=sqlalchemy.text(sql),parameters=parameters)

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
    edit_prices()