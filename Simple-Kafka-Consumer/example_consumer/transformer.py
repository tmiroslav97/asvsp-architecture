import json
from typing import Dict, List, Optional, Tuple

from confluent_kafka import Consumer, Message, Producer
from confluent_kafka.cimpl import KafkaException

import example_consumer.config as config
from example_consumer.enrichments.user_agent import UserAgent
from example_consumer.event_extractor import EventExtractor, ExtractException
from example_consumer.logger import LogMixin


class Transformer(LogMixin):
    """ Read from a source, modify the message, write to a target/sink """

    def __init__(
        self,
        consumer_group_id: str,
        source_topic: str,
        target_topic: str,
        target_failed_topic: str,
        extractor: EventExtractor,
        stop_on_empty=False
    ):
        super().__init__()
        self.consumer_group_id = consumer_group_id
        self.source_topic = source_topic  # topic we consume from (source)
        self.target_topic = target_topic  # topic we produce to (destination)
        self.target_failed_topic = target_failed_topic  # topic we produce to if failed (destination)
        self.extractor = extractor()
        self.is_running = True  # state of the consumer
        self.sampling_message_count = 0
        self.stop_on_empty = stop_on_empty

        # Initialize Consumers and Producers
        self.logger.info("Starting Consumer with config: %s and joining Consumer Group: %s",
                         config.CONSUMER_CONFIG,
                         self.consumer_group_id)
        self.consumer = Consumer(config.CONSUMER_CONFIG)  # Used to read from a Kafka topic
        self.producer_valid = Producer(config.PRODUCER_CONFIG)  # Used to write to a Kafka topic
        self.producer_invalid = Producer(config.PRODUCER_CONFIG)  # Used to write to a Kafka topic
        self.logger.info("Consumer subscribing to topic: %s", self.source_topic)
        self.consumer.subscribe([self.source_topic])  # Specifies which topic to fetch/consume from

    def _acked(self, err, message: Message, event_type: str):
        """ Acknowledgement regarding delivery of a produced message """
        if err is not None:
            self.logger.error("Failed to produce message: 'Topic=%s | Key=%s | Timestamp=%s'. Error message: %s",
                              message.topic(),
                              message.key(),
                              message.timestamp()[1],
                              err)
        else:
            self.logger.debug("Message produced: 'Topic=%s | Key=%s | Timestamp=%s'",
                              message.topic(),
                              message.key(),
                              message.timestamp()[1])

    def validate_message(self, message: Dict):
        """ Validate and return a message """
        is_valid = True
        try:
            message_id = message.get('id', None)
            assert message_id is not None
            self.logger.debug("Validated message id: %s", message_id)
        except AssertionError as e:
            is_valid = False

        return is_valid

    def process_message(self, message: Dict) -> Tuple[bool, Optional[Dict]]:
        """ Implement this method with your transformer's logic (i.e. how you want to transform message) """
        raise NotImplementedError

    def extract_events(self, message: Message) -> List[Dict]:
        self.logger.debug("Extracting events from message: 'Topic=%s | PayloadSize=%s | Key=%s | Timestamp=%s'",
                          message.topic(),
                          len(message),
                          message.key(),
                          message.timestamp()[1])
        return self.extractor.extract(message)

    def get_events_from_source(self, kafka_message: Message) -> Tuple[List, List, List]:
        events = []
        valid_events = []
        bad_events = []
        unprocessable_messages = []
        try:
            events = self.extract_events(kafka_message)
        except ExtractException as e:
            self.logger.exception(e)
            unprocessable_messages.append(kafka_message)


        for event in events:
            # Validate the message
            is_valid = self.validate_message(event)
            if is_valid:
                # Run custom processing/transform code on the message
                is_success, message_processed = self.process_message(event)
                if is_success:
                    valid_events.append(message_processed)
                else:
                    bad_events.append(event)

            else:
                bad_events.append(event)

        return valid_events, bad_events, unprocessable_messages

    def send_valid_events_to_target(self, valid_events: List) -> None:
        for event in valid_events:
            message_id = event['id']
            self.logger.debug('Producing message id {} to topic: {}'.format(message_id, config.KAFKA_ENRICHED_TOPIC))
            try:
                self.producer_valid.produce(
                    topic=self.target_topic,
                    key=message_id,
                    value=json.dumps(event),
                    callback=lambda err, message: self._acked(err, message, "valid_event")
                )
                self.producer_valid.poll(config.PRODUCER_CONFIG_POLL_TIMEOUT)
            except KafkaException as e:
                # For now, increment metric and skip on any type of Kafka error
                self.logger.exception("Failed to produce to %s due to KafkaException", self.target_topic)

    def send_invalid_events_to_target(self, bad_events: List) -> None:
        for event in bad_events:
            # Write the invalid event to an invalid topic
            self.logger.error("Producing invalid event to %s", self.target_failed_topic)
            try:
                self.producer_invalid.produce(
                    topic=self.target_failed_topic,
                    value=json.dumps(event),
                    callback=lambda err, message: self._acked(err, message, "invalid_event")
                )
                self.producer_invalid.poll(config.PRODUCER_CONFIG_POLL_TIMEOUT)
            except KafkaException as e:
                # For now, increment metric and skip on any type of Kafka error
                self.logger.exception("Failed to produce to %s due to KafkaException", self.target_failed_topic)

    def send_unprocessable_messages_to_target(self, bad_messages: List[Message]) -> None:
        for bad_message in bad_messages:
            # Write the invalid message to an invalid topic
            self.logger.error("Producing invalid message to %s", self.target_failed_topic)
            try:
                self.producer_invalid.produce(
                    topic=self.target_failed_topic,
                    value=bad_message.value(),
                    callback=lambda err, message: self._acked(err, message, "unprocessable_message")
                )
                self.producer_invalid.poll(config.PRODUCER_CONFIG_POLL_TIMEOUT)
            except KafkaException as e:
                self.logger.exception("Failed to produce to %s due to KafkaException", self.target_failed_topic)

    def pre_execute(self):
        """ Execute prior to running transform """
        self.logger.info("Running transformer %s...", type(self).__name__)

    def run(self):
        """ Main method to get messages from the source, process the messages, write to destination """
        self.pre_execute()
        try:
            while self.is_running:
                # Get the Kafka Message from the Topic
                kafka_message = self.consumer.poll(timeout=config.CONSUMER_CONFIG_POLL_TIMEOUT)
                if kafka_message is None:
                    if self.stop_on_empty:
                        self.is_running = False
                    continue
                if kafka_message.error():
                    self.logger.exception("Consumer error: %s", kafka_message.error())
                    self.is_running = False
                    raise kafka_message.error()  # KafkaError

                valid_events, bad_events, unprocessable_messages = self.get_events_from_source(kafka_message)

                self.send_valid_events_to_target(valid_events)
                self.send_invalid_events_to_target(bad_events)
                self.send_unprocessable_messages_to_target(unprocessable_messages)

                self.consumer.commit(asynchronous=False)  # Synchronous guarantees, Asynchronous will speed up

        except Exception as e:
            self.logger.exception(e)
        finally:
            self.logger.info("Shutting down Consumer: %s", self.consumer_group_id)
            self.producer_valid.flush()
            self.producer_invalid.flush()
            self.consumer.close()  # Close down consumer to commit final offsets,
            # by default, autocommit=True (waits indefinitely for any needed cleanup)
            # https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html#kafka.KafkaConsumer.close
            self.logger.info("Consumer: %s successfully closed", self.consumer_group_id)


class EventEnricher(Transformer):
    """ A transformer that enriches raw records with additional data (e.g. ip geolocation) """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_agent = UserAgent()
        self.enrichments = [self.user_agent]

    def pre_execute(self):
        super().pre_execute()
        self.logger.info("\n".join([
            "The following enrichments are enabled:",
            *[f"  {enrichment.description}" for enrichment in self.enrichments],
        ]))

    def process_message(self, message: Dict) -> Tuple[bool, Optional[Dict]]:
        """ Process Message """
        is_success = True
        message_enriched = None
        for enrichment in self.enrichments:
            self.logger.debug("Applying enrichment: %s", enrichment.description)

            try:
                message_enriched = enrichment.enrich(message)
            except KeyError as e:
                self.logger.exception("Error (%s) with message", e)
                is_success = False
                return is_success, None
        return is_success, message_enriched
