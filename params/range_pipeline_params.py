from interfaces.pipeline_params_interface import Pipeline_params_interface
from utils.enums import Feature_extraction_enum, Detector_enum, Postprocessing_enum


class Range_pipeline_params(Pipeline_params_interface):

    def __init__(self,
                 feature_extraction: Feature_extraction_enum,
                 feature_extraction_params: dict,
                 model: Detector_enum,
                 model_params: dict,
                 postprocessing: Postprocessing_enum,
                 postprocessing_params: dict,
                 subsequence_size: int,
                 #slide_size: int = 1, # TODO currently slide is not usable
                 labeling_threshold: float = 0.0):
        super().__init__(feature_extraction, feature_extraction_params, model,
                         model_params, postprocessing, postprocessing_params)
        self.__subsequence_size = subsequence_size
        self.__slide_size = 1
        self.__labeling_threshold = labeling_threshold

    # Getters
    @property
    def subsequence_size(self) -> int:
        return self.__subsequence_size

    @property
    def slide_size(self) -> int:
        return self.__slide_size

    @property
    def labeling_threshold(self) -> float:
        return self.__labeling_threshold
