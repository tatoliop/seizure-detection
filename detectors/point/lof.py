import numpy as np
import pandas as pd

from interfaces.detector_interface import Detector_interface
from sklearn.neighbors import LocalOutlierFactor


class Lof(Detector_interface):
    __detector_name = 'lof'
    __subsequence_label = 'subsequence'
    __n_neighbors_label = 'n_neighbors'
    __algorithm_label = 'algorithm'
    __leaf_size_label = 'leaf_size'
    __metric_label = 'metric'
    __p_label = 'p'
    __metric_params_label = 'metric_params'
    __contamination_label = 'contamination'
    __n_jobs_label = 'n_jobs'

    def __init__(self, **kwargs):
        self.__n_neighbors = kwargs.get(self.__n_neighbors_label, 20)
        self.__algorithm = kwargs.get(self.__algorithm_label, 'auto')
        self.__leaf_size = kwargs.get(self.__leaf_size_label, 30)
        self.__metric = kwargs.get(self.__metric_label, 'minkowski')
        self.__p = kwargs.get(self.__p_label, 2)
        self.__metric_params = kwargs.get(self.__metric_params_label, None)
        self.__contamination = kwargs.get(self.__contamination_label, 'auto')
        self.__n_jobs = kwargs.get(self.__n_jobs_label, None)

    def scoring(self, X: pd.DataFrame) -> np.array:
        clf = LocalOutlierFactor(self.__n_neighbors,
                                 algorithm=self.__algorithm,
                                 leaf_size=self.__leaf_size,
                                 metric=self.__metric,
                                 p=self.__p,
                                 metric_params=self.__metric_params,
                                 contamination=self.__contamination,
                                 n_jobs=self.__n_jobs)
        clf.fit(X)
        scores = -clf.negative_outlier_factor_  # In LOF the higher the score the more normal the data point
        return scores

    # Getters
    @property
    def name(self) -> str:
        return self.__detector_name

    @property
    def params(self):
        return {
            self.__n_neighbors_label: self.__n_neighbors,
            self.__algorithm_label: self.__algorithm,
            self.__leaf_size_label: self.__leaf_size,
            self.__metric_label: self.__metric,
            self.__p_label: self.__p,
            self.__metric_params_label: self.__metric_params,
            self.__contamination_label: self.__contamination,
            self.__n_jobs_label: self.__n_jobs
        }

    @property
    def point(self) -> bool:
        return True
