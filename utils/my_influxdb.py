import os

from influxdb import InfluxDBClient


class My_influxdb:

    def __init__(self):
        self.__influxdb_host = os.environ['INFLUXDB_HOST'] \
            if os.environ.get('INFLUXDB_HOST') is not None else 'localhost'
        self.__influxdb_port = os.environ['INFLUXDB_PORT'] \
            if os.environ.get('INFLUXDB_PORT') is not None else '8086'
        self.__influxdb_user = os.environ['INFLUXDB_ADMIN_USER'] \
            if os.environ.get('INFLUXDB_ADMIN_USER') is not None else 'user'
        self.__influxdb_pass = os.environ['INFLUXDB_ADMIN_PASSWORD'] \
            if os.environ.get('INFLUXDB_ADMIN_PASSWORD') is not None else 'password'
        self.__influxdb_db = os.environ['INFLUXDB_DB'] \
            if os.environ.get('INFLUXDB_DB') is not None else 'eeg'

    def write_point(self, point):
        client = self.__connect_influx()
        client.write_points(point)

    def read_tags(self, measurement):
        pass

    def __connect_influx(self):
        tmpClient = InfluxDBClient(self.__influxdb_host, self.__influxdb_port, self.__influxdb_user,
                                   self.__influxdb_pass, self.__influxdb_db)
        return tmpClient
