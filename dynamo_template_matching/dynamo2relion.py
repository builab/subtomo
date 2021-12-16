#/usr/bin/python3
# Convert dynamo table to relion
# Conversion based on the tomograms.doc, therefore, it will be a lot easier to organize than dynamo2relion from Pyle
# https://pypi.org/project/dynamo2relion/
# Better use the starfile from Alister Burt in the future
# Huy Bui, McGill 2021

import numpy as np
import pandas as pd
import argparse

from eulerangles import euler2matrix
from eulerangles import matrix2euler
from eulerangles import euler2euler
from eulerangles import convert_eulers

def write_star_4(dfin, outfile):
	out = open(outfile, 'w')
	out.write("# version 30001\n\n")
	out.write("data_particles\n\n")
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
	eulers_dynamo = tbl[:,6:9]
	eulers_relion = convert_eulers(eulers_dynamo, source_meta='dynamo', target_meta='warp')
	df_all['TomoName'] = tbl[:,19].astype(int)
	df_all['CoordinateX'] = tbl[:,23]*binFactor;
	df_all['CoordinateY'] = tbl[:,24]*binFactor;
	df_all['CoordinateZ'] = tbl[:,25]*binFactor;
	df_all['OriginXAngst'] = tbl[:,3]*0;
	df_all['OriginYAngst'] = tbl[:,4]*0;
	df_all['OriginZAngst'] = tbl[:,5]*0;
	df_all['ClassNumber'] = tbl[:,21].astype(int);
	df_all['TomoManifoldIndex'] = tbl[:,21].astype(int); # Place holder, no use
	df_all['AngleRot'] = eulers_relion[:,0]
	df_all['AngleTilt'] = eulers_relion[:,1]
	df_all['AnglePsi'] = eulers_relion[:,2]
	df_all['TomoParticleId'] = np.arange(len(df_all), dtype=np.int16) + 1
	
	#print(df_all)
	
	# Loop through tomoName to replace with name
	for idx in len(df_tomolist):
		print(idx)
	
	tomoPath = df_tomolist.loc[idx, 'TomoPath'];
	tomoNum = df_tomolist.loc[idx, 'TomoNo'];
	tomoName = os.path.basename(tomoName)
	tomoName = tomoName.replace('_rec.mrc', '.mrc') 
	df_all["TomoName"].replace({tomoNum:tomoName}, inplace=True)
	
	write_star_4(df_all, args.ostar) 
