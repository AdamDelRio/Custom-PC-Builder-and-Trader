import os
import dotenv
from sqlalchemy import create_engine

def database_connection_url():
    dbtype = 'local'
    if dotenv.load_dotenv() == False:
        dotenv.load_dotenv(dotenv_path="passwords.env")
    if dbtype == 'local':
        dotenv.load_dotenv('passwords.env')
        DB_USER: str = os.environ.get("POSTGRES_USER")
        DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
        DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
        DB_PORT: str = os.environ.get("POSTGRES_PORT")
        DB_NAME: str = os.environ.get("POSTGRES_DB")
        return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
    return os.environ.get("POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True, isolation_level="REPEATABLE READ")