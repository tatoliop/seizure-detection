from abc import ABC, abstractmethod

from models.record import Record


class Feature_extraction_interface(ABC):

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def transform(self, input_record: Record) -> Record:
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def params(self) -> dict:
        pass

