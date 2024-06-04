import numpy as np

from interfaces.postprocessing_interface import Postprocessing_interface


class Default_postprocessing(Postprocessing_interface):
    __feature_name = 'default'

    def __init__(self, **kwargs):
        pass

    def transform(self, scores: np.ndarray) -> np.ndarray:
        return scores

    # Getters
    @property
    def name(self) -> str:
        return self.__feature_name

    @property
    def params(self):
        return {
        }
