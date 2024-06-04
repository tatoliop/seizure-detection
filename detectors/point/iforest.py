import numpy as np
import pandas as pd

from interfaces.detector_interface import Detector_interface
from sklearn.ensemble import IsolationForest


class Iforest(Detector_interface):
    __detector_name = 'isolation_forest'
    __n_estimators_label = 'n_estimators'
    __max_samples_label = 'max_samples'
    __contamination_label = 'contamination'
    __max_features_label = 'max_features'
    __bootstrap_label = 'bootstrap'
    __n_jobs_label = 'n_jobs'
    __random_state_label = 'random_state'
    __verbose_label = 'verbose'
    __warm_start_label = 'warm_start'

    def __init__(self, **kwargs):
        self.__n_estimators = kwargs.get(self.__n_estimators_label, 100)
        self.__max_samples = kwargs.get(self.__max_samples_label, 'auto')
        self.__contamination = kwargs.get(self.__contamination_label, 'auto')
        self.__max_features = kwargs.get(self.__max_features_label, 1.0)
        self.__bootstrap = kwargs.get(self.__bootstrap_label, False)
        self.__n_jobs = kwargs.get(self.__n_jobs_label, None)
        self.__random_state = kwargs.get(self.__random_state_label, None)
        self.__verbose = kwargs.get(self.__verbose_label, 0)
        self.__warm_start = kwargs.get(self.__warm_start_label, False)

    def scoring(self, X: pd.DataFrame) -> np.array:
        clf = IsolationForest(n_estimators=self.__n_estimators,
                              max_samples=self.__max_samples,
                              contamination=self.__contamination,
                              max_features=self.__max_features,
                              bootstrap=self.__bootstrap,
                              n_jobs=self.__n_jobs,
                              random_state=self.__random_state,
                              verbose=self.__verbose,
                              warm_start=self.__warm_start)
        clf.fit(X)
        scores = -clf.score_samples(X)  # In Iforest the higher the score the more normal the data point
        return scores

    # Getters
    @property
    def name(self) -> str:
        return self.__detector_name

    @property
    def params(self):
        return {
            self.__n_estimators_label: self.__n_estimators,
            self.__max_samples_label: self.__max_samples,
            self.__contamination_label: self.__contamination,
            self.__max_features_label: self.__max_features,
            self.__bootstrap_label: self.__bootstrap,
            self.__n_jobs_label: self.__n_jobs,
            self.__random_state_label: self.__random_state,
            self.__verbose_label: self.__verbose,
            self.__warm_start_label: self.__warm_start
        }

    @property
    def point(self) -> bool:
        return True
