from abc import ABC, abstractmethod

import numpy as np


class Postprocessing_interface(ABC):

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def transform(self, scores: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def params(self) -> dict:
        pass
