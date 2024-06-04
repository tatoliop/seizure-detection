from math import floor

import numpy as np
import pandas as pd

from interfaces.feature_extraction_interface import Feature_extraction_interface
from models.record import Record


class Hjorth_activity_feature(Feature_extraction_interface):
    __feature_name = 'hjorth_activity'
    __sampling_label = 'sampling'

    def __init__(self, **kwargs):
        self.__sampling = kwargs.get(self.__sampling_label, 1)

    def transform(self, input_record: Record) -> Record:
        input_sample = input_record.sampling
        if input_sample < self.__sampling:
            raise ValueError("Hjorth activity sampling error")
        window = floor(input_sample / self.__sampling)
        input_length = input_record.data.shape[0]
        feature_length = input_length / window
        feature_list = input_record.dimensions
        features = pd.DataFrame(0.0, index=np.arange(feature_length), columns=feature_list)
        feature_index = 0
        for i in range(0, input_length, window):
            # Compute activity feature
            current_window = input_record.data.loc[i:i + window]
            current_features = current_window.var()
            features.loc[feature_index] = current_features
            feature_index += 1
        # Rename columns with feature name
        renamed_features = features
        # Create new record
        result_record = Record(input_record.record_id,
                               renamed_features.columns.values.tolist(),
                               renamed_features,
                               input_record.duration,
                               input_record.datetime,
                               self.__sampling,
                               self.__feature_name,
                               input_record.episode_meta)
        return result_record

    # Getters
    @property
    def name(self) -> str:
        return self.__feature_name

    @property
    def params(self):
        return {
            self.__sampling_label: self.__sampling
        }
