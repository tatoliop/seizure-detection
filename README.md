## Description

The aim of the repository is to provide different sets of unsupervised algorithms for time-series outlier detection for the purpose of detecting seizure segments in EEG.

## Dataset

The dataset used is the [CHB-MIT EEG database](https://physionet.org/content/chbmit/1.0.0/). The dataset has EEG recordings of 24 subjects with 256 Hz sampling rate with 21 bipolar channels. The complete unzipped directory of the dataset should be available and the path should be provided in the `.env` file for the code to work. 

## Preprocessing

The pre-processing includes only the [Hjorth Activity](https://en.wikipedia.org/wiki/Hjorth_parameters) feature which is extracted per channel. For each 256 recordings (once per second) the Activity measure has been computed. This means that for each 1-hour session the preprocessed data contain 3600 values per channel.

## Detection algorithms

At present there are 9 algorithms supported:

* LOF [1] (through the [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) [8] repository)
* Isolation Forest [2] (through the [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) [8] repository)
* K-Means [9] (through the [TimeEval-algorithms](https://github.com/timeeval/timeeval-algorithms) [12] repository)
* K-NN [10] (through the [TimeEval-algorithms](https://github.com/timeeval/timeeval-algorithms) [12] repository)
* XStream [3] (through the [XStream](https://github.com/cmuxstream/cmuxstream-core) repository)
* NormA [4] (through the [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) [8] repository)
* Series2Graph [5] (through the [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) [8] repository)
* SAND [11] (through the [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) [8] repository)
* Matrix Profile [7] ([Stump](https://stumpy.readthedocs.io/en/latest/index.html) algorithm)

## Deployment

The deployment needs the set of services available in `docker-compose-services.yml` file of the `Docker` folder. The `MLflow` service is mandatory to store the results from the experiments. The rest of the services are optional and can be used to write/read/visualize data.

To build the docker image, from the repository folder run the command `docker build -t seizuredetection:1.0.0 -f Dockerfile .`

An example `docker-compose-app.yml` file is available on the `Docker` folder to run the experiments with the current settings.

The experimental settings are currently hardcoded in the code. Every necessary/optional variables are available in the `.env.example` file of the `Docker` repository.

The 'environment.yaml` file in the root folder is available to debug/test the code on a local python environment.

## References

[1] Breunig, Markus M., Hans-Peter Kriegel, Raymond T. Ng, and Jörg Sander. "LOF: identifying density-based local outliers." In Proceedings of the 2000 ACM SIGMOD international conference on Management of data, pp. 93-104. 2000.

[2] Liu, Fei Tony, Kai Ming Ting, and Zhi-Hua Zhou. "Isolation forest." In 2008 eighth ieee international conference on data mining, pp. 413-422. IEEE, 2008.

[3] Manzoor, Emaad, Hemank Lamba, and Leman Akoglu. "xstream: Outlier detection in feature-evolving data streams." In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pp. 1963-1972. 2018.

[4] Paul Boniol, Michele Linardi, Federico Roncallo, Themis Palpanas, Mohammed Meftah. Emmanuel Remy. Unsupervised and Scalable Subsequence Anomaly Detection in Large Data Series. International Journal on Very Large Data Bases (VLDBJ), 2021 

[5] Paul Boniol and Themis Palpanas, Series2Graph: Graph-based Subsequence Anomaly Detection in Time Series, PVLDB, 2020

[6] Van Benschoten, Andrew H., Austin Ouyang, Francisco Bischoff, and Tyler W. Marrs. "MPA: a novel cross-language API for time series analysis." Journal of Open Source Software 5, no. 49 (2020): 2179.

[7] Law, Sean M. "STUMPY: A powerful and scalable Python library for time series data mining." Journal of Open Source Software 4, no. 39 (2019): 1504.

[8] Paparrizos, John, Yuhao Kang, Paul Boniol, Ruey S. Tsay, Themis Palpanas, and Michael J. Franklin. "TSB-UAD: an end-to-end benchmark suite for univariate time-series anomaly detection." Proceedings of the VLDB Endowment 15, no. 8 (2022): 1697-1711.

[9] Yairi, Takehisa, Yoshikiyo Kato, and Koichi Hori. "Fault detection by mining association rules from house-keeping data." proceedings of the 6th International Symposium on Artificial Intelligence, Robotics and Automation in Space. Vol. 18. Citeseer, 2001.

[10] Ramaswamy, Sridhar, Rajeev Rastogi, and Kyuseok Shim. "Efficient algorithms for mining outliers from large data sets." Proceedings of the 2000 ACM SIGMOD international conference on Management of data. 2000.

[11] Boniol, Paul, et al. "SAND: streaming subsequence anomaly detection." Proceedings of the VLDB Endowment 14.10 (2021): 1717-1729.

[12] Schmidl, Sebastian, Phillip Wenig, and Thorsten Papenbrock. "Anomaly detection in time series: a comprehensive evaluation." Proceedings of the VLDB Endowment 15.9 (2022): 1779-1797.