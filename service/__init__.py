from . import transmitters


result_submission_publisher = transmitters.PostPublisher()
kafka_producer_subscriber = transmitters.KafkaProducerSubscriber()

result_submission_publisher.attach(kafka_producer_subscriber)
