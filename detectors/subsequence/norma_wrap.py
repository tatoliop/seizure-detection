import numpy as np
import pandas as pd

from detectors.sources.norma.norma import NORMA
from interfaces.detector_interface import Detector_interface


class Norma_wrapper(Detector_interface):
    __detector_name = 'norma'
    __pattern_len_label = 'pattern_length'
    __nm_size_label = 'nm_size'

    def __init__(self, **kwargs):
        if 'custom_subsequence_length' in kwargs:
            self.__pattern_len = kwargs['custom_subsequence_length']
        else:
            self.__pattern_len = kwargs.get(self.__pattern_len_label, 60)
        self.__nm_size = kwargs.get(self.__nm_size_label, 3 * self.__pattern_len)

    def scoring(self, X: pd.DataFrame) -> np.array:
        clf = NORMA(self.__pattern_len, self.__nm_size)
        clf.fit(X.to_numpy())
        score = clf.decision_scores_
        return score

    # Getters
    @property
    def name(self) -> str:
        return self.__detector_name

    @property
    def params(self):
        return {
            self.__pattern_len_label: self.__pattern_len,
            self.__nm_size_label: self.__nm_size
        }

    @property
    def point(self) -> bool:
        return False
