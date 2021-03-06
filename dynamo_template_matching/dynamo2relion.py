#/usr/bin/python3
# Convert dynamo table to relion
# Conversion based on the tomograms.doc, therefore, it will be a lot easier to organize than dynamo2relion from Pyle
# https://pypi.org/project/dynamo2relion/
#
# Better use the starfile from Alister Burt in the future
# Output also the tomograms_descr.star
# Huy Bui, McGill 2021

import numpy as np
import pandas as pd
import argparse, os

from eulerangles import euler2matrix
from eulerangles import matrix2euler
from eulerangles import euler2euler
from eulerangles import convert_eulers

def write_star_4(dfin, tag, outfile):
	out = open(outfile, 'w')
	out.write("# version 30001\n\n")
	out.write("data_{:s}\n\n".format(tag))
	out.write("loop_\n")
	for i in range(len(dfin.columns)):
		out.write('_rln{:s} #{:d}\n'.format(dfin.columns[i], i+1))
	out.write(dfin.to_string(index=False, header=False))
	out.write("\n")
	out.close()		



if __name__=='__main__':
   	# get name of input starfile, output starfile, output stack file
	print('Script to convert from Dynamo to Relion 4')
	
	parser = argparse.ArgumentParser(description='Convert tbl file to Relion 4.0 input file')
	parser.add_argument('--tbl', help='Input table file',required=True)
	parser.add_argument('--tomodoc', help='Input tomo doc file',required=True)
	parser.add_argument('--ostar', help='Output star file',required=True)
	parser.add_argument('--angpix', help='Original pixel size',required=True)
	parser.add_argument('--bin', help='Bin of current tomo',required=True)
	parser.add_argument('--frac_dose', help='Tomo fractional dose',required=True, default=2)


	args = parser.parse_args()
	pixelSize = float(args.angpix)
	binFactor = float(args.bin)

	
	tomodoc_header=["TomoNo", "TomoPath"]
	df_tomolist = pd.read_csv(args.tomodoc, delim_whitespace=True, names=tomodoc_header, index_col=False)
	#print(df_tomolist)
	
	header_list = ["TomoName", "TomoParticleId", "TomoManifoldIndex", "CoordinateX", "CoordinateY", "CoordinateZ", "OriginXAngst", "OriginYAngst", "OriginZAngst", "AngleRot", "AngleTilt", "AnglePsi", "ClassNumber"]
	df_all = pd.DataFrame(columns = header_list)
	#print(df_all)
		
	# Renumber
	tbl = np.genfromtxt(args.tbl, delimiter=' ')
	# Set ClassNumber to 1
	tbl[:,21] = tbl[:,21]*0 + 1
	tbl[:,23:26] = tbl[:,23:26]*binFactor # Take care of binning
	eulers_dynamo = tbl[:,6:9]
	eulers_relion = convert_eulers(eulers_dynamo, source_meta='dynamo', target_meta='warp')
	#print(eulers_relion)
	df_all['TomoName'] = tbl[:,19].astype(int)
	df_all['CoordinateX'] = tbl[:,23].astype(int);
	df_all['CoordinateY'] = tbl[:,24].astype(int);
	df_all['CoordinateZ'] = tbl[:,25].astype(int);
	df_all['OriginXAngst'] = tbl[:,3]*0;
	df_all['OriginYAngst'] = tbl[:,4]*0;
	df_all['OriginZAngst'] = tbl[:,5]*0;
	df_all['ClassNumber'] = tbl[:,21].astype(int);
	df_all['TomoManifoldIndex'] = tbl[:,21].astype(int) # Place holder, no use
	df_all['AngleRot'] = eulers_relion[:,0].astype(int) # Temporary convert
	df_all['AngleTilt'] = eulers_relion[:,1].astype(int) # Temporary convert
	df_all['AnglePsi'] = eulers_relion[:,2].astype(int) # Temporary convert
	df_all['TomoParticleId'] = np.arange(len(df_all), dtype=np.int16) + 1
	
	#print(df_all)
	
	# Loop through tomoName to replace with name
	for idx in range(len(df_tomolist)):	
		tomoPath = df_tomolist.loc[idx, 'TomoPath'];
		tomoNum = df_tomolist.loc[idx, 'TomoNo'];
		tomoName = os.path.basename(tomoPath)
		tomoName = tomoName.replace('_rec.mrc', '') 
		df_all["TomoName"].replace({tomoNum:tomoName}, inplace=True)
	print("Writing coordinate file {:s}\n".format(args.ostar))
	write_star_4(df_all, "particles", args.ostar)
	
	# Making tomogram_desc.star	
	descr_header = ["TomoName", "TomoTiltSeriesName", "TomoImportCtfFindFile", "TomoImportImodDir", "TomoImportFractionalDose", "TomoImportOrderList", "TomoImportCulledFile"]
	df_descr = pd.DataFrame(columns =descr_header)
	for idx in range(len(df_tomolist)):	
		tomoPath = df_tomolist.loc[idx, 'TomoPath'];
		tomoNum = df_tomolist.loc[idx, 'TomoNo'];
		tomoName = os.path.basename(tomoPath)
		tomoName = tomoName.replace('_rec.mrc', '') 
		tsName = "tomograms/{:s}/{:s}.mrc".format(tomoName, tomoName)
		ctfFile = "tomograms/{:s}/{:s}_output.txt".format(tomoName, tomoName)
		imodDir = "tomograms/{:s}".format(tomoName)
		orderList = "input/order_list.csv"
		cullMrc = "tomograms/{:s}/{:s}_culled.mrc".format(tomoName, tomoName)	
		row = [tomoName, tsName, ctfFile, imodDir, args.frac_dose, orderList, cullMrc]
		df_length = len(df_descr)
		df_descr.loc[df_length] = row
		
	print("Writing tomogram description tomograms_descr.star\n")
	write_star_4(df_descr, "", 'tomograms_descr.star')
	
