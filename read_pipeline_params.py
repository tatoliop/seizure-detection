from interfaces.pipeline_params_interface import Pipeline_params_interface
from params.point_pipeline_params import Point_pipeline_params
from params.range_pipeline_params import Range_pipeline_params
from utils.enums import Feature_extraction_enum, Detector_enum, Postprocessing_enum


def get_pipeline_params(subsequence_size: list[int]) -> list[Pipeline_params_interface]:
    pipeline_params = []
    for data in Detector_enum:
        # If point-based detectors then create additionally two point params
        if data.name in ['LOF', 'IFOREST', 'KMEANS', 'KNN', 'XSTREAM']:
            pipeline_params.append(Point_pipeline_params(
                Feature_extraction_enum.HJORTH_ACTIVITY,
                {'sampling': 1},
                data,
                {},
                Postprocessing_enum.MIN_MAX_SCALER,
                {},
                multivariate=True))
            pipeline_params.append(Point_pipeline_params(
                Feature_extraction_enum.HJORTH_ACTIVITY,
                {'sampling': 1},
                data,
                {},
                Postprocessing_enum.MIN_MAX_SCALER,
                {},
                multivariate=False))
            for sub_size in subsequence_size:
                pipeline_params.append(Range_pipeline_params(
                    Feature_extraction_enum.HJORTH_ACTIVITY,
                    {'sampling': 1},
                    data,
                    {},
                    Postprocessing_enum.MIN_MAX_SCALER,
                    {},
                    subsequence_size=sub_size))
        else:
            for sub_size in subsequence_size:
                pipeline_params.append(Range_pipeline_params(
                    Feature_extraction_enum.HJORTH_ACTIVITY,
                    {'sampling': 1},
                    data,
                    {'custom_subsequence_length': sub_size},
                    Postprocessing_enum.MIN_MAX_SCALER,
                    {},
                    subsequence_size=sub_size))

    return pipeline_params
