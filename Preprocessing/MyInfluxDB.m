classdef MyInfluxDB
    properties (Access = private)
        URL
        USER
        PASS
        DATABASE
        influxdb
    end
    
    methods
        function obj = MyInfluxDB()
            % Build an InfluxDB client
            obj.URL = 'http://localhost:8086';
            obj.USER = 'user';
            obj.PASS = 'password';
            obj.DATABASE = 'eeg';
            obj.influxdb = InfluxDB(obj.URL, obj.USER, obj.PASS, obj.DATABASE);
        end
        
        function writeChannels(obj, data, channelNo, Fs, patientNo, recordNo)
            seriesName = 'Raw';
            %Create timetable
            my_timetable = table2timetable(data,"SampleRate",Fs);
            my_timetable.Time = datetime('01.01.2023','InputFormat','dd.mm.yyyy') + my_timetable.Time;
            obj.writeTimetable(my_timetable, channelNo, seriesName, patientNo, recordNo);
        end
    
        function writeFeatures(obj, data, channelNo, seriesName, patientNo, recordNo)
            %Create timetable
            data.Time = datetime('01.01.2023','InputFormat','dd.mm.yyyy') + data.Time;
            obj.writeTimetable(data, channelNo, seriesName, patientNo, recordNo);
        end
    end

    methods (Access = private)

        function writeTimetable(obj, data, channelNo, seriesName, patientNo, recordNo)
            ictalLabel = 'Ictal';
            nonIctalLabel = 'Non ictal';
            ictal = find(data.Type == 1);
            if(~isempty(ictal))
                startIctal = ictal(1);
                %Write first non-ictal
                toWrite = data(1:startIctal-1,1:channelNo);
                obj.writeData(seriesName, toWrite, patientNo, recordNo, nonIctalLabel);
                idx = 1;
                while(idx < length(ictal))
                    diff = ictal(idx + 1) - ictal(idx);
                    if(diff ~= 1) %write ictal and non-ictal till next idx
                        %Ictal
                        toWrite = data(startIctal:ictal(idx),1:channelNo);
                        obj.writeData(seriesName, toWrite, patientNo, recordNo, ictalLabel);
                        %Non ictal
                        toWrite = data(ictal(idx) + 1:ictal(idx+1) - 1,1:channelNo);
                        obj.writeData(seriesName, toWrite, patientNo, recordNo, nonIctalLabel);
                    end
                    idx = idx + 1;
                end
                %Ictal
                toWrite = data(startIctal:ictal(end),1:channelNo);
                obj.writeData(seriesName, toWrite, patientNo, recordNo, ictalLabel);
                %Non ictal
                toWrite = data(ictal(end) + 1:end,1:channelNo);
                obj.writeData(seriesName, toWrite, patientNo, recordNo, nonIctalLabel);
            else
                %Non ictal
                toWrite = data(:,1:channelNo);
                obj.writeData(seriesName, toWrite, patientNo, recordNo, nonIctalLabel);
            end

        end
    
        function writeData(obj, series, data, patientNo, recordNo, label)
            series = Series(series)...
                .tags('patient', patientNo, 'record', recordNo, 'label', label) ...
                .import(data);
            obj.influxdb.writer().append(series).execute();
        end

    end
end

