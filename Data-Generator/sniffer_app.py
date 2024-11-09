import json
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from functools import partial

import jsonlines
from confluent_kafka import Producer
from scapy.all import sniff
from scapy.packet import Packet

logging.basicConfig(
    filename="./logs/" + datetime.now().strftime("run_%Y-%m-%d-%H-%M.log"),
    filemode="w",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SniffingAPP")


DATA_GENERATOR_NETWORK_INTERFACES = os.getenv("DATA_GENERATOR_NETWORK_INTERFACES", "enp2s0,lo").split(",")
DATA_GENERATOR_PACKET_COUNT = int(os.getenv("DATA_GENERATOR_PACKET_COUNT", "300"))
DATA_GENERATOR_OUTPUT_MODE = os.getenv("DATA_GENERATOR_OUTPUT_MODE", "Kafka")
DATA_GENERATOR_KAFKA_BOOTSTRAP_SERVERS = os.getenv("DATA_GENERATOR_KAFKA_BOOTSTRAP_SERVERS", "localhost:29092,localhost:29093")
DATA_GENERATOR_KAFKA_TOPIC = os.getenv("DATA_GENERATOR_KAFKA_TOPIC", "network_data")


class Writer(ABC):
    @abstractmethod
    def write(self, data):
        raise NotImplementedError()


class JsonLinesFileWriter(Writer):
    def __init__(self, file_name: str, mode: str="w"):
        self.writer = jsonlines.open(file=file_name, mode=mode)

    def write(self, data: dict):
        logger.info("Writing data to file...")
        self.writer.write(data)

    def __del__(self):
        if self.writer:
            logger.info("Closing the resource")
            self.writer.close()


class KafkaTopicWriter(Writer):
    def __init__(self, bootstrap_servers: str, topic_name: str):
        self.topic_name = topic_name
        self.bootstrap_servers = bootstrap_servers

        self.producer_config = {
            "bootstrap.servers": self.bootstrap_servers,
        }
        self.producer = Producer(self.producer_config)

    def write(self, data: dict):
        logger.info(f"Writing data to Kafka topic: {self.topic_name}...")
        try:
            self.producer.produce(topic=self.topic_name, value=json.dumps(data))
        except Exception as e:
            logger.error("An error ocurred while sending data to Kafka topic")
            logger.exception(e)


class PacketDataExtractor:
    def get_packet_layers(self, packet: Packet):
        layers = []

        for layer in packet.layers():
            if layer is None:
                break
            layers.append(layer.__name__)
        return layers

    def extract(self, packet: Packet) -> dict:
        logger.info("Extracting a packet...")
        top_layer_dict = None
        previous_layer_dict = None

        packet_received_at = datetime.strftime(
            datetime.now(timezone.utc), "%Y-%m-%d %H:%M:%S"
        )

        for packet_layer in self.get_packet_layers(packet):
            current_layer = packet[packet_layer]
            current_layer_dict = {k: v for (k, v) in current_layer._command(json=True)}

            if not top_layer_dict:
                top_layer_dict = current_layer_dict
                top_layer_dict["packet_received_at"] = packet_received_at

            if packet_layer == "TCP":
                if current_layer_dict["dport"] in [80, 8091, 8092] or current_layer_dict["sport"] in [80, 8091, 8092]:
                    current_layer_dict["protocol"] = "HTTP"
                elif (
                    current_layer_dict["dport"] == 443 or current_layer_dict["sport"] == 443
                ):
                    current_layer_dict["protocol"] = "HTTPS"
                else:
                    current_layer_dict["protocol"] = "OTHER"

            current_layer_dict["layer_type"] = packet_layer

            if previous_layer_dict:
                previous_layer_dict["payload"] = current_layer_dict

            previous_layer_dict = current_layer_dict

        return top_layer_dict


def packet_callback(packet: Packet, extractor: PacketDataExtractor, writer: Writer):
    writer.write(extractor.extract(packet))


def main():
    logger.info("Sniffing App started")
    logger.info(f"Starting up with the following setup: NETWORK_INTERFACES: {str(DATA_GENERATOR_NETWORK_INTERFACES)}, OUTPUT_MODE: {DATA_GENERATOR_OUTPUT_MODE}, PACKET_COUNT: {DATA_GENERATOR_PACKET_COUNT}")
    # show_interfaces()  # TODO: use this to see which interfaces are available

    extractor = PacketDataExtractor()

    if DATA_GENERATOR_OUTPUT_MODE == 'File':
        writer = JsonLinesFileWriter("./prepared_data/packets_new_multi.jsonl", mode="a")
    elif DATA_GENERATOR_OUTPUT_MODE == 'Kafka':
        logger.info("Using Kafka output mode, bootstrap servers: {DATA_GENERATOR_KAFKA_BOOTSTRAP_SERVERS}, kafka topic: {DATA_GENERATOR_KAFKA_TOPIC}")

        writer = KafkaTopicWriter(bootstrap_servers= DATA_GENERATOR_KAFKA_BOOTSTRAP_SERVERS,topic_name=DATA_GENERATOR_KAFKA_TOPIC)
    
    partial_packet_callback = partial(packet_callback, extractor=extractor, writer=writer)

    try:
        sniff(prn=partial_packet_callback, iface=DATA_GENERATOR_NETWORK_INTERFACES, count=DATA_GENERATOR_PACKET_COUNT, store=False)
    except Exception as e:
        logger.error("A top level exception has ocurred!")
        logger.exception(e)


if __name__ == "__main__":
    main()
