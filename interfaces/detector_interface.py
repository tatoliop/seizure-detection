from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class Detector_interface(ABC):

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def scoring(self, input_data: pd.DataFrame) -> np.array:
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def params(self) -> dict:
        pass

    @abstractmethod
    def point(self) -> bool:
        pass

