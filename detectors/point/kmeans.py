import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from interfaces.detector_interface import Detector_interface


class Kmeans(Detector_interface):
    __detector_name = 'kmeans'
    __n_clusters_label = 'n_clusters'

    def __init__(self, **kwargs):
        self.__n_clusters = kwargs.get(self.__n_clusters_label, 8)

    def scoring(self, X: pd.DataFrame) -> np.array:
        clf = KMeans(n_clusters=self.__n_clusters)
        clf.fit(X)
        clusters = clf.predict(X)
        scores = np.linalg.norm(X - clf.cluster_centers_[clusters], axis=1)
        return scores

    # Getters
    @property
    def name(self) -> str:
        return self.__detector_name

    @property
    def params(self):
        return {
            self.__n_clusters_label: self.__n_clusters,
        }

    @property
    def point(self) -> bool:
        return True
