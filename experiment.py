import os

from interfaces.pipeline_interface import Pipeline_interface
from interfaces.pipeline_params_interface import Pipeline_params_interface
from params.evaluation_params import Evaluation_set
from params.point_pipeline_params import Point_pipeline_params
from params.range_pipeline_params import Range_pipeline_params
from models.record import Record
import mlflow

from pipelines.point_pipeline import Point_pipeline
from pipelines.range_pipeline import Range_pipeline


class Experiment:
    __MLFLOW_URI = os.environ["MLFLOW_URI"] if os.environ.get(
        'MLFLOW_URI') is not None else 'localhost:8080'

    def __init__(self,
                 input_data: Record,
                 params: list[Pipeline_params_interface],
                 evaluation_params: Evaluation_set):
        self.__input = input_data
        self.__params = params
        self.__eval_params = evaluation_params
        mlflow.tracking.set_tracking_uri(self.__MLFLOW_URI)
        mlflow.set_experiment(self.__get_experiment_name())

    def run_experiments(self):
        total_experiments = len(self.__params)
        counter_experiment = 1
        for param in self.__params:
            print(f'Starting detection experiment {counter_experiment}/{total_experiments}.')
            # Init pipeline
            pipeline = None
            range_pipeline = False
            range_size = 1
            if isinstance(param, Range_pipeline_params):
                pipeline = Range_pipeline(param)
                range_pipeline = True
                range_size = param.subsequence_size
            elif isinstance(param, Point_pipeline_params):
                pipeline = Point_pipeline(param)
                range_pipeline = False
                range_size = 1
            if pipeline is None:
                raise ValueError('Error creating pipeline.')
            pipeline.execute(self.__input)
            # Get evaluation parameters
            eval_param_list = self.__eval_params.cartesian if range_pipeline else self.__eval_params.coeff
            # For each evaluation parameter compute the metrics
            for eval_param in eval_param_list:
                metrics = pipeline.metrics(**eval_param)
                for dim in metrics.keys():
                    # Store experiment
                    run_name = self.__get_run_name(pipeline, dim, range_pipeline)
                    exp_params = self.__get_run_params(pipeline, range_pipeline, range_size)
                    with mlflow.start_run(run_name=run_name):
                        mlflow.log_params(exp_params)
                        mlflow.log_params(eval_param)
                        mlflow.log_param('dimension', dim)
                        mlflow.log_metrics(metrics[dim])
            print(f'Detection experiment {counter_experiment}/{total_experiments} completed.')
            counter_experiment += 1

    def __get_experiment_name(self) -> str:
        experiment_name = self.__input.record_id.dataset + '-' + self.__input.record_id.subject + '-' + self.__input.record_id.record
        return experiment_name

    @staticmethod
    def __get_run_name(pipeline: Pipeline_interface, dimension: str, subsequence: bool) -> str:
        run_name = pipeline.detector.name
        run_name = run_name + '-' + dimension
        run_name = 'Subsequence-' + run_name if subsequence else 'Point-' + run_name
        return run_name

    @staticmethod
    def __get_run_params(pipeline: Pipeline_interface, subsequence: bool, subsequence_size: int) -> dict:
        techniques = pipeline.technique_names
        params = pipeline.params
        exp_type = 'Subsequence' if subsequence else 'Point'
        final_type = {'type': exp_type, 'experiment_subsequence_size': subsequence_size}
        run_params = techniques | params | final_type
        return run_params
