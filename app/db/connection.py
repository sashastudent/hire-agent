import os

import sqlalchemy as db
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pandas as pd

load_dotenv()  # Load variables from .env file

SERVER = os.getenv("DB_SERVER", "localhost")
DATABASE = os.getenv("DB_NAME", "TECH")
DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
AUTH_MODE = os.getenv("DB_AUTH_MODE", "sql").strip().lower()
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")

if not DATABASE:
    raise RuntimeError("Missing DB_NAME in .env file")

if AUTH_MODE not in {"sql", "windows"}:
    raise RuntimeError("Missing DB_AUTH_MODE in .env file. It must be 'sql' or 'windows'")

connection_query = {"driver": DRIVER}
if AUTH_MODE == "windows":
    connection_query["trusted_connection"] = "yes"
else:
    if not all([USERNAME, PASSWORD]):
        raise RuntimeError("Missing DB_USERNAME / DB_PASSWORD in .env file")

# URL.create escapes special characters in the password safely
DATABASE_CONNECTION = URL.create(
    "mssql+pyodbc",
    username=USERNAME if AUTH_MODE == "sql" else None,
    password=PASSWORD if AUTH_MODE == "sql" else None,
    host=SERVER,
    database=DATABASE,
    query=connection_query,
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