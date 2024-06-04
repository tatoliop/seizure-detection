import numpy as np
import itertools as it

from utils.constants import EVAL_COEFF_DEFAULT, EVAL_ALPHA_DEFAULT, EVAL_COEFF_LABEL, EVAL_ALPHA_LABEL


class Evaluation_set_iterator:
    def __init__(self, data):
        self.data = data
        self._pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = self.data[self._pos]
            res = {EVAL_COEFF_LABEL: item[0], EVAL_ALPHA_LABEL: item[1]}
        except IndexError:
            raise StopIteration
        self._pos += 1
        return res

class Evaluation_single_iterator:
    def __init__(self, data, label):
        self.data = data
        self._pos = 0
        self.label = label

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = self.data[self._pos]
            res = {self.label: item}
        except IndexError:
            raise StopIteration
        self._pos += 1
        return res

class Evaluation_set:

    def __init__(self,
                 coeff=None,
                 alpha=None
                 ):
        if coeff is None:
            coeff = [EVAL_COEFF_DEFAULT]
        if alpha is None:
            alpha = [EVAL_ALPHA_DEFAULT]
        self.__coeff = np.array(coeff)
        self.__alpha = np.array(alpha)

    # Getters
    @property
    def coeff(self):
        return Evaluation_single_iterator(self.__coeff, EVAL_COEFF_LABEL)

    @property
    def alpha(self):
        return Evaluation_single_iterator(self.__alpha, EVAL_ALPHA_LABEL)

    @property
    def cartesian(self):
        return Evaluation_set_iterator(np.array(list(it.product(self.__coeff, self.__alpha))))

