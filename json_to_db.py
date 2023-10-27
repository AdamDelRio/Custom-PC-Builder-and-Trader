import sqlalchemy
from json import load
from src import database as db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from sys import argv

def main():
    if len(argv) == 1:
        filename = input("filename: ")
    else:
        filename = argv[1]

    path = f"./src/data/json/{filename}"
    with open(path, "r") as f:
        data = load(f)
    with db.engine.begin() as connection:
        schema = [key for key in data[0].keys()]
        sql = f"INSERT into users (name, address, phone, email) VALUES (:name, :address, :phone, :email)"
        parameters = {
            "name":"Test",
            "address":"Test",
            "phone":"Test",
            "email":"Test"
            
        }
        result = connection.execute(statement=sqlalchemy.text(sql),parameters=parameters)
        

    ### INSERT to inventory table return ID and put inventory id in insert table
    


if __name__ == "__main__":
    main()