import json
from kafka import KafkaConsumer
from config import Config
from service import handlers
# from service import result_submission_publisher


class ContentMSA:
    """Retrieving data from kafka, invoking the necessary handlers"""

    def __init__(self, topic_consumer: str, topic_producer: str, broker: dict, group_id: str):
        self.topic_consumer = topic_consumer
        self.topic_producer = topic_producer
        self.consumer = KafkaConsumer(self.topic_consumer,
                                      bootstrap_servers=broker,
                                      enable_auto_commit=False,
                                      group_id=group_id)

    def run(self):
        for message in self.consumer:
            # Get data from kafka

            try:
                message_value = json.loads(message.value.decode('utf-8'))
                message.key.decode('utf-8')
            except Exception as e:
                # Write some log record
                message_value = {'detail': 'Data consuming error'}

            # Consumer commit
            self.consumer.commit()

            # Depending on the received name (route, request), call the corresponding handler
            handlers.DefineHandler(message_value, message.key).execute_handler()



if __name__ == '__main__':
    app = ContentMSA(topic_consumer=Config.KAFKA_TOPIC_CONSUMER,
                     topic_producer=Config.KAFKA_TOPIC_PRODUCER,
                     broker={Config.BROKER_ADDRESS: Config.BROKER_PORT},
                     group_id=Config.KAFKA_GROUP_ID)
    app.run()
