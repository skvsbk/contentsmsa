import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv('contentnsa.env'))


class Config:
    BROKER_ADDRESS = os.getenv('BROKER_ADDRESS')
    BROKER_PORT = os.getenv('BROKER_PORT')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_CONNECTOR = os.getenv('DB_CONNECTOR')
