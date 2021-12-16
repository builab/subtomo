%
% Script to use relion4_tomo_robot for autoalignment of tiltseries
% Required alignment of relion4_tomo_robot
% Use on cluster (however, need to change to autoalign.m for not crashing)

run /london/data0/software/dynamo/dynamo_activate.m
run /london/data0/software/relion_tomo_robot/robot_activate.m

local_cluster = parcluster('local');

local_cluster.JobStorageLocation = '/tmp'
local_cluster.NumWorkers = 12
  
tiltaxisangle=85.7;
beadDiameter = 15; % nm
pixelSize = 2.12;
tsDir = "/london/data0/2021_RNA_Ribosome/tiltseries"; % tsDir must contain tilt series director TS_01, TS_02, TS_03 etc. Stack must be .st)

dautoalign4relion(tsDir, pixelSize, beadDiameter, tiltaxisangle, 'default')
