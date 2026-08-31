%% Import data from text file.
% This script imports AllDistances.csv received from Erin on 9/19/2016 and
% computes routing distances for each.

%% Import starting and desitination nodes
fprintf('Importing .csv file...\n');
filename = 'C:\Users\masariat\Documents\MATLAB\AllDistances.csv';
delimiter = ',';
startRow = 2;
% Format string for each line of text:
formatSpec = '%s%s%s%f%f%f%f%[^\n\r]'; %Specific to .csv format
% Open the text file.
fileID = fopen(filename,'r');
% Read columns of data according to format string.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);
% Close the text file.
fclose(fileID);
% Allocate imported array to column variable names
ResHomeUnitCd = dataArray{:, 1};
StartingIncID = dataArray{:, 2};
DestinationIncID = dataArray{:, 3};
StartingLatitude = dataArray{:, 4};
StartingLongitude = dataArray{:, 5};
DestinationLatitude = dataArray{:, 6};
DestinationLongitude = dataArray{:, 7};
% Clear temporary variables
clearvars filename delimiter startRow formatSpec fileID dataArray ans;

%% Batch distance calculations
% Load road network
load('C:\Users\masariat\Documents\MATLAB\roads.mat');
% Call main_DistCalc with plotting
numCalls = numel(ResHomeUnitCd); %Total number of calls
fprintf('Starting distance calculations (%i calls)...\n',numCalls);
thresh = 0.0; %Threshold to track progress
dist = NaN*ones(numCalls,1);
fprintf('    Progress:');
for kk = 1:numCalls
    if (100.0*kk/numCalls > thresh)
        fprintf(' %i%%,',thresh);
        thresh = thresh + 2.0;
    end
    optimal = main_DistCalc([StartingLongitude(kk,1) StartingLatitude(kk,1) 0;...
        DestinationLongitude(kk,1) DestinationLatitude(kk,1) 0],roads,false(1));
    dist(kk,1) = optimal(1).cost; %Parse optimal distance
end
fprintf(' 100%%\n');

%% Write to .csv output
fprintf('Writing to .xlsx file...\n');
xlswrite('C:\Users\masariat\Documents\MATLAB\AllDistancesALEX.xlsx',...
    [ResHomeUnitCd(1:numCalls,1)...
    StartingIncID(1:numCalls,1)...
    DestinationIncID(1:numCalls,1)...
    num2cell(StartingLatitude(1:numCalls,1))...
    num2cell(StartingLongitude(1:numCalls,1))...
    num2cell(DestinationLatitude(1:numCalls,1))...
    num2cell(DestinationLongitude(1:numCalls,1))...
    num2cell(dist)] );
fprintf('DONE\n');