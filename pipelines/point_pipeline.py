import time

import pandas as pd

from interfaces.pipeline_interface import Pipeline_interface
from params.point_pipeline_params import Point_pipeline_params
from models.record import Record
from utils.constants import EPISODE_LABEL, DETECTOR_TIME_LABEL
from utils.enums import Metrics_enum


class Point_pipeline(Pipeline_interface):

    __multivariate_label = 'multivariate'

    def __init__(self, params: Point_pipeline_params):
        super().__init__(params)
        self.__multivariate = params.multivariate
        self.__labels = None
        self.__scores = {}
        self.__times = {}

    def execute(self, input_data: Record):
        # Extract features
        features = self.get_features(input_data)
        self.__labels = features.label
        # Transform to uni or multi dims
        data_transformed = self.__transform_data(features)
        # Detect
        for dim in data_transformed:
            data_tmp = data_transformed[dim]
            time_start = time.time()
            score = self.detector.scoring(data_tmp)
            time_end = time.time()
            post_score = self.postprocess(score)
            self.__scores[dim] = post_score
            self.__times[dim] = time_end - time_start

    def __transform_data(self, record: Record) -> dict[str:pd.DataFrame]:
        # Initiate stuff
        dimensions = record.dimensions
        transformed_data = {}
        if self.__multivariate:
            transformed_data[self.__multivariate_label] = record.data
        else:
            for dimension in dimensions:
                transformed_data[dimension] = record.data.loc[:, [dimension]]
        return transformed_data

    def metrics(self, coeff) -> dict[str: dict]:
        if self.__labels is None or self.__scores is None:
            raise ValueError('Error on evaluation. No labels and scores are available.')
        ground_truth = self.__labels[EPISODE_LABEL]  # TODO do something with the seizure type as well
        res = {}
        for dim in self.__scores.keys():
            metrics = self.evaluator.metrics(Metrics_enum.POINT, self.__scores[dim], ground_truth, coeff)
            metrics[DETECTOR_TIME_LABEL] = self.__times[dim]
            res[dim] = metrics
        return res
