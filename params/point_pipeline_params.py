from interfaces.pipeline_params_interface import Pipeline_params_interface
from utils.enums import Feature_extraction_enum, Detector_enum, Postprocessing_enum


class Point_pipeline_params(Pipeline_params_interface):

    def __init__(self,
                 feature_extraction: Feature_extraction_enum,
                 feature_extraction_params: dict,
                 model: Detector_enum,
                 model_params: dict,
                 postprocessing: Postprocessing_enum,
                 postprocessing_params: dict,
                 multivariate: bool = True):
        super().__init__(feature_extraction, feature_extraction_params, model,
                         model_params, postprocessing, postprocessing_params)
        self.__multivariate = multivariate

    # Getters
    @property
    def multivariate(self) -> bool:
        return self.__multivariate
