import numpy as np
from sklearn.preprocessing import MinMaxScaler

from interfaces.postprocessing_interface import Postprocessing_interface
from utils import constants


class Min_max_scaler_postprocessing(Postprocessing_interface):
    __feature_name = 'min_max_scaler'
    __target_min_label = 'target_min'
    __target_max_label = 'target_max'

    def __init__(self, **kwargs):
        self.__target_min = kwargs.get(self.__target_min_label, 0)
        self.__target_max = kwargs.get(self.__target_max_label, 1)

    def transform(self, scores: np.ndarray) -> np.ndarray:
        res = (MinMaxScaler(feature_range=(self.__target_min, self.__target_max)).fit_transform(scores.reshape(-1, 1)).ravel())
        return res

    # Getters
    @property
    def name(self) -> str:
        return self.__feature_name

    @property
    def params(self):
        return {
            self.__target_min_label: self.__target_min,
            self.__target_max_label: self.__target_max
        }
