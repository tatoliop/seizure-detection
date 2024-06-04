import enum

from detectors.point.iforest import Iforest
from detectors.point.kmeans import Kmeans
from detectors.point.knn import Knn
from detectors.point.lof import Lof
from detectors.subsequence.mp_stumpy import MP_stumpy
from detectors.subsequence.norma_wrap import Norma_wrapper
from detectors.subsequence.s2g_wrap import Series2graph_wrapper
from detectors.subsequence.sand_wrap import SAND_wrapper
from detectors.point.xstream_wrap import Xstream
from feature_extraction.default_feature import Default_feature
from feature_extraction.hjorth_activity_feature import Hjorth_activity_feature
from load_data.load_chb_mit import Load_CHB_MIT
from load_data.load_influx import Load_Influx
from postprocessing.default_preprocessing import Default_postprocessing
from postprocessing.min_max_scaler_preprocessing import Min_max_scaler_postprocessing


class Write_format_enum(enum.Enum):
    CSV = 'csv'
    INFLUX = 'influx'


class Load_data_enum(enum.Enum):
    CHB_MIT = Load_CHB_MIT
    INFLUX = Load_Influx


class Feature_extraction_enum(enum.Enum):
    HJORTH_ACTIVITY = Hjorth_activity_feature
    DEFAULT = Default_feature


class Detector_enum(enum.Enum):
    LOF = Lof
    IFOREST = Iforest
    KMEANS = Kmeans
    KNN = Knn
    XSTREAM = Xstream
    S2G = Series2graph_wrapper
    NORMA = Norma_wrapper
    SAND = SAND_wrapper
    STUMPY = MP_stumpy


class Postprocessing_enum(enum.Enum):
    MIN_MAX_SCALER = Min_max_scaler_postprocessing
    DEFAULT = Default_postprocessing


class Metrics_enum(enum.Enum):
    POINT = 'point'
    ALL = 'all'
