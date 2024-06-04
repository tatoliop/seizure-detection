import time

import numpy as np
import pandas as pd

from ensemble.ensembles import get_ensembles
from interfaces.pipeline_interface import Pipeline_interface
from params.range_pipeline_params import Range_pipeline_params
from models.record import Record
from utils import constants
from utils.constants import EPISODE_LABEL, DETECTOR_TIME_LABEL
from utils.enums import Metrics_enum


class Range_pipeline(Pipeline_interface):

    def __init__(self,
                 params: Range_pipeline_params):
        super().__init__(params)
        self.__subsequence_size = params.subsequence_size
        self.__slide_size = params.slide_size
        self.__labeling_threshold = params.labeling_threshold
        self.__labels = None
        self.__scores = {}
        self.__times = {}

    def execute(self, input_data: Record):
        # Extract features
        features = self.get_features(input_data)
        # Split each dimension and create subsequences if necessary
        data_transformed = self.__transform_data_for_point_detector(features) if self.detector.point \
            else self.__transform_data_for_range_detector(features)
        # Transform labels
        labels_transformed = self.__transform_labels(features)
        self.__labels = labels_transformed
        # Detect
        for dim in data_transformed:
            data_tmp = data_transformed[dim]
            time_start = time.time()
            score = self.detector.scoring(data_tmp)
            time_end = time.time()
            post_score = self.postprocess(score)
            # fix score length (in some algos the results are different from the labels)
            fixed_score = self.fixLength(post_score, labels_transformed)
            self.__scores[dim] = fixed_score
            self.__times[dim] = time_end - time_start
        # TODO currently ensembles are hardcoded. need to be optional
        ensembles = get_ensembles(self.__scores)
        self.__scores.update(ensembles)


    def metrics(self, coeff, alpha) -> dict[str: dict]:
        if self.__labels is None or self.__scores is None:
            raise ValueError('Error on evaluation. No labels and scores are available.')
        ground_truth = self.__labels[EPISODE_LABEL]  # TODO do something with the seizure type as well
        res = {}
        for dim in self.__scores.keys():
            metrics = self.evaluator.metrics(Metrics_enum.ALL, self.__scores[dim], ground_truth, coeff, alpha)
            metrics[DETECTOR_TIME_LABEL] = self.__times.get(dim, 0)
            res[dim] = metrics
        return res

    def __transform_labels(self, record: Record) -> pd.DataFrame:
        label_len = record.label.shape[0] - self.__subsequence_size + 1
        # Initialize dataframe
        label_df = pd.DataFrame(constants.NORMAL_BINARY, index=np.arange(label_len), columns=[constants.EPISODE_LABEL])
        label_df[constants.EPISODE_TYPE_LABEL] = constants.EPISODE_TYPE_DEFAULT_VALUE
        # Decide on labels for subsequences
        for i in range(0, label_len, self.__slide_size):
            label_tmp = record.label.loc[i:i + self.__subsequence_size - 1]
            # Get the counts and compare to threshold to decide whether to label a subsequence as anomalous or normal
            counts_binary = label_tmp[constants.EPISODE_LABEL].value_counts()
            if constants.EPISODE_BINARY in counts_binary.keys():
                episode_count = counts_binary[constants.EPISODE_BINARY]
                if (episode_count / self.__subsequence_size) >= self.__labeling_threshold:
                    # Get the types and remove the default value of normal labels
                    counts_type = label_tmp[constants.EPISODE_TYPE_LABEL].value_counts()
                    if constants.EPISODE_TYPE_DEFAULT_VALUE in counts_type.keys():
                        counts_type = counts_type.drop(constants.EPISODE_TYPE_DEFAULT_VALUE)
                    type_tmp = counts_type.idxmax()
                    label_df.loc[i] = [constants.EPISODE_BINARY, type_tmp]
        return label_df

    def __transform_data_for_point_detector(self, record: Record) -> dict[str:pd.DataFrame]:
        # Initiate stuff
        dimensions = record.dimensions
        data_len = record.data.shape[0] - self.__subsequence_size + 1
        cols = range(1, self.__subsequence_size + 1)
        preprocessed_data = {}
        # Initialize dataframes for data
        for dimension in dimensions:
            data_tmp = pd.DataFrame(0.0, index=np.arange(data_len), columns=cols)
            preprocessed_data[dimension] = data_tmp
        # Create subsequences
        for i in range(0, data_len, self.__slide_size):
            data_tmp: pd.DataFrame = record.data.loc[i:i + self.__subsequence_size - 1]
            for dimension in dimensions:
                preprocessed_data[dimension].loc[i] = data_tmp.get(dimension).to_list()
        return preprocessed_data

    def __transform_data_for_range_detector(self, record: Record) -> dict[str:pd.DataFrame]:
        # Initiate stuff
        dimensions = record.dimensions
        transformed_data = {}
        for dimension in dimensions:
            transformed_data[dimension] = record.data.loc[:, dimension]
        return transformed_data

    @staticmethod
    def fixLength(score, label):
        score_len = len(score)
        label_len = len(label)
        if score_len > label_len:
            return score[:label_len]
        elif label_len > score_len:
            return list(score) + [score[-1]] * (label_len - score_len)
        else:
            return score
