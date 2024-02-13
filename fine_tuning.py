### TESTING MANGO

from mango import Tuner, scheduler

import algorithms
from basic_metrics import basic_metricor
from main import getData, METRIC_ALPHA, METRIC_SCORE

# search space for KNN classifier's hyperparameters
# n_neighbors can vary between 1 and 50, with different choices of algorithm
param_space_lof = dict(n_neighbors=range(1, 50))


param_space_iforest = dict(n_estimators=range(50, 150))

param_space_xstream = dict(k=range(25, 75),
                           nchains=range(25,75),
                           depth=range(1,20))


@scheduler.serial
def objective_LOF(**params):
    #Get data
    # Get data
    X, Y, featureNames = getData('HjorthActivity', 1, 3)
    [score, elapsedTime] = algorithms.getModelPrediction('LOF', params, X)
    grader = basic_metricor(alpha=METRIC_ALPHA, metric_outlierness=METRIC_SCORE)
    [AUC_ROC, Pprecision, Precall, Pf, Rrecall, ExistenceReward, OverlapReward, Rprecision, RF,
     Precision_at_k] = grader.metric_new(Y, score)
    return Rrecall

@scheduler.serial
def objective_iForest(**params):
    #Get data
    # Get data
    X, Y, featureNames = getData('HjorthActivity', 1, 3)
    [score, elapsedTime] = algorithms.getModelPrediction('IForest', params, X)
    grader = basic_metricor(alpha=METRIC_ALPHA, metric_outlierness=METRIC_SCORE)
    [AUC_ROC, Pprecision, Precall, Pf, Rrecall, ExistenceReward, OverlapReward, Rprecision, RF,
     Precision_at_k] = grader.metric_new(Y, score)
    return Rrecall


@scheduler.serial
def objective_xStream(**params):
    #Get data
    # Get data
    X, Y, featureNames = getData('HjorthActivity', 1, 3)
    [score, elapsedTime] = algorithms.getModelPrediction('xStream', params, X)
    grader = basic_metricor(alpha=METRIC_ALPHA, metric_outlierness=METRIC_SCORE)
    [AUC_ROC, Pprecision, Precall, Pf, Rrecall, ExistenceReward, OverlapReward, Rprecision, RF,
     Precision_at_k] = grader.metric_new(Y, score)
    return Rrecall



#LOF
tuner = Tuner(param_space_lof, objective_LOF)
results = tuner.maximize()
print('best parameters:', results['best_params'])
print('best accuracy:', results['best_objective'])
# best parameters: {'n_neighbors': 40}
# best accuracy: 0.3292682926829268

#Iforest
tuner = Tuner(param_space_iforest, objective_iForest)
results = tuner.maximize()
print('best parameters:', results['best_params'])
print('best accuracy:', results['best_objective'])
# best parameters: {'n_estimators': 103}
# best accuracy: 0.5701219512195121


#xStream
tuner = Tuner(param_space_xstream, objective_xStream)
results = tuner.maximize()
print('best parameters:', results['best_params'])
print('best accuracy:', results['best_objective'])
# best parameters: {'depth': 1, 'k': 25, 'nchains': 73}
# best accuracy: 0.4695121951219512