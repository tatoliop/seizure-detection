function [patientNo, recordNo, data, channelNo, labelCol] = prepareData(filepath, filename)
    

    %Sampling of dataset
    sampling = 256;
    %Channels for extraction
    filters = ["FP1-F7", "F7-T7","T7-P7","P7-O1","FP1-F3","F3-C3","C3-P3","P3-O1","FP2-F4","F4-C4","C4-P4","P4-O2","FP2-F8","F8-T8","T8-P8","P8-O2","FZ-CZ","CZ-PZ","T7-FT9","FT9-FT10","FT10-T8"];

    if(endsWith(filename, ".csv"))
        %Get patient, record and event no
        exprPatient = replace(regexp(filename,'p[0-9]+','match'),"p","");
        exprRecord = replace(regexp(filename,'r[0-9]+','match'),"r","");
        patientNo = str2num(exprPatient{1});
        recordNo = str2num(exprRecord{1});
        data = readtable(filepath);
    elseif(endsWith(filename,".edf"))
        exprPatient = replace(regexp(filename,'chb[0-9]+','match'),"chb","");
        exprRecord = replace(regexp(filename,'_[0-9]+','match'),"_","");
        patientNo = str2num(exprPatient{1});
        recordNo = str2num(exprRecord{1});
        %Get signal from edf
        [signal, times, labels] = readEdf(filepath);
        %Check length and escape if it has less channels
        if(size(signal,2) < length(filters))
            ME = MException('prepareData:filtering','Signals are less than the filter');
            throw(ME);
        end
        %Filter channels
        [filteredSignal, filteredLabels] = filterChannels(signal, labels, filters);
        %Re-Check length and escape if it has less channels
        if(size(filteredSignal,2) ~= length(filters))
            ME = MException('prepareData:filtering','Signals are less than the filter');
            throw(ME);
        end
        %Get ground truth
        truth = getTruth(patientNo, recordNo);
        %Create the type column
        type = zeros(size(filteredSignal,1), 1);
        for i=1:size(truth,1)
            ictalStart = truth(i,1) * 256;
            ictalEnd = (truth(i,2) * 256) - 1;
            type(ictalStart : ictalEnd,1) = 1;
        end
        %Return stats
        channelNo = size(filteredSignal,2);
        labelCol = size(filteredSignal,2) + 1;
        %Add the type
        filteredSignal(:, labelCol) = type;
        filteredLabels(:, labelCol) = "Type";
        data = array2table(filteredSignal(:,:));
        data.Properties.VariableNames(:) = filteredLabels(1,:);
    end
end

function [newSignal, newLabels] = filterChannels(signal, labels, filters)
    count = 1;
    newSignal = [];
    newLabels = filters;
    for channel=1:length(filters)
        index = (find(labels(:,1) == filters(channel)));
        if(isempty(index))
            continue
        end
        newSignal(:,count) = signal(:,index(1));
        count = count + 1;
    end
end




