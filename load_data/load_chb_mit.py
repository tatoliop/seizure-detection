"""
Script to read EDF data
"""
from pathlib import Path
import re

import pandas as pd
import pyedflib

from interfaces.load_data_interface import Load_data_interface
from models.record import Record
from models.record_id import Record_id
from models.episode_meta import Episode_meta


class Load_CHB_MIT(Load_data_interface):
    """
    :param kwargs: { path: path to unzipped root directory of CHB MIT dataset }
    """
    # Constants
    __SEIZURE_META_TAIL = '-summary.txt'
    __SEIZURE_RECORDS = 'RECORDS-WITH-SEIZURES'
    __RECORDS = 'RECORDS'
    __SEIZURE_TYPE = 'sz'
    __CHANNEL_FILTER = ['FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', 'FP1-F3', 'F3-C3', 'C3-P3', 'P3-O1', 'FP2-F4', 'F4-C4',
                        'C4-P4', 'P4-O2', 'FP2-F8', 'F8-T8', 'T8-P8', 'P8-O2', 'FZ-CZ', 'CZ-PZ', 'T7-FT9', 'FT9-FT10',
                        'FT10-T8']
    __FILTER_LEN = len(__CHANNEL_FILTER)
    __DATASET_NAME = 'CHB-MIT'
    __DATA_FORMAT = 'raw'
    __FILTER_DATA_FORMAT = 'filtered_raw'

    def __init__(self, **kwargs):
        self.__path = Path(kwargs.get('path', '.'))
        self.__sampling = 256
        # Load records
        self.__records = self.__load_records()

    def load_data(self, record_id, filter_channels: bool = True) -> Record:
        # First load the seizure meta (if they exist)
        seizure_meta = self.__load_seizure_meta(record_id)
        # Then load the data and append the seizure meta
        data_tmp = self.__load_channel_data(record_id, seizure_meta)
        if filter_channels is True:
            new_data = self.__filter_channels(data_tmp)
            return new_data
        return data_tmp

    def records(self) -> list[Record_id]:
        return self.__records

    def __load_records(self) -> list:
        record_file = self.__path / self.__RECORDS
        seizure_file = self.__path / self.__SEIZURE_RECORDS
        result = []
        with open(record_file) as f:
            records = f.read().splitlines()
        with open(seizure_file) as f:
            seizures = f.read().splitlines()
        for i in records:
            [subject_tmp, record_tmp] = self.__parse_record_filename(i)
            has_episode = True if i in seizures else False
            my_record = Record_id(subject_tmp, record_tmp, i, self.__DATASET_NAME, has_episode)
            result.append(my_record)
        return result

    def __load_seizure_meta(self, record_id: Record_id):
        # Split the filename and get patient folder and only the filename
        [folder, filename] = self.__parse_filename(record_id.filename)
        # # Get info path
        my_path = self.__path / folder / (folder + self.__SEIZURE_META_TAIL)
        # Read info file
        with my_path.open('r') as f:
            line = f.readline()
            while line:
                if filename in line:
                    # Skip the next 2 lines (start and end time of record) and get the 3rd one (unless subject is 24)
                    if record_id.subject != '24':
                        for i in range(0, 2):
                            f.readline()
                    line = f.readline()
                    seizure_no = self.__parse_seizure_info_no(line)
                    # For each seizure get start and end times
                    if seizure_no > 0:
                        seizure_start = []
                        seizure_end = []
                        seizure_type = []
                        for i in range(0, seizure_no):
                            # Get start time
                            line = f.readline()
                            seizure_start.append(self.__parse_seizure_info_timestamp(line))
                            # Get end time
                            line = f.readline()
                            seizure_end.append(self.__parse_seizure_info_timestamp(line))
                            # Seizure type is not known for CHB-MIT dataset
                            seizure_type.append(self.__SEIZURE_TYPE)
                        # Create seizure meta objects
                        return Episode_meta(seizure_no, seizure_start, seizure_end, seizure_type)
                    break
                else:
                    line = f.readline()
        return None

    def __load_channel_data(self, record_id: Record_id, seizure_meta: Episode_meta):
        # Get file path
        my_path = self.__path / record_id.filename
        with pyedflib.EdfReader(str(my_path)) as f:
            dateTime = f.getStartdatetime()
            duration = f.getFileDuration()
            channels = f.getSignalLabels()
            channels_no = len(channels)
            data_df = pd.DataFrame()
            for i in range(channels_no):
                data_tmp = f.readSignal(i)
                data_df[channels[i]] = data_tmp
            # Create data object
            my_data = Record(record_id, channels, data_df,
                             duration, dateTime, self.__sampling, self.__DATA_FORMAT, seizure_meta)
        return my_data

    def __filter_channels(self, record_data: Record) -> Record | None:
        result_channels = [x for x in self.__CHANNEL_FILTER if x in record_data.dimensions]
        result_channels_no = len(result_channels)
        if result_channels_no != self.__FILTER_LEN:
            return None
        result_data = record_data.data.loc[:, record_data.data.columns.isin(result_channels)]
        new_record_data = Record(record_data.record_id, result_channels, result_data,
                                 record_data.duration, record_data.datetime, record_data.sampling,
                                 self.__FILTER_DATA_FORMAT, record_data.episode_meta)
        return new_record_data

    @staticmethod
    def __parse_filename(filename):
        return filename.split('/')

    @staticmethod
    def __parse_record_filename(name):
        subject = None
        record = None
        m = re.search('chb(.+?)/', name)
        if m:
            subject = m.group(1)
        m = re.search('_(.+?).edf', name)
        if m:
            record = m.group(1)
        return [subject, record]

    @staticmethod
    def __parse_seizure_info_no(line):
        m = re.search('Number of Seizures in File: (.+?)', line)
        if m:
            found = int(m.group(1))
            return found

    @staticmethod
    def __parse_seizure_info_timestamp(line):
        m = re.search('Time: (.+?) seconds', line)
        if m:
            found = int(m.group(1))
            return found
