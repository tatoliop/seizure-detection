import csv
import json
import sys
import os

import algorithms
from basic_metrics import basic_metricor
from preprocessing import getSubsequenceLabel, getSubsequence, FEATURE_NO, getData

# Import TSB and Xstream
sys.path.insert(0, '../TSB-UAD')
sys.path.insert(0, '../cmuxstream-core/python')

METRIC_ALPHA = float(os.environ["METRIC_ALPHA"]) if os.environ.get('METRIC_ALPHA') is not None else 0.25
METRIC_SCORE = float(os.environ["METRIC_SCORE"]) if os.environ.get('METRIC_SCORE') is not None else 3
EXPERIMENT_FILE = os.environ["EXP_FILE"] if os.environ.get('EXP_FILE') is not None else 'experiments.json'
MEASUREMENT_FILE = os.environ["MEASUREMENT_FILE"] if os.environ.get(
    'MEASUREMENT_FILE') is not None else 'measurements.json'
RESULTS_FILE = os.environ["RESULT_FILE"] if os.environ.get('RESULT_FILE') is not None else 'results.csv'
DEBUG = False


def fixLength(cX, cY):
    minLen = min(len(cX), len(cY))
    cX = cX[0:minLen]
    cY = cY[0:minLen]
    return cX, cY


def toDict(cPatientNo, cRecordNo, cModelName, cParameter, cSource, cFeatureName, cSequenceSize, cElapsedTime, cRrecall,
           cExistenceReward,
           cOverlapReward, cRprecision, cRf, cPrecall, cPprecision, cPf, cAuc):
    cRes = {
        'Patient': cPatientNo,
        'Record': cRecordNo,
        'Model': cModelName,
        'Parameters': cParameter,
        'Source': cSource,
        'Feature': cFeatureName,
        'SubSequence size': cSequenceSize,
        'Range alpha': METRIC_ALPHA,
        'Score2Binary': METRIC_SCORE,
        'Prediction elapsed time': cElapsedTime,
        'Range recall': cRrecall,
        'Existence reward': cExistenceReward,
        'Overlap reward': cOverlapReward,
        'Range precision': cRprecision,
        'Range F-score': cRf,
        'AUC score': cAuc,
        'Point recall': cPrecall,
        'Point precision': cPprecision,
        'Point F-score': cPf
    }
    return cRes


def writeResults(csvFile, returnResults):
    if csvFile is None:
        print(json.dumps(returnResults, indent=2, default=str))
    else:
        file_exists = os.path.isfile(RESULTS_FILE)
        with open(RESULTS_FILE, 'a', newline='') as output_file:
            keys = returnResults.keys()
            dict_writer = csv.DictWriter(output_file, keys)
            if not file_exists:
                dict_writer.writeheader()
            dict_writer.writerow(returnResults)


