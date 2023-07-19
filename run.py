import json
from kafka import KafkaConsumer
from config import Config
from service import handlers
from service import result_submission_publisher


class ContentMSA:
    def __init__(self, topic_consumer: str, topic_producer: str, broker: dict, group_id: str):
        self.topic_consumer = topic_consumer
        self.topic_producer = topic_producer
        self.consumer = KafkaConsumer(self.topic_consumer,
                                      bootstrap_servers=broker,
                                      enable_auto_commit=False,
                                      group_id=group_id)

    def run(self):
        """
        Retrieving data from kafka, invoking the necessary handlers, and pushing the json back to kafka
        """
        for message in self.consumer:
            # Get data from kafka
            message_value = json.loads(message.value.decode('utf-8'))
            try:
                message.key.decode('utf-8')
            except:
                # Commit if message.key is None or can't be decode
                self.consumer.commit()
                continue

            # Consumer commit
            self.consumer.commit()

            # Depending on the received name, we call the corresponding crud
            result = self.define_handler(message_value)

            # Send result in Kafka using publisher with subscribers
            result_submission_publisher.change_state(key=message.key, value=result)

    @staticmethod
    def define_handler(message_value):
        result = {'detail': 'No haldler for request'}
        # 2
        if message_value["name"] == "get_posts_list":
            match message_value['method']:
                case 'get':
                    result = handlers.GetAllPosts().produce()
                case 'post':
                    result = handlers.CreatePost().produce(message_value)
        # 3
        if message_value["name"] == "get_authors_id_posts_list":
            result = handlers.GetPostsByAuthor().produce(message_value)

        # 4
        if message_value["name"] == "get_posts_id":
            match message_value['method']:
                case 'get':
                    result = handlers.GetPostById().produce(message_value)
                case 'put':
                    result = handlers.UpdatePost().produce(message_value)
                case 'delete':
                    result = handlers.DeletePost().produce(message_value)

        # 5
        if message_value["name"] == "get_posts_with_authors_list":
            result = handlers.GetAllPostsOrderedByUserId().produce(message_value)

        return result


if __name__ == '__main__':
    app = ContentMSA(topic_consumer=Config.KAFKA_TOPIC_CONSUMER,
                     topic_producer=Config.KAFKA_TOPIC_PRODUCER,
                     broker={Config.BROKER_ADDRESS: Config.BROKER_PORT},
                     group_id=Config.KAFKA_GROUP_ID)
    app.run()
