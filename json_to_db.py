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
        part_type = filename.split(".")[0]
        schemas = [key for key in data[0].keys()]
        for value in data:
            sql = f"INSERT into part_inventory (name, type, quantity) VALUES (:name, :type, :quantity) RETURNING part_id"
            parameters = {
                "name":str(value["name"]),
                "type":str(part_type),
                "quantity":0
            }
            result = connection.execute(statement=sqlalchemy.text(sql),parameters=parameters)
            part_id = result.first()[0]
            sql = f"INSERT into {part_type}_specs (part_id, {', '.join(schemas)}) VALUES (:part_id,{', '.join([f':{column_name}' for column_name in schemas])})"
            parameters = {
                "part_id": part_id,
            }
            for schema in schemas:
                parameters[schema] = value[schema]
            
            result = connection.execute(statement=sqlalchemy.text(sql),parameters=parameters)

        ### INSERT to inventory table return ID and put inventory id in insert table
        


if __name__ == "__main__":
    main()