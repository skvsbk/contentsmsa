import json
from abc import ABC, abstractmethod
from kafka import KafkaProducer

from config import Config


class Publisher(ABC):
    """Interface for concrete publishers"""
    @abstractmethod
    def attach(self, subscriber):
        pass

    @abstractmethod
    def detach(self, subscriber):
        pass

    @abstractmethod
    def notify(self):
        pass


class Subscriber(ABC):
    """Interface for concrete subscribers"""
    @abstractmethod
    def update(self, publisher):
        pass


class KafkaProducerSubscriber(Subscriber):
    """Subscriber for sending message by Kafka"""

    def update(self, publisher):
        try:
            producer = KafkaProducer(bootstrap_servers=f'{Config.BROKER_ADDRESS}:{Config.BROKER_PORT}',
                                     value_serializer=lambda m: json.dumps(m).encode('ascii'))
            producer.send(topic=Config.KAFKA_TOPIC_PRODUCER,
                          value=publisher.value,
                          key=publisher.key)
        except:
            # Write some log record
            pass


class PostPublisher(Publisher):
    """Publisher for notify concrete subscribers"""
    def __init__(self):
        self._observers = []
        self.key = None
        self.value = None

    def attach(self, subscriber):
        self._observers.append(subscriber)

    def detach(self, subscriber):
        self._observers.remove(subscriber)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def change_state(self, key, value):
        self.key = key
        self.value = value
        self.notify()