seizures = [
    (1, 3),
    (1, 4),
    (1, 15),
    (1, 16),
    (1, 18),
    (1, 21),
    (1, 26),
    (2, 161),
    (2, 162),
    (2, 19),
    (3, 1),
    (3, 2),
    (3, 3),
    (3, 4),
    (3, 34),
    (3, 35),
    (3, 36),
    (4, 5),
    (4, 8),
    (4, 28),
    (5, 6),
    (5, 13),
    (5, 16),
    (5, 17),
    (5, 22),
    (6, 1),
    (6, 4),
    (6, 9),
    (6, 10),
    (6, 13),
    (6, 18),
    (6, 24),
    (7, 12),
    (7, 13),
    (7, 19),
    (8, 2),
    (8, 5),
    (8, 11),
    (8, 13),
    (8, 21),
    (9, 6),
    (9, 8),
    (9, 19),
    (10, 12),
    (10, 20),
    (10, 27),
    (10, 30),
    (10, 31),
    (10, 38),
    (10, 89),
    (11, 82),
    (11, 92),
    (11, 99),
    (12, 6),
    (12, 8),
    (12, 9),
    (12, 10),
    (12, 11),
    (12, 23),
    (12, 27),
    (12, 28),
    (12, 29),
    (12, 33),
    (12, 36),
    (12, 38),
    (12, 42),
    (13, 19),
    (13, 21),
    (13, 40),
    (13, 55),
    (13, 58),
    (13, 59),
    (13, 60),
    (13, 62),
    (14, 3),
    (14, 4),
    (14, 6),
    (14, 11),
    (14, 17),
    (14, 18),
    (14, 27),
    (15, 6),
    (15, 10),
    (15, 15),
    (15, 17),
    (15, 20),
    (15, 22),
    (15, 28),
    (15, 31),
    (15, 40),
    (15, 46),
    (15, 49),
    (15, 52),
    (15, 54),
    (15, 62),
    (16, 10),
    (16, 11),
    (16, 14),
    (16, 16),
    (16, 17),
    (16, 18),
    (17, 3),
    (17, 4),
    (17, 63),
    (18, 29),
    (18, 30),
    (18, 31),
    (18, 32),
    (18, 35),
    (18, 36),
    (19, 28),
    (19, 29),
    (19, 30),
    (20, 12),
    (20, 13),
    (20, 14),
    (20, 15),
    (20, 16),
    (20, 68),
    (21, 19),
    (21, 20),
    (21, 21),
    (21, 22),
    (22, 20),
    (22, 25),
    (22, 38),
    (23, 6),
    (23, 8),
    (23, 9),
    (24, 1),
    (24, 3),
    (24, 4),
    (24, 6),
    (24, 7),
    (24, 9),
    (24, 11),
    (24, 13),
    (24, 14),
    (24, 15),
    (24, 17),
    (24, 21),
]

seizuresTest = [
    (1, 3),
    # (9, 19),
    # (23, 8),
]

