from abc import ABC, abstractmethod

from models.record import Record
from models.record_id import Record_id


class Load_data_interface(ABC):
    # TODO add stuff for streaming (e.g. interval, timestamps, etc)

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def load_data(self, record_id: Record_id) -> Record:
        pass

    @abstractmethod
    def records(self) -> list[Record_id]:
        pass
