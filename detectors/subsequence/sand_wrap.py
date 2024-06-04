import sys

import numpy as np
import pandas as pd

from detectors.sources.sand import SAND
from interfaces.detector_interface import Detector_interface


class SAND_wrapper(Detector_interface):
    __detector_name = 'SAND'
    __pattern_len_label = 'pattern_length'
    __subsequence_len_label = 'subsequence_length'

    def __init__(self, **kwargs):
        if 'custom_subsequence_length' in kwargs:
            self.__pattern_len = kwargs['custom_subsequence_length']
        else:
            self.__pattern_len = kwargs.get(self.__pattern_len_label, 60)
        self.__subsequence_len = kwargs.get(self.__subsequence_len_label, 4 * self.__pattern_len)

    def scoring(self, X: pd.DataFrame) -> np.array:
        clf = SAND(self.__pattern_len, self.__subsequence_len)
        clf.fit(X)
        scores = clf.decision_scores_
        np.set_printoptions(threshold=sys.maxsize)
        # Skip the first X values since they are the same for the subsequence length
        scores_final = scores[(self.__pattern_len-1):-1]
        return scores_final

    # Getters
    @property
    def name(self) -> str:
        return self.__detector_name

    @property
    def params(self):
        return {
            self.__pattern_len_label: self.__pattern_len,
            self.__subsequence_len_label: self.__subsequence_len
        }

    @property
    def point(self) -> bool:
        return False
