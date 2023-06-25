import json
from kafka import KafkaConsumer, KafkaProducer
from config import Config
import crud


class ContentMSA:
    def __init__(self, topic_consumer: str, topic_producer: str, broker: dict, group_id: str):
        self.topic_consumer = topic_consumer
        self.topic_producer = topic_producer
        self.consumer = KafkaConsumer(self.topic_consumer,
                                      bootstrap_servers=broker,
                                      enable_auto_commit=False,
                                      group_id=group_id)
        self.producer = KafkaProducer(bootstrap_servers=broker,
                                      value_serializer=lambda m: json.dumps(m).encode())

    def run(self):
        """
        Retrieving data from kafka, invoking the necessary CRUD, and pushing the data back to kafka
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

            # Depending on the received name, we call the corresponding crud
            # 2
            if message_value["name"] == "get_posts_list":
                match message_value['method']:
                    case 'get':
                        # Consumer commit
                        self.consumer.commit()
                        # Database query
                        result = crud.get_all_posts()
                        # Send result in Kafka
                        self.producer.send(topic=self.topic_producer, value=result, key=message.key)
                    case 'post':
                        # Consumer commit
                        self.consumer.commit()
                        # Database query
                        result = crud.create_post(message_value)
                        # Send result in Kafka
                        self.producer.send(topic=self.topic_producer, value=result, key=message.key)
            # 3
            if message_value["name"] == "get_authors_id_posts_list":  
                # Consumer commit
                self.consumer.commit()
                # Database query
                result = crud.get_posts_by_author(message_value["user_id"])
                # Send result in Kafka
                self.producer.send(topic=self.topic_producer, value=result, key=message.key)
            # 4
            if message_value["name"] == "get_posts_id":  
                match message_value['method']:
                    case 'get':
                        # Consumer commit
                        self.consumer.commit()
                        # Database query
                        result = crud.get_post_by_id(post_id=message_value["post_id"])
                        # Send result in Kafka
                        self.producer.send(topic=self.topic_producer, value=result, key=message.key)
                    case 'put':
                        # Consumer commit
                        self.consumer.commit()
                        # Database query
                        result = crud.update_post(value=message_value)
                        # Send result in Kafka
                        self.producer.send(topic=self.topic_producer, value=result, key=message.key)
                    case'delete':
                        # Consumer commit
                        self.consumer.commit()
                        # Database query
                        result = crud.delete_post(post_id=message_value["post_id"])
                        # Send result in Kafka
                        self.producer.send(topic=self.topic_producer, value=result, key=message.key)
            # 5
            if message_value["name"] == "get_posts_with_authors_list":
                # Consumer commit
                self.consumer.commit()
                # Database query
                result = crud.get_all_posts_ordered_by_userid()
                # Send result in Kafka
                self.producer.send(topic=self.topic_producer, value=result, key=message.key)


if __name__ == '__main__':
    app = ContentMSA(topic_consumer=Config.KAFKA_TOPIC_CONSUMER,
                     topic_producer=Config.KAFKA_TOPIC_PRODUCER,
                     broker={Config.BROKER_ADDRESS: Config.BROKER_PORT},
                     group_id=Config.KAFKA_GROUP_ID)
    app.run()
