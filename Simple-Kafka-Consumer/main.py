import example_consumer.config as config
from example_consumer.event_extractor import JsonEventExtractor
from example_consumer.transformer import EventEnricher

if __name__ == '__main__':
    event_enricher = EventEnricher(
        consumer_group_id = config.CONSUMER_CONFIG_GROUP_ID,
        source_topic = config.KAFKA_RAW_TOPIC,
        target_topic = config.KAFKA_ENRICHED_TOPIC,
        target_failed_topic = config.KAFKA_ENRICHED_FAILED_TOPIC,
        extractor = JsonEventExtractor
    )
    event_enricher.run()
