import numpy as np


def get_ensembles(scores: dict) -> dict:
    sum_scores = ensembleSumRule(scores)
    avg_scores = ensembleAvgRule(scores)
    return sum_scores | avg_scores


def ensembleSumRule(scores: dict) -> dict:
    keys = list(scores.keys())
    size = len(scores[keys[0]])
    res_scores = np.zeros(size)
    for i in range(0, size):
        tmpSum = 0
        for y in range(0, len(keys)):
            tmpSum = tmpSum + scores[keys[y]][i]
        res_scores[i] = tmpSum
    return {'sum_ensemble': res_scores}


def ensembleAvgRule(scores: dict) -> dict:
    keys = list(scores.keys())
    size = len(scores[keys[0]])
    res_scores = np.zeros(size)
    for i in range(0, size):
        tmpSum = 0
        tmpCount = 0
        for y in range(0, len(keys)):
            tmpSum = tmpSum + scores[keys[y]][i]
            tmpCount = tmpCount + 1
        res_scores[i] = tmpSum / tmpCount
    return {'avg_ensemble': res_scores}
