import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from interfaces.detector_interface import Detector_interface


class Knn(Detector_interface):
    __detector_name = 'knn'
    __n_neighbors_label = 'n_neighbors'
    __distance_method_label = 'distance_method'

    def __init__(self, **kwargs):
        self.__n_neighbors = kwargs.get(self.__n_neighbors_label, 5)
        self.__distance_method = kwargs.get(self.__distance_method_label, 'largest')

    def scoring(self, X: pd.DataFrame) -> np.array:
        clf = NearestNeighbors()
        clf.fit(X)
        dist_arr, _ = clf.kneighbors(n_neighbors=self.__n_neighbors)
        dist = self._get_dist_by_method(dist_arr)
        scores = dist.ravel()
        return scores

    def _get_dist_by_method(self, dist_arr):
        """Internal function to decide how to process passed in distance array

        Parameters
        ----------
        dist_arr : numpy array of shape (n_samples, n_neighbors)
            Distance matrix.

        Returns
        -------
        dist : numpy array of shape (n_samples,)
            The outlier scores by distance.
        """

        if self.__distance_method == 'largest':
            return dist_arr[:, -1]
        elif self.__distance_method == 'mean':
            return np.mean(dist_arr, axis=1)
        elif self.__distance_method == 'median':
            return np.median(dist_arr, axis=1)
        else:
            return dist_arr[:, -1]

    # Getters
    @property
    def name(self) -> str:
        return self.__detector_name

    @property
    def params(self):
        return {
            self.__n_neighbors_label: self.__n_neighbors,
        }

    @property
    def point(self) -> bool:
        return True
