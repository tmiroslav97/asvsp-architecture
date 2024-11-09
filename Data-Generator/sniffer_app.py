import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from functools import partial

import jsonlines
from confluent_kafka import Producer
from scapy.all import sniff

logging.basicConfig(
    filename="./logs/" + datetime.now().strftime("run_%Y-%m-%d-%H-%M.log"),
    filemode="w",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SniffingAPP")

all_packet_data = []
packet_count: int = 0


class Writer(ABC):
    @abstractmethod
    def write(self, data):
        raise NotImplementedError()


class FileWriter(Writer):
    def __init__(self, file_name, mode="w"):
        self.writer = jsonlines.open(file=file_name, mode=mode)

    def write(self, data):
        logger.info("Writing data to file...")
        self.writer.write(data)

    def __del__(self):
        if self.writer:
            logger.info("Closing the resource")
            self.writer.close()

class KafkaTopicWriter(Writer):
    def __init__(self, topic_name):
        self.topic_name = topic_name
        self.producer_config = {  # TODO
            "bootstrap.servers": 'localhost:29092,localhost:29093',
        }
        self.producer = Producer(self.producer_config)

    def write(self, data):
        logger.info(f"Writing data to Kafka topic: {self.topic_name}...")
        try:
            self.producer.produce(topic=self.topic_name, value=json.dumps(data))
        except Exception as e:
            logger.error("An error ocurred while sending data to Kafka topic")
            logger.exception(e)


def get_packet_layers(packet):
    layers = []

    for layer in packet.layers():
        if layer is None:
            break
        layers.append(layer.__name__)
    return layers


# Function to process each packet
def extract_packet_data(packet):
    logger.info("Processing a packet...")
    top_layer_dict = None
    previous_layer_dict = None

    packet_received_at = datetime.strftime(
        datetime.now(timezone.utc), "%Y-%m-%d %H:%M:%S"
    )

    for packet_layer in get_packet_layers(packet):
        current_layer = packet[packet_layer]
        current_layer_dict = {k: v for (k, v) in current_layer._command(json=True)}

        if packet_layer == "TCP":
            if current_layer_dict["dport"] in [80, 8091, 8092] or current_layer_dict["sport"] in [80, 8091, 8092]:  # Proveriti da li treba i sport...
                current_layer_dict["protocol"] = "HTTP"
            elif (
                current_layer_dict["dport"] == 443 or current_layer_dict["sport"] == 443
            ):
                current_layer_dict["protocol"] = "HTTPS"
            else:
                current_layer_dict["protocol"] = "OTHER"

        if not top_layer_dict:
            top_layer_dict = current_layer_dict
            top_layer_dict["packet_received_at"] = packet_received_at

        current_layer_dict["layer_type"] = packet_layer

        if previous_layer_dict:
            previous_layer_dict["payload"] = current_layer_dict

        previous_layer_dict = current_layer_dict

    return top_layer_dict


# Sniff packets on the network (use 'Wi-Fi'/ 'eth0' / 'all' or your interface)
def main():
    logger.info("Sniffing App started")
    # TODO: print current setup
    # TODO: vars to global consts?
    # show_interfaces()  # TODO: use this to see which interfaces are available
    network_interfaces = ["enp2s0", "lo"]  # TODO: change - selected interface to sniff
    packet_count = 30  # Number of packets to process
    output_mode = 'File'  # TODO: take this from a cli arg
    if output_mode == 'File':
        writer = FileWriter("./output/packets_new_multi.jsonl", mode="a")
    elif output_mode == 'Kafka':
        writer = KafkaTopicWriter(topic_name='network_data')
    
    try:
        
        def packet_callback(packet, writer):
            writer.write(extract_packet_data(packet))
        partial_packet_callback = partial(packet_callback, writer=writer)

        for i in range(1, 30):  # TODO delete this
            sniff(prn=partial_packet_callback, iface=network_interfaces, count=packet_count, store=False)
    except Exception as e:
        logger.error("A top level exception has ocurred!")
        logger.exception(e)


if __name__ == "__main__":
    main()
