import csv
import os
from datetime import datetime
from pathlib import Path


from models.record import Record
from utils.enums import Write_format_enum
from utils.my_influxdb import My_influxdb


class WriteData:

    def __init__(self):
        self.__file_path = Path(os.environ["SAVE_FILE_PATH"]) if os.environ.get(
            'SAVE_FILE_PATH') is not None else Path('./data')

    def write_data(self, record_data: Record, output: Write_format_enum, **kwargs):
        if output == Write_format_enum.INFLUX:
            # Get db measurement
            measurement = kwargs.get('measurement', record_data.data_format)
            # Write data
            self.__write_to_influx(record_data, measurement)
        elif output == Write_format_enum.CSV:
            # Get filenames
            filename = f'{record_data.record_id.dataset}_{record_data.record_id.subject}_{record_data.record_id.record}'
            datafile = self.__file_path / f'{filename}_data.{output.value}'
            metafile = self.__file_path / f'{filename}_meta.{output.value}'
            # Write data and meta
            self.__write_to_csv(record_data, datafile, metafile)

    @staticmethod
    def __write_to_csv(record: Record, datafile, metafile):
        record.data_w_label.to_csv(datafile)
        metadata = record.toDict()
        with open(metafile, 'w') as f:  # You will need 'wb' mode in Python 2.x
            w = csv.DictWriter(f, metadata.keys())
            w.writeheader()
            w.writerow(metadata)

    def __write_to_influx(self, record_data: Record, measurement: str):
        my_influxdb = My_influxdb()
        start_time = datetime.now()
        # Get tags from meta
        tags = self.__create_influx_tags(record_data, measurement)
        # Timestep for each data point's timestamp
        timestep = 1 / record_data.sampling
        # Start from 0 unix (1970-01-01 00:00:00)
        for i in range(0, len(record_data.data)):
            time = datetime.utcfromtimestamp(i * timestep)
            tags['time'] = time
            data_row = record_data.data.iloc[[i]].to_dict('index')[i]
            label_row = record_data.label.iloc[[i]].to_dict('index')[i]
            tags['tags'].update(label_row)
            tags['fields'] = data_row
            final_output = [tags]
            # Write each row
            my_influxdb.write_point(final_output)
        end_time = datetime.now()
        print(
            f'Completed write for subject {record_data.record_id.subject} and record {record_data.record_id.record}'
            f' in {end_time - start_time}')

    @staticmethod
    def __create_influx_tags(record_data: Record, measurement: str) -> dict:
        return {
            'measurement': measurement,
            'tags': record_data.toDict()
        }
