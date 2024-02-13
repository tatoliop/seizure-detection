import numpy as np
import stumpy
import time

from sklearn.preprocessing import MinMaxScaler


def ensembleSumRule(predictions):
    size = len(predictions[0])
    resPrediction = np.zeros(size)
    for i in range(0, size):
        tmpSum = 0
        for y in range(0, len(predictions)):
            tmpSum = tmpSum + predictions[y][i]
        resPrediction[i] = tmpSum
    return resPrediction


def ensembleMeanRule(predictions):
    size = len(predictions[0])
    resPrediction = np.zeros(size)
    for i in range(0, size):
        tmpSum = 0
        tmpCount = 0
        for y in range(0, len(predictions)):
            tmpSum = tmpSum + predictions[y][i]
            tmpCount = tmpCount + 1
        resPrediction[i] = tmpSum / tmpCount
    return resPrediction


def getModelPrediction(model, parameters, X):
    score = None
    start = time.time()
    if model == 'IForest':
        from TSB_UAD.models.iforest import IForest
        clf = IForest(**parameters)
        clf.fit(X)
        score = clf.decision_scores_
    elif model == 'LOF':
        from TSB_UAD.models.lof import LOF
        clf = LOF(**parameters)
        clf.fit(X)
        score = clf.decision_scores_
    elif model == 'xStream':
        from Chains import Chains
        clf = Chains(**parameters)
        clf.fit(X)
        score = -clf.score(X)  # Bigger score inliers / lower score outliers SO REVERT IT
    elif model == 'NormA':
        from TSB_UAD.models.norma import NORMA
        clf = NORMA(**parameters)
        newX = X.reshape(-1)
        clf.fit(newX)
        score = clf.decision_scores_
    elif model == 'Series2Graph':
        from TSB_UAD.models.series2graph import Series2Graph
        s2g = Series2Graph(parameters['pattern_length'])
        s2g.fit(X)
        s2g.score(query_length=parameters['query_length'], dataset=X)
        score = s2g.decision_scores_
    elif model == 'MatrixProfile':  # MPX algorithm
        from TSB_UAD.models.matrix_profile import MatrixProfile
        clf = MatrixProfile(**parameters)
        newX = X.reshape(-1)
        clf.fit(newX)
        score = clf.decision_scores_
    elif model == 'Stumpy':
        newX = X.reshape(-1)
        mp = stumpy.stump(newX, **parameters)  # Scores are distance to the closer neighbor subsequence so bigger
        score = mp[:, 0]
    score = MinMaxScaler(feature_range=(0, 1)).fit_transform(score.reshape(-1, 1)).ravel()
    end = time.time()
    return [score, end - start]

    # def __MStump(self, X, parameters):
    #     mps, indices = stumpy.mstump(np.transpose(X),
    #                                  **parameters)  # Cols should be the time axis and rows the dimensions (thats why transpose is needed)
    #     motifs_idx = np.argsort(mps, axis=1)[:, :2]
    #     print(motifs_idx)
    #
    #     print(mps)
    #     print(len(mps))
    #     print(len(mps[0]))
