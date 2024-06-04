from abc import ABC

from utils.enums import Feature_extraction_enum, Detector_enum, Postprocessing_enum


class Pipeline_params_interface(ABC):

    def __init__(self,
                 feature_extraction: Feature_extraction_enum,
                 feature_extraction_params: dict,
                 model: Detector_enum,
                 model_params: dict,
                 postprocessing: Postprocessing_enum,
                 postprocessing_params: dict
                 ):
        self.__feature_extraction = feature_extraction
        self.__feature_extraction_params = feature_extraction_params
        self.__model = model
        self.__model_params = model_params
        self.__postprocessing = postprocessing
        self.__postprocessing_params = postprocessing_params

    # Getters
    @property
    def feature_extraction(self) -> Feature_extraction_enum:
        return self.__feature_extraction

    @property
    def feature_extraction_params(self) -> dict:
        return self.__feature_extraction_params

    @property
    def model(self) -> Detector_enum:
        return self.__model

    @property
    def model_params(self) -> dict:
        return self.__model_params

    @property
    def postprocessing(self) -> Postprocessing_enum:
        return self.__postprocessing

    @property
    def postprocessing_params(self) -> dict:
        return self.__postprocessing_params
