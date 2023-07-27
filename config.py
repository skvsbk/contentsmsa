import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv('contentmsa.env'))


class Config:
    # === Kafka ===
    BROKER_ADDRESS = os.getenv('BROKER_ADDRESS')
    BROKER_PORT = os.getenv('BROKER_PORT')
    KAFKA_TOPIC_PRODUCER = os.getenv('KAFKA_TOPIC_PRODUCER')
    KAFKA_TOPIC_CONSUMER = os.getenv('KAFKA_TOPIC_CONSUMER')
    KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID')

    # === Database ===
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_CONNECTOR = os.getenv('DB_CONNECTOR')

    # Handlers
    AVAILABLE_REQUESTS = ['get_posts_list',
                          'get_authors_id_posts_list',
                          'get_posts_id',
                          'get_posts_with_authors_list']
