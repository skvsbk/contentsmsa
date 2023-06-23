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
        for message in self.consumer:
            message_value = json.loads(message.value.decode('utf-8'))  # dict {"name": "get_posts_with_author_list"}
            try:
                message.key.decode('utf-8')  # key=b'unique string for determine message 9929'
            except:
                # Commit if message.key is None or can't be decode
                self.consumer.commit()
                continue

            if message_value["name"] == "get_posts_list": # 2
                self.consumer.commit()
                # Query from DB
                result = [item.to_dict() for item in crud.get_all_posts()]
                # Send result to kafka
                self.producer.send(topic=self.topic_producer, value=result,
                                   key=message.key)

            if message_value["name"] == "get_authors_id_posts_list":  # 3
                self.consumer.commit()
                # Query from DB
                result = [i.to_dict() for i in crud.get_posts_by_author(message_value["user_id"])]
                # Send result to kafka
                self.producer.send(topic=self.topic_producer, value=result,
                                   key=message.key)

            if message_value["name"] == "get_posts_id":  # 4
                match message_value['method']:
                    case 'get':
                        # Query from DB
                        result = crud.get_post_by_id(post_id=message_value["post_id"]).to_dict()
                        # Send result to kafka
                        self.producer.send(topic=self.topic_producer, value=result,
                                           key=message.key)
                    case 'post':
                        result = crud.create_post(value=message_value)
                    case 'put':
                        # value = {'name': 'post_posts_id', 'user_id': user_id,
                        #         'method': 'post', 'title': request.data['title'], 'body': request.data['body']},
                        result = crud.update_post(value=message_value)
                    case'delete':
                        result = crud.delete_post(post_id=message_value["post_id"])

            if message_value["name"] == "get_posts_with_authors_list":  # 5
                # value = {'name': 'get_posts_with_authors_list'},
                result = crud.get_all_posts()


if __name__ == '__main__':
    app = ContentMSA(topic_consumer=Config.KAFKA_TOPIC_CONSUMER,
                     topic_producer=Config.KAFKA_TOPIC_PRODUCER,
                     broker={Config.BROKER_ADDRESS: Config.BROKER_PORT},
                     group_id=Config.KAFKA_GROUP_ID)
    app.run()
