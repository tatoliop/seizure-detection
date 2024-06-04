import numpy as np
import pandas as pd
import stumpy

from interfaces.detector_interface import Detector_interface


class MP_stumpy(Detector_interface):
    __detector_name = 'MP_stumpy'
    __pattern_len_label = 'pattern_length'

    def __init__(self, **kwargs):
        if 'custom_subsequence_length' in kwargs:
            self.__pattern_len = kwargs['custom_subsequence_length']
        else:
            self.__pattern_len = kwargs.get(self.__pattern_len_label, 60)

    def scoring(self, X: pd.DataFrame) -> np.array:
        # X = X.reshape(-1)
        mp = stumpy.stump(X, self.__pattern_len)  # Scores are distance to the closer neighbor subsequence so bigger
        score = mp[:, 0]
        return score

    # Getters
    @property
    def name(self) -> str:
        return self.__detector_name

    @property
    def params(self):
        return {
            self.__pattern_len_label: self.__pattern_len
        }

    @property
    def point(self) -> bool:
        return False
