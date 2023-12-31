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

    # Logging
    LOG_FILENAME = './log/contentmsa.log'

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s module:%(name)s %(levelname)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "logfile": {
                "formatter": "default",
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_FILENAME,
                "backupCount": 7,
            },
        },
        # "loggers": {
        #     "contentmsa": {
        #         "level": "INFO",
        #         "handlers": [
        #             "logfile",
        #         ],
        #     },
        # },
        "root": {
            "level": "WARNING",
            "handlers": [
                "logfile",
            ]
        }
    }

    # Handlers
    AVAILABLE_REQUESTS = ['get_posts_list',
                          'get_authors_id_posts_list',
                          'get_posts_id',
                          'get_posts_with_authors_list']
