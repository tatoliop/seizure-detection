import os

import numpy as np
import pandas as pd
from influxdb import InfluxDBClient

LABEL_ICTAL = 1
LABEL_NON_ICTAL = 0
INFLUXDB_HOST = os.environ['INFLUX_HOST'] if os.environ.get('INFLUX_HOST') is not None else 'localhost'
INFLUXDB_USER = os.environ['INFLUX_USER'] if os.environ.get('INFLUX_USER') is not None else 'user'
INFLUXDB_PASS = os.environ['INFLUX_PASS'] if os.environ.get('INFLUX_PASS') is not None else 'password'
FEATURE_NO = 21


def connectInflux():
    port = '8086'
    user = INFLUXDB_USER
    password = INFLUXDB_PASS  # getpass.getpass()
    dbName = 'eeg'
    tmpClient = InfluxDBClient(INFLUXDB_HOST, port, user, password, dbName)
    return tmpClient


def createInfluxQuery(cMeasurement, cPatient, cRecord):
    cQuery = 'SELECT * FROM ' + cMeasurement + ' WHERE patient = \'' + str(cPatient) + '\' and record = \'' + str(
        cRecord) + '\''
    return cQuery


def getData(cMeasurement, cPatient, cRecord):
    client = connectInflux()
    query = createInfluxQuery(cMeasurement, cPatient, cRecord)
    qResults = client.query(query)
    qResultPD = pd.DataFrame(qResults.get_points())
    # Split into data and label
    featureNames = qResultPD.columns[1: FEATURE_NO + 1].values
    X = qResultPD.iloc[:, 1: FEATURE_NO + 1].to_numpy()
    Y = qResultPD.iloc[:, FEATURE_NO + 1].apply(
        lambda x: LABEL_ICTAL if x == 'Ictal' else LABEL_NON_ICTAL).to_numpy()  # 1 for outlier 0 for inlier (for the TSB metrics)
    client.close()
    return X, Y, featureNames


def getSubsequence(X, size):
    result = np.ndarray(shape=(len(X) - size + 1, size))
    i = size
    while i <= len(X):
        index = i - size
        tmpRange = range(index, i)
        result[index] = np.transpose(X[tmpRange])
        i = i + 1
    return result


def getSubsequenceLabel(labels, size):
    result = np.arange(len(labels) - size + 1)
    i = size
    while i <= len(labels):
        index = i - size
        tmpRange = range(index, i)
        if LABEL_ICTAL in labels[tmpRange]:
            result[index] = LABEL_ICTAL
        else:
            result[index] = LABEL_NON_ICTAL
        i = i + 1
    return result
