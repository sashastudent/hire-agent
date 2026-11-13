import sqlalchemy as db
from sqlalchemy import create_engine, text
import pandas as pd

SERVER = 'localhost'
DATABASE = 'Tech'
DRIVER = 'ODBC+Driver+17+for+SQL+Server'
USERNAME = 'tech_user'
PASSWORD = 'x0MnwoR7'
DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

engine = db.create_engine(DATABASE_CONNECTION)
connection = engine.connect()
metadata = db.MetaData()

#check if the connection is successful
# if __name__ == "__main__":
#     try:
#         with engine.connect() as conn:
#             result = conn.execute(text("SELECT DB_NAME()"))
#             print("Connected successfully to:", result.scalar())
#     except Exception as e:
#         print("Connection failed:", e)