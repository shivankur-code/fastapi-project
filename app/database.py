# WAY OF ORM
from requests import Session
from urllib.parse import quote  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
import time
from .config import settings

st = "shiv@123"

# SQLALCHEMY_DATABASE_URL = ("postgresql://postgres:%s@localhost:5432/fastapi", % urlquote('shiv@123'))

engine = create_engine(f'postgresql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'%quote(f'{settings.database_password}'))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="shiv@123")
#         cursor = conn.cursor()
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)

# print("Database connection was succesfull!")