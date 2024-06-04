import numpy as np
import pandas as pd

from models.record_id import Record_id
from models.episode_meta import Episode_meta
from utils import constants


class Record:

    def __init__(self,
                 record_id: Record_id,
                 dimensions: list[str],
                 data: pd.DataFrame,
                 duration: float,
                 datetime: str,
                 sampling: int,
                 data_format: str,
                 episode_meta: Episode_meta
                 ):
        self.__record_id: Record_id = record_id
        self.__dimensions: list[str] = dimensions
        self.__dimensions_no: int = len(dimensions)
        self.__data: pd.DataFrame = data
        self.__duration: float = duration  # Seconds
        self.__datetime: str = datetime
        self.__sampling: int = sampling
        self.__data_format: str = data_format if data_format != '' else 'default'
        self.__episode_meta: Episode_meta = episode_meta
        self.__label: pd.DataFrame = self.__get_ground_truth_col()

    def __get_ground_truth_col(self) -> pd.DataFrame:
        data_len = self.__data.shape[0]
        truth_df = pd.DataFrame(constants.NORMAL_BINARY, index=np.arange(data_len), columns=[constants.EPISODE_LABEL])
        truth_df[constants.EPISODE_TYPE_LABEL] = constants.EPISODE_TYPE_DEFAULT_VALUE
        if self.__episode_meta is not None:
            for i in range(self.__episode_meta.count):
                start = self.__episode_meta.start_time[i] * self.__sampling
                end = self.__episode_meta.end_time[i] * self.__sampling - 1
                type_tmp = self.__episode_meta.episode_type[i]
                truth_df.loc[start:end, constants.EPISODE_LABEL] = constants.EPISODE_BINARY
                truth_df.loc[start:end, constants.EPISODE_TYPE_LABEL] = type_tmp
        return truth_df

    # Getters
    @property
    def record_id(self) -> Record_id:
        return self.__record_id

    @property
    def dimensions(self) -> list[str]:
        return self.__dimensions

    @property
    def dimensions_no(self) -> int:
        return self.__dimensions_no

    @property
    def data(self) -> pd.DataFrame:
        return self.__data

    @property
    def label(self) -> pd.DataFrame:
        return self.__label

    @property
    def duration(self) -> float:
        return self.__duration

    @property
    def datetime(self) -> str:
        return self.__datetime

    @property
    def sampling(self) -> int:
        return self.__sampling

    @property
    def data_format(self) -> str:
        return self.__data_format

    @property
    def episode_meta(self) -> Episode_meta:
        return self.__episode_meta

    @property
    def data_w_label(self) -> pd.DataFrame:
        return pd.concat([self.__data, self.__label], axis=1)

    def toDict(self) -> dict:
        record = self.__record_id.toDict()
        episode_meta = self.__episode_meta.toDict()
        current_dict = {
            'dimensions': self.__dimensions,
            'dimensions_no': self.__dimensions_no,
            'duration': self.__duration,
            'datetime': str(self.__datetime),
            'sampling': self.__sampling,
            'data_format': self.data_format,
        }
        record.update(current_dict)
        record.update(episode_meta)
        return record

    def __repr__(self):
        return (f"<Record: \n"
                f"record={self.__record_id}, \n"
                f"dimensions={self.__dimensions}, \n"
                f"dimensions_no={self.__dimensions_no}, \n"
                f"data={self.__data.head(2)}, \n"
                f"data_length={len(self.__data)}, \n"
                f"labels={self.__label.head(2)}, \n"
                f"label_length={len(self.__label)}, \n"
                f"duration={self.__duration}, \n"
                f"datetime={self.__datetime}, \n"
                f"sampling={self.__sampling}, \n"
                f"data_format={self.__data_format}, \n"
                f"episode_meta={self.__episode_meta}"
                f">")
