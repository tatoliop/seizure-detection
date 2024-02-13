## Description

The aim of the repository is to provide different sets of unsupervised algorithms for time-series outlier detection for the purpose of detecting seizure segments in EEG.

## Dataset

The dataset used is the [CHB-MIT EEG database](https://physionet.org/content/chbmit/1.0.0/). The dataset has EEG recordings of 24 subjects with 256 Hz sampling rate with 21 bipolar channels. 

## Preprocessing

The dataset has been preprocessed in a Matlab environment and the [Hjorth Activity](https://en.wikipedia.org/wiki/Hjorth_parameters) feature has been extracted per channel. For each 256 recordings (once per second) the Activity measure has been computed. This means that for each 1-hour segment the preprocessed data contain 3600 values per channel.

The source code of the pre-processing steps, along with all the necessary .m files, is available in the folder `Preprocessing`.

## Algorithms

At present there are 7 algorithms supported:

* LOF [1] (through the [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) [8] repository)
* Isolation Forest [2] (through the [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) [8] repository)
* XStream [3] (through the [XStream](https://github.com/cmuxstream/cmuxstream-core) repository)
* NormA [4] (through the [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) [8] repository)
* Series2Graph [5] (through the [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) [8] repository)
* Matrix Profile [6] (MPX algorithm) (through the [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) [8] repository)
* Matrix Profile [7] ([Stump](https://stumpy.readthedocs.io/en/latest/index.html) algorithm)

## Deployment
The repository needs two additional repositories ,i.e. [TSB_UAD](https://github.com/TheDatumOrg/TSB-UAD) and [XStream](https://github.com/cmuxstream/cmuxstream-core) to be in the same root folder as the current repository, as presented below:
```
├── root
│   ├── TSB_UAD
│   ├── cmuxstream-core
│   └── seizure-detection
```
To build the docker image, from the repository folder run the command `docker build -t seizuredetection:1.0.0 -f Docker/Dockerfile .`

An example `docker-compose.yml` file is available on the `Docker` folder to run the solution with the current settings.

The experiments and the features should be in 2 `.json` files from which the project reads and runs them. The `experiment.json` and `measurement.json` files contain an example set of experiments and the feature.

## References

[1] Breunig, Markus M., Hans-Peter Kriegel, Raymond T. Ng, and Jörg Sander. "LOF: identifying density-based local outliers." In Proceedings of the 2000 ACM SIGMOD international conference on Management of data, pp. 93-104. 2000.

[2] Liu, Fei Tony, Kai Ming Ting, and Zhi-Hua Zhou. "Isolation forest." In 2008 eighth ieee international conference on data mining, pp. 413-422. IEEE, 2008.

[3] Manzoor, Emaad, Hemank Lamba, and Leman Akoglu. "xstream: Outlier detection in feature-evolving data streams." In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pp. 1963-1972. 2018.

[4] Paul Boniol, Michele Linardi, Federico Roncallo, Themis Palpanas, Mohammed Meftah. Emmanuel Remy. Unsupervised and Scalable Subsequence Anomaly Detection in Large Data Series. International Journal on Very Large Data Bases (VLDBJ), 2021 

[5] Paul Boniol and Themis Palpanas, Series2Graph: Graph-based Subsequence Anomaly Detection in Time Series, PVLDB, 2020

[6] Van Benschoten, Andrew H., Austin Ouyang, Francisco Bischoff, and Tyler W. Marrs. "MPA: a novel cross-language API for time series analysis." Journal of Open Source Software 5, no. 49 (2020): 2179.

[7] Law, Sean M. "STUMPY: A powerful and scalable Python library for time series data mining." Journal of Open Source Software 4, no. 39 (2019): 1504.

[8] Paparrizos, John, Yuhao Kang, Paul Boniol, Ruey S. Tsay, Themis Palpanas, and Michael J. Franklin. "TSB-UAD: an end-to-end benchmark suite for univariate time-series anomaly detection." Proceedings of the VLDB Endowment 15, no. 8 (2022): 1697-1711.