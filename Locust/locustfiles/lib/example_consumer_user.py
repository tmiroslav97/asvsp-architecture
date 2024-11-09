from locust import task, constant_throughput
import os
import json

from .sample_data import get_valid_data, get_invalid_data
from .kafka_client import KafkaUser


def format_message(data):
    return json.dumps(data)


class ExampleConsumerUser(KafkaUser):
    bootstrap_servers = os.getenv("LOCUST_KAFKA_SERVERS", "localhost:29092")
    wait_time = constant_throughput(int(os.getenv('LOCUST_THROUGHPUT_CONSTANT', '2')))

    @task(99)  # 99/100
    def send_valid_message_task(self):
        topic = os.getenv("LOCUST_KAFKA_RAW_TOPIC", "example_kafka_consumer.raw")
        self.client.send(topic, json.dumps(get_valid_data()))
        self.client.producer.poll(1)

    @task(1)  # 1/100
    def send_invalid_message_task(self):
        topic = os.getenv("LOCUST_KAFKA_RAW_TOPIC", "example_kafka_consumer.raw")
        self.client.send(topic, json.dumps(get_invalid_data()))
        self.client.producer.poll(1)
