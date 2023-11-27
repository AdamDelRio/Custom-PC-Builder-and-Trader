import sqlalchemy
from json import load
from src import database as db

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from sys import argv

def main():
    print('test')
    with db.engine.begin() as connection:
        sql = 'SELECT part_id, price from part_inventory'
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




if __name__ == "__main__":
    main()