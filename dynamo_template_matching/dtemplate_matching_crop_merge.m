%
% Script to merge table from template matching
%
tblDir = 'table';
tomoListFile = 'tomograms.vll';
cbnTblFile = 'mergedTable.tbl';
starFileName = 'mergedStar.star';
boxSize = 64;
mw = 12; % Number of worker/cores

% Output
docFilePath = 'tomograms.doc';


run /london/data0/software/dynamo/dynamo_activate.m

% Parse tomo doc
fileID = fopen(tomoListFile); listTomo = textscan(fileID,'%s'); fclose(fileID);
listTomo = listTomo{1};
nTomo = length(listTomo); % get total number of tomogramsmkdir(outDir)

% Making docFilePath to record tomoNumber
outfileID = fopen(docFilePath, 'wt');
for idx = 1:nTomo
	fprintf(outfileID, '%d\t%s\n', idx, listTomo{idx});
end

fclose(outfileID)


% Set target folder & crop
for idx = 1:nTomo
	tomo = listTomo{idx};
	[tomoPath, tomoName, ext] = fileparts(tomo);
	% IMOD 4.11 specific
	tomoName = strrep(tomoName, '_rec', '');
	disp(['Reading ' tblDir '/' tomoName '_peaks.tbl']);
	tableName{idx} = [tblDir '/' tomoName '_peaks.tbl'];
	targetFolder{idx} = [tomoName '_Particles'];
	tableNameCrop{idx} = [targetFolder{idx} '/crop.tbl'];
	disp(targetFolder{idx});
	tbl = dread(tableName{idx});
	% Insert tomogram name
	tbl(:,20) = tbl(:,20)*0 + idx;
	dtcrop(tomo,tbl,targetFolder{idx},boxSize,'mw',mw);
end

% create ParticleListFile object (this object only exists temporarily in matlab)
plfClean = dpkdata.containers.ParticleListFile.mergeDataFolders(targetFolder, 'tables', tableNameCrop);

% create and write the .star file
plfClean.writeFile(starFileName);

% create merged table
disp('Writing the merged table and star file');
tMergedClean = plfClean.metadata.table.getClassicalTable();
dwrite(tMergedClean,cbnTblFile);
