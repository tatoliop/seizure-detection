import os

from params.evaluation_params import Evaluation_set
from read_pipeline_params import get_pipeline_params
from utils.enums import Load_data_enum
from experiment import Experiment
from write_data.write_data import WriteData


if __name__ == '__main__':
    DATASET_PATH = os.environ["DATASET_PATH"] if os.environ.get('DATASET_PATH') is not None else './data'
    alpha_values = [0.25, 0.5]
    coeff_values = [3]
    subsequence_size = [60, 120]
    # Initiate writer
    # writer = WriteData()
    # Initiate loader
    loader = Load_data_enum.CHB_MIT.value(path=DATASET_PATH)
    # Init pipeline params
    params = get_pipeline_params(subsequence_size)
    # Get a record and its data
    subjects = [x for x in loader.records() if x.has_episode is True]
    total_experiments = len(subjects)
    counter_experiment = 1
    for sub in subjects:
        print(f'Starting experiment on subject {sub.subject}-{sub.record}. {counter_experiment}/{total_experiments}.')
        data = loader.load_data(sub)
        if data is None:
            print(f'Error getting data on subject {sub.subject}-{sub.record}.')
            continue
        # Init experiment
        experiment = Experiment(data, params, Evaluation_set(coeff_values, alpha_values))
        experiment.run_experiments()
        print(f'Experiment on subject {counter_experiment}/{total_experiments} completed.')
        counter_experiment += 1
    #     # Write the data
    #     # writer.write_data(data, Write_format_enum.INFLUX)
    #     # writer.write_data(data, Write_format.CSV)
