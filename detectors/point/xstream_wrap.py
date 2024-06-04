import pandas as pd

from detectors.sources.xstream.Chains import Chains
from interfaces.detector_interface import Detector_interface


class Xstream(Detector_interface):
    __detector_name = 'xstream'
    __k_label = 'k'
    __nchains_label = 'nchains'
    __depth_label = 'depth'

    def __init__(self, **kwargs):
        self.__k = kwargs.get(self.__k_label, 50)
        self.__nchains = kwargs.get(self.__nchains_label, 50)
        self.__depth = kwargs.get(self.__depth_label, 10)

    def scoring(self, X: pd.DataFrame) -> list[float]:
        clf = Chains(k=self.__k, nchains=self.__nchains, depth=self.__depth)
        clf.fit(X)
        score = -clf.score(X)  # Bigger score inliers / lower score outliers SO REVERT IT
        return score

    # Getters
    @property
    def name(self) -> str:
        return self.__detector_name

    @property
    def params(self):
        return {
            self.__k_label: self.__k,
            self.__nchains_label: self.__nchains,
            self.__depth_label: self.__depth
        }

    @property
    def point(self) -> bool:
        return True
