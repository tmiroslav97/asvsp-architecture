"""Configurations

For producer and consumer configs, look at the lower level library configs as reference:
https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
"""
import dotenv
import os


DOTENV_LOCATION = f"{os.path.dirname(os.path.abspath(__file__))}/.env"


def get_env(var_name: str, default=None) -> str:
    """
    Retrieve an environment value, using the following priority order:
    1. .env file
    2. Environment variable
    :return:
    """

    existing_dotenv = dotenv.dotenv_values(DOTENV_LOCATION)
    return existing_dotenv.get(var_name, os.getenv(var_name, default=default))


# General
LOG_LEVEL = get_env('LOG_LEVEL', default='error').lower()

# Kafka, Consumer, Producer
BOOTSTRAP_SERVERS = get_env('BOOTSTRAP_SERVERS', default='kafka:9092')

CONSUMER_CONFIG_ENABLE_AUTO_COMMIT = get_env('CONSUMER_CONFIG_ENABLE_AUTO_COMMIT', default='False')
CONSUMER_CONFIG_AUTO_OFFSET_RESET = get_env('CONSUMER_CONFIG_AUTO_OFFSET_RESET', default='earliest')
CONSUMER_CONFIG_FETCH_MIN_BYTES = get_env('CONSUMER_CONFIG_FETCH_MIN_BYTES', '1')  # see PRODUCER_CONFIG_MESSAGE_MAX_BYTES
CONSUMER_CONFIG_GROUP_ID = get_env('CONSUMER_CONFIG_GROUP_ID', default='example-consumer')
CONSUMER_CONFIG_POLL_TIMEOUT = int(get_env('CONSUMER_CONFIG_POLL_TIMEOUT', '1'))

UUID_NAMESPACE = get_env('UUID_NAMESPACE', 'f6d14bcc-40d7-11ec-b754-dffd8e59d5da')

KAFKA_ENRICHED_TOPIC = get_env('KAFKA_ENRICHED_TOPIC', default='example_kafka_consumer.enriched')
KAFKA_ENRICHED_FAILED_TOPIC = get_env('KAFKA_ENRICHED_FAILED_TOPIC', default='example_kafka_consumer.enriched.failed')
KAFKA_RAW_TOPIC = get_env('KAFKA_RAW_TOPIC', default='example_kafka_consumer.raw')

PRODUCER_CONFIG_POLL_TIMEOUT = int(get_env('PRODUCER_CONFIG_POLL_TIMEOUT', '0'))
PRODUCER_CONFIG_MESSAGE_MAX_BYTES = int(get_env('PRODUCER_CONFIG_MESSAGE_MAX_BYTES', '1000000'))

# Consumer and Producer config
CONSUMER_CONFIG = {
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "group.id": CONSUMER_CONFIG_GROUP_ID,
    "auto.offset.reset": CONSUMER_CONFIG_AUTO_OFFSET_RESET,
    "fetch.min.bytes": CONSUMER_CONFIG_FETCH_MIN_BYTES,
    "enable.auto.commit": CONSUMER_CONFIG_ENABLE_AUTO_COMMIT,
}
PRODUCER_CONFIG = {
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "message.max.bytes": PRODUCER_CONFIG_MESSAGE_MAX_BYTES,
}

# Processor
CONSUMER_FEATURE_DEDUPLICATE = get_env('CONSUMER_FEATURE_DEDUPLICATE', 'False')
