from interfaces.feature_extraction_interface import Feature_extraction_interface
from models.record import Record


class Default_feature(Feature_extraction_interface):
    __feature_name = 'default'

    def __init__(self, **kwargs):
        pass

    def transform(self, input_record: Record) -> Record:
        return input_record

    # Getters
    @property
    def name(self) -> str:
        return self.__feature_name

    @property
    def params(self):
        return {
        }
