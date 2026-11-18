import os

import sqlalchemy as db
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pandas as pd

load_dotenv()  # Load variables from .env file

SERVER = os.getenv("DB_SERVER", "localhost")
DATABASE = os.getenv("DB_NAME")
DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")

if not all([DATABASE, USERNAME, PASSWORD]):
    raise RuntimeError("Missing DB_NAME / DB_USERNAME / DB_PASSWORD in .env file")

# URL.create escapes special characters in the password safely
DATABASE_CONNECTION = URL.create(
    "mssql+pyodbc",
    username=USERNAME,
    password=PASSWORD,
    host=SERVER,
    database=DATABASE,
    query={"driver": DRIVER},
)

engine = db.create_engine(DATABASE_CONNECTION)
connection = engine.connect()
metadata = db.MetaData()

#check if the connection is successful
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DB_NAME()"))
            print("Connected successfully to:", result.scalar())
    except Exception as e:
        print("Connection failed:", e)