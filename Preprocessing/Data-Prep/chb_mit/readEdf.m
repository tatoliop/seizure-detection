function [signals, times, labels] = readEdf(path, varargin)
    defaultSignal = 0;
    
    p = inputParser;
    validScalarPosNum = @(x) isnumeric(x) && isscalar(x) && (x > 0);
    addRequired(p,'path',@isstring);
    addOptional(p,'signal',defaultSignal,validScalarPosNum);
    parse(p,path,varargin{:});
    tmpSignal = p.Results.signal;

    info = edfinfo(path);
    no_signals = length(info.SignalLabels);

    tt = edfread(path); % Get the data
    RecTime = seconds(tt.('Record Time')); % Get Time Variable
    
    if(tmpSignal ~= defaultSignal && tmpSignal <=no_signals)
        [signals, times] = getSignal(tt, RecTime, tmpSignal); %get signal and time
    else
        for i = 1:no_signals
            %if(info.SignalLabels(i) ~= "-") %Remove dummy signals
                [sig, time] = getSignal(tt, RecTime, i); %get signal and time
                if(i == 1) %init arrays
                    len = length(sig);
                    signals = zeros(len, 3);
                    times = zeros(len, 3);
                end
                %store them
                signals(:,i) = sig;
                times(:,i) = time;
            %end
        end
    end
    labels = info.SignalLabels;
    [signals, times, labels] = clearSignals(signals, times, labels);
end

function [signal, time] = getSignal(tt, RecTime, i)
    row = tt.(i);
    signal = cat(1,row{:}); % Concatenate The signal
    Ts = numel(row{1})/mean(diff(RecTime)); % Sampling Intervals (Samples/Second)
    time = linspace(0, numel(signal)-1, numel(signal)).'/Ts; % Create Continuous Time Vector
end

function [signal, time, labels] = clearSignals(signal, time, labels)

    for channel=1:size(signal,2)-1
        counter = channel + 1;
        if (strcmp(char(labels(channel)),'ECG')==1) || ...
           (strcmp(char(labels(channel)),'VNS')==1) || ...
           (strcmp(char(labels(channel)),'-')==1) || ...
           (strcmp(char(labels(channel)),'.')==1) || ...
           (strcmp(char(labels(channel)),'LOC-ROC')==1) || ...
           (strcmp(char(labels(channel)),'LUE-RAE')==1) || ...
           (strcmp(char(labels(channel)),'EKG1-EKG2')==1) || ...
           mean(signal(:,channel))==0
            
            signal(:,channel) = 0;
            continue
        else
            while counter <= size(signal,2)
                if (strcmp(char(labels(counter)),'ECG')==1) || ...
                   (strcmp(char(labels(counter)),'VNS')==1) || ...
                   (strcmp(char(labels(counter)),'-')==1) || ...
                   (strcmp(char(labels(counter)),'.')==1) || ...
                   (strcmp(char(labels(counter)),'LOC-ROC')==1) || ...
                   (strcmp(char(labels(counter)),'LUE-RAE')==1) || ...
                   (strcmp(char(labels(counter)),'EKG1-EKG2')==1) || ...
                   mean(signal(:,counter))==0
        
                     signal(:,counter) = 0;
                     counter = counter + 1;
                else
                    % mirror channel
                    a = signal(:,channel) + signal(:,counter);
                    if max(a) <= 10
                        signal(:,counter) = 0;
                    end
                    % same channel
                    a = signal(:,channel) - signal(:,counter);
                    if max(a) <= 10
                        signal(:,counter) = 0;
                    end
                    counter = counter + 1;
                end
            end
        end
    end
    channel=1;
    while channel<=size(signal,2)
        if mean(signal(:,channel))==0
            signal(:,channel)=[];
            time(:,channel) = [];
            labels(channel) = [];
        else
            channel=channel+1;
        end
    end
end


