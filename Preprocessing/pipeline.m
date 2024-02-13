function pipeline(datasetPath, fileName)
%% ----------Data read----------
warning('off')
addpath(genpath("Data-Prep"));
addpath(genpath("influxdb-client2"));
disp('Data read');
tic
%Vars
%Sampling per sec
Fs = 256;
%Get file
pathFileName = fullfile(datasetPath, fileName);
disp("Checking: " + fileName);
%Read data into a table with each column representing each channel
%and the label for each row that represents time values 
[patientNo, recordNo, data, channelNo, labelCol] = prepareData(pathFileName, fileName);
toc

%% ----Write signal to influx 
disp('Write signal to influx');
tic
influx = MyInfluxDB();
influx.writeChannels(data, channelNo, Fs, patientNo, recordNo);
toc

%% ----------Feature extraction----------
disp('Feature extraction');
tic
%Get features
fe = FeatureExtraction(data, labelCol);
featureType = 'HjorthActivity';
features = fe.getFeatureWindowed(featureType, Fs); %returns a timetable
toc

%% ----Write feature to influx
disp('Write feature to influx');
tic
influx = MyInfluxDB();
influx.writeFeatures(features, channelNo, featureType, patientNo, recordNo);
toc

end