if __name__ == '__main__':
    # Read exp file
    with open(EXPERIMENT_FILE) as exp_file:
        exp_contents = exp_file.read()
    experiment_dict = json.loads(exp_contents)
    # Read measurement file
    with open(MEASUREMENT_FILE) as meas_file:
        meas_contents = meas_file.read()
    measurement_dict = json.loads(meas_contents)
    inputData = seizuresTest if DEBUG else seizures
    total_experiments = len(inputData) * len(measurement_dict['measurements']) * len(experiment_dict['experiments'])
    count_experiments = 0
    for patientNo, recordNo in inputData:
        for measurementName in measurement_dict['measurements']:
            measurement = measurementName['measurement']
            # Get data
            try:
                X, Y, featureNames = getData(measurement, patientNo, recordNo)
            except IndexError:
                print("Exception in patient: " + str(patientNo) + " and record: " + str(recordNo))
                continue
            except:
                print("Exception in patient: " + str(patientNo) + " and record: " + str(recordNo))
                continue
            for experiment in experiment_dict['experiments']:
                count_experiments += 1
                print('Experiment: ', count_experiments, '/', total_experiments)
                # Get metadata
                modelName = experiment['modelName']
                parameters = experiment['parameters']
                univariate = experiment['univariate']
                sequenceSize = experiment['sequenceSize']
                for parameter in parameters:
                    # Get ground truth
                    if sequenceSize > 1:
                        tmpY = getSubsequenceLabel(Y, sequenceSize)
                    elif modelName == 'MatrixProfile':
                        tmpY = getSubsequenceLabel(Y, parameter['window'])
                    elif modelName == 'NormA':
                        tmpY = getSubsequenceLabel(Y, parameter['pattern_length'])
                    elif modelName == 'Series2Graph':
                        tmpY = getSubsequenceLabel(Y, parameter['query_length'])
                    elif modelName == 'Stumpy':
                        tmpY = getSubsequenceLabel(Y, parameter['m'])
                    else:
                        tmpY = Y
                    grader = basic_metricor(alpha=METRIC_ALPHA, metric_outlierness=METRIC_SCORE)
                    if univariate == 'True':
                        predictions = []
                        for i in range(0, FEATURE_NO):
                            tmpX = X[:, i].reshape(-1, 1)  # Reshape for univariate
                            # Extract custom subsequences
                            if sequenceSize > 1:
                                tmpX = getSubsequence(tmpX, sequenceSize)
                            # Get predictions
                            [score, elapsedTime] = algorithms.getModelPrediction(modelName, parameter, tmpX)
                            # Store univariate predictions for ensembles
                            predictions.append(score)
                            # Get metrics
                            tmpY, score = fixLength(tmpY, score)
                            [AUC_ROC, Pprecision, Precall, Pf, Rrecall, ExistenceReward, OverlapReward, Rprecision, RF,
                             Precision_at_k] = grader.metric_new(tmpY, score)
                            # Create dictionary
                            dictRes = toDict(patientNo, recordNo, modelName, parameter, measurement, featureNames[i],
                                             sequenceSize,
                                             elapsedTime, Rrecall, ExistenceReward, OverlapReward, Rprecision, RF,
                                             Precall, Pprecision, Pf, AUC_ROC)
                            if DEBUG:
                                writeResults(None, dictRes)
                            else:
                                writeResults(RESULTS_FILE, dictRes)
                        # Get mean assemble score
                        ensemble = algorithms.ensembleMeanRule(predictions)
                        tmpY, ensemble = fixLength(tmpY, ensemble)
                        [AUC_ROC, Pprecision, Precall, Pf, Rrecall, ExistenceReward, OverlapReward, Rprecision, RF,
                         Precision_at_k] = grader.metric_new(tmpY, ensemble)
                        dictRes = toDict(patientNo, recordNo, modelName, parameter, measurement, 'Mean assemble',
                                         sequenceSize,
                                         'N/A', Rrecall, ExistenceReward, OverlapReward, Rprecision, RF,
                                         Precall, Pprecision, Pf, AUC_ROC)
                        if DEBUG:
                            writeResults(None, dictRes)
                        else:
                            writeResults(RESULTS_FILE, dictRes)
                        # Get Sum assemble score
                        ensemble = algorithms.ensembleSumRule(predictions)
                        tmpY, ensemble = fixLength(tmpY, ensemble)
                        [AUC_ROC, Pprecision, Precall, Pf, Rrecall, ExistenceReward, OverlapReward, Rprecision, RF,
                         Precision_at_k] = grader.metric_new(tmpY, ensemble)
                        dictRes = toDict(patientNo, recordNo, modelName, parameter, measurement, 'Sum assemble',
                                         sequenceSize,
                                         'N/A', Rrecall, ExistenceReward, OverlapReward, Rprecision, RF,
                                         Precall, Pprecision, Pf, AUC_ROC)
                        if DEBUG:
                            writeResults(None, dictRes)
                        else:
                            writeResults(RESULTS_FILE, dictRes)
                    else:
                        # Get predictions
                        [score, elapsedTime] = algorithms.getModelPrediction(modelName, parameter, X)
                        # Get metrics
                        tmpY, score = fixLength(tmpY, score)
                        [AUC_ROC, Pprecision, Precall, Pf, Rrecall, ExistenceReward, OverlapReward, Rprecision, RF,
                         Precision_at_k] = grader.metric_new(tmpY, score)
                        # Create dictionary
                        dictRes = toDict(patientNo, recordNo, modelName, parameter, measurement, 'Multivariate',
                                         sequenceSize, elapsedTime,
                                         Rrecall, ExistenceReward, OverlapReward, Rprecision, RF, Precall, Pprecision,
                                         Pf, AUC_ROC)
                        if DEBUG:
                            writeResults(None, dictRes)
                        else:
                            writeResults(RESULTS_FILE, dictRes)
