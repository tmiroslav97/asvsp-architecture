#!/bin/bash

/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic network_data --replication-factor 2 --partitions 2
/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic example_kafka_consumer.raw --replication-factor 1 --partitions 4
/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic example_kafka_consumer.enriched --replication-factor 1 --partitions 4
/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic example_kafka_consumer.enriched.failed --replication-factor 1 --partitions 4