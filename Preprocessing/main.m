clc
clear

base_path = "/media/data/datasets/EEG";
%Get full path
dataset_path = base_path + "/chb-mit-scalp-eeg-database-1.0.0/seizures"; %A folder that only contains the files with seizures for each subject
%Get folders
dirFolders = dir(dataset_path);
isub = [dirFolders(:).isdir]; %# returns logical vector
myFolders = {dirFolders(isub).name}';
myFolders(ismember(myFolders,{'.','..'})) = [];
totalFolders = length(myFolders);
%For each folder/patient
for folder = 1 : totalFolders
    currFolder = dataset_path + "/" + myFolders(folder);
    myFiles = dir(fullfile(currFolder,'*.edf')); %gets all edf files in struct
    totalFiles = length(myFiles);
    %Extract ictal events
    for file = 1: totalFiles
        fileName = myFiles(file).name;
        try
            pipeline(currFolder, fileName);
        catch
            disp("Error on file " + fileName);
            continue
        end
    end
end