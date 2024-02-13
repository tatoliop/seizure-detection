classdef FeatureExtraction
    %FEATUREEXTRACTION Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        signal table
        channels {mustBeNumeric}
        label {mustBeNumeric}
    end
    
    methods
        
        function obj = FeatureExtraction(signal, label)
            %FEATUREEXTRACTION Construct an instance of this class
            %   Detailed explanation goes here
            obj.signal = signal;
            obj.label = label;
            obj.channels = size(signal,2);
            if(label ~= 0)
                obj.channels = size(signal,2) - 1;
            end
        end

        function result = getFeature(obj, feature)
            features = getResult(obj, obj.signal{:,1:obj.channels}, feature);
            if(obj.label ~= 0)
                ictal = ismember(1,obj.signal{:,obj.label});
                tmpArray = [features, ictal];
                result = array2timetable(tmpArray, 'RowTimes', seconds(1), 'VariableNames', obj.signal.Properties.VariableNames);
            else
                result = array2timetable(features, 'RowTimes', seconds(1), 'VariableNames', obj.signal.Properties.VariableNames);
            end
        end

        function result = getFeatureWindowed(obj, feature, windowSize)
            features = [];
            counter = 1;
            %Window data
            windowStart = 1;
            while windowStart < size(obj.signal,1)
                windowEnd = windowStart + windowSize - 1;
                if(windowEnd > size(obj.signal,1))
                    windowEnd = size(obj.signal,1);
                end
                %Get current window data
                windowData = obj.signal{windowStart:windowEnd, 1:obj.channels};
                %Get feature for current window
                tmpFeatures = getResult(obj, windowData, feature);
                if(obj.label ~= 0)
                    ictal = ismember(1,obj.signal{windowStart:windowEnd,obj.label});
                    features(counter, :) = [tmpFeatures, ictal];
                else
                    features(counter, :) = tmpFeatures;
                end
                counter = counter + 1;
                %Slide window
                windowStart = windowStart + windowSize;
            end
            result = array2timetable(features, 'RowTimes', seconds(1:counter - 1), 'VariableNames', obj.signal.Properties.VariableNames);
        end

    end

    methods (Access = private)

        function result = getResult(obj, signal, feature)
                if(feature == 'HjorthActivity')
                    result = getHjorthActivity(obj, signal);
                elseif(feature == 'HjorthMobility')
                    result = getHjorthMobility(obj, signal);
                elseif(feature == 'HjorthComplexity')
                    result = getHjorthComplexity(obj, signal);
                end
        end

        function result = getHjorthActivity(obj, signal)
            result = var(signal,[],1);
        end
        function result = getHjorthMobility(obj, signal) %Not good results - visually
            DIFF1=diff(signal,1,1);
            result = std(DIFF1,[],1)./(std(signal,[],1)+eps); 
        end
        function result = getHjorthComplexity(obj, signal) %Not good results - visually
            DIFF1=diff(signal,1,1);
            DIFF2=diff(signal,2,1);
            mobility = getHjorthMobility(obj,signal);
            result = (std(DIFF2,[],1)./(std(DIFF1,[],1)+eps))./(mobility+eps);
        end
        
    end
end

