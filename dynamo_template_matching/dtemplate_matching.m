%
% Script to loop through all the tomogram from tomograms.vll for template maching
% Can be run local but on cluster as well
%

% Input
JobStorageLocation = '/tmp';
NumWorkers = 30; % same as cpu-per-task in SBATCH
mask = 'mask_tm.mrc';
ref = 'ribosome_ref_tm.mrc';
tomoListFile = 'tomograms.vll'; % list file to contain all tomogram path files
threshold = 0.09; % This threshold can be adjusted later on
outDir = 'table';

% Activate dynamo
run /london/data0/software/dynamo/dynamo_activate.m

% read and parse tomo file
fileID = fopen(tomoListFile); listTomo = textscan(fileID,'%s'); fclose(fileID);
listTomo = listTomo{1};
nTomo = length(listTomo); % get total number of tomogramsmkdir(outDir)

  
% Cluster related setting
local_cluster = parcluster('local');
local_cluster.JobStorageLocation = '/tmp';
local_cluster.NumWorkers = NumWorkers;

% make output dir
mkdir(outDir)


for i = 1:nTomo
	tomo = listTomo{i};
	[tomoPath, tomoName, ext] = fileparts(tomo);
	% Assumming name of IMOD 4.11
	tomoName = strrep(tomoName, '_rec', '');
	disp(tomoName)
	pts = dynamo_match(tomo, ref,'mask', mask, 'outputFolder', tomoName, 'ytilt',[-60,60],'sc',[256,256,256],'cr',360,'cs',30,'ir', 40,'bin',1,'mw', local_cluster.NumWorkers);
	%pts = dynamo_match(tomo, ref,'mask', mask, 'outputFolder', tomoName, 'ytilt',[-60,60],'sc',[256,256,256],'cr',360,'cs',30,'bin',1,'mw', local_cluster.NumWorkers);
	%pts.peaks.plotCCPeaks('sidelength',50);
	myTable = pts.peaks.computeTable('mcc',threshold);
	%dtplot(myTable,'pf','oriented_positions');
	%save(gcf, 'TS_001.png')
	tableOriginalScale = dynamo_table_rescale(myTable,'factor',2);
	disp([outDir '/' tomoName '_peaks.tbl'])
	dwrite(tableOriginalScale, [outDir '/' tomoName '_peaks.tbl']);

end
