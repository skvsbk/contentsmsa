from sqlalchemy import create_engine
import mysql.connector
from sqlalchemy.orm import sessionmaker
from model.models import Base
from config import Config


# Check the database on the server and create it if not
conn = mysql.connector.connect(
    host=Config.DB_HOST,
    user=Config.DB_USER,
    passwd=Config.DB_PASSWORD
)

cursor = conn.cursor()
databases = f"show databases like '{Config.DB_NAME}'"
cursor.execute(databases)

try:
    if cursor.fetchone() is None:
        cursor.execute(f"create database {Config.DB_NAME}")
except StopIteration:
    cursor.execute(f"create database {Config.DB_NAME}")

# Connect to database
try:
    engine = create_engine(f'{Config.DB_CONNECTOR}://'
                           f'{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}')
    # engine.connect()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
except Exception as e:
    print(e)
