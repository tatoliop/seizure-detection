import math

import numpy as np
import pandas as pd

from interfaces.detector_interface import Detector_interface
from detectors.sources.s2g.series2graph import Series2Graph


class Series2graph_wrapper(Detector_interface):
    __detector_name = 'series2graph'
    __pattern_len_label = 'pattern_length'
    __query_len_label = 'query_length'

    def __init__(self, **kwargs):
        if 'custom_subsequence_length' in kwargs:
            self.__query_len = kwargs['custom_subsequence_length']
        else:
            self.__query_len = kwargs.get(self.__query_len_label, 60)
        self.__pattern_len = kwargs.get(self.__pattern_len_label, math.floor(self.__query_len / 2))

    def scoring(self, X: pd.DataFrame) -> np.array:
        s2g = Series2Graph(self.__pattern_len)
        s2g.fit(X)
        s2g.score(query_length=self.__query_len, dataset=X)
        scores = s2g.decision_scores_
        return scores

    # Getters
    @property
    def name(self) -> str:
        return self.__detector_name

    @property
    def params(self):
        return {
            self.__pattern_len_label: self.__pattern_len,
            self.__query_len_label: self.__query_len
        }

    @property
    def point(self) -> bool:
        return False
