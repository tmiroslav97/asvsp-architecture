import abc
from typing import Dict

from example_consumer.logger import LogMixin


class Enrichment(abc.ABC, LogMixin):
    """ Modify the event with additional data """
    def __init__(self):
        LogMixin.__init__(self)
        self.logger.info("Initializing %s Enrichment", self.description)

    @property
    def description(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def enrich(self, record: Dict) -> Dict:
        pass
