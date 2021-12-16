%
% Script to use a different CC threshold for template matching: lower = more particles
%
% Input
threshold = 0.09; % New threshold
outDir = 'table_threshold'; % New output directory
tomoListFile = 'tomograms.vll';

run /london/data0/software/dynamo/dynamo_activate.m


% Parse tomo file
fileID = fopen(tomoListFile); listTomo = textscan(fileID,'%s'); fclose(fileID);
listTomo = listTomo{1};
nTomo = length(listTomo); % get total number of tomogramsmkdir(outDir)

for i = 1:nTomo
	tomo = listTomo{i};
	[tomoPath, tomoName, ext] = fileparts(tomo);
    pts = dread([tomoName '.TM/process.mat']);
    myTable = pts.peaks.computeTable('mcc',threshold);
	tableOriginalScale = dynamo_table_rescale(myTable,'factor',2);
	disp([outDir '/' tomoName '_peaks.tbl'])
	dwrite(tableOriginalScale, [outDir '/' tomoName '_peaks.tbl']);
end
