import abc
import base64
import json
import uuid
from typing import Dict, List
from urllib.parse import parse_qs

from jsonpath_ng import parse as jsonpath_parse

import example_consumer.config as config
from example_consumer.logger import LogMixin

UUID_NAMESPACE = config.UUID_NAMESPACE


class ExtractException(Exception):
    pass


class DeserializationException(ExtractException):
    pass


class EventMappingException(ExtractException):
    pass


class EventExtractor(abc.ABC, LogMixin):
    def extract(self, message):
        message_obj = self.deserialize_message(message)
        return self.map_events(message_obj)

    @abc.abstractmethod
    def deserialize_message(self, message):
        pass

    @abc.abstractmethod
    def map_events(self, message_obj) -> List[Dict]:
        pass


class JsonEventExtractor(EventExtractor):
    def deserialize_message(self, kafka_message):
        try:
            if kafka_message.value() is not None:
                return json.loads(kafka_message.value())
            else:
                return None
        except Exception as e:
            raise DeserializationException(e)

    def map_events(self, message_obj):
        if message_obj:
            return [message_obj]
        else:
            return []
