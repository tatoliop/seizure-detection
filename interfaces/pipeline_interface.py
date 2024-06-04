from abc import ABC, abstractmethod

import numpy as np

from metrics.metrics import Metrics
from interfaces.pipeline_params_interface import Pipeline_params_interface
from models.record import Record


class Pipeline_interface(ABC):
    __feature_extraction_prefix = 'feature_extraction_'
    __detector_prefix = 'detector_'
    __postprocessor_prefix = 'postprocessor_'

    def __init__(self, params: Pipeline_params_interface):
        self.__feature_extractor = params.feature_extraction.value(**params.feature_extraction_params)
        self.__detector = params.model.value(**params.model_params)
        self.__postprocessor = params.postprocessing.value(**params.postprocessing_params)
        self.__evaluator = Metrics()

    @abstractmethod
    def execute(self, input_record: Record):
        pass

    def get_features(self, input_data: Record) -> Record:
        features = self.feature_extractor.transform(input_data)
        return features

    def postprocess(self, scores: np.array) -> np.array:
        features = self.postprocessor.transform(scores)
        return features

    @property
    def feature_extractor(self):
        return self.__feature_extractor

    @property
    def detector(self):
        return self.__detector

    @property
    def postprocessor(self):
        return self.__postprocessor

    @property
    def evaluator(self):
        return self.__evaluator

    @property
    def params(self) -> dict:
        feature_extraction_params = self.__feature_extractor.params
        detector_params = self.__detector.params
        postprocessor_params = self.__postprocessor.params
        prefixed_fe_dict = {self.__feature_extraction_prefix + str(key): val for key, val in
                            feature_extraction_params.items()}
        prefixed_detector_dict = {self.__detector_prefix + str(key): val for key, val in detector_params.items()}
        prefixed_postprocessor_dict = {self.__postprocessor_prefix + str(key): val for key, val in
                                       postprocessor_params.items()}
        final_dict = prefixed_fe_dict | prefixed_detector_dict | prefixed_postprocessor_dict
        return final_dict

    @property
    def technique_names(self) -> dict:
        feature_extraction = {self.__feature_extraction_prefix + 'technique': self.__feature_extractor.name}
        model = {self.__detector_prefix + 'technique': self.__detector.name}
        postprocessor = {self.__postprocessor_prefix + 'technique': self.__postprocessor.name}
        final_dict = feature_extraction | model | postprocessor
        return final_dict

    @abstractmethod
    def metrics(self, **kwargs) -> dict[str: dict]:
        pass
