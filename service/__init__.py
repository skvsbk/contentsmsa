from . import observer


result_submission_publisher = observer.PostPublisher()
kafka_producer_subscriber = observer.KafkaProducerSubscriber()

result_submission_publisher.attach(kafka_producer_subscriber)
