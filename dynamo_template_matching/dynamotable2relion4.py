#/usr/bin/python3
# Convert dynamo table to relion 4
# A lot of the code is from dynamo2m
# Now using dynamotable & starfile from Alisterburt
# Conversion based on the tomograms.doc, therefore, it will be a lot easier to organize than dynamo2relion from Pyle
# https://pypi.org/project/dynamo2relion/
#
# Better use the starfile from Alister Burt in the future
# Output also the tomograms_descr.star
# Huy Bui, McGill 2021

import numpy as np
import pandas as pd
import argparse, os
import starfile
import dynamotable
import re

from eulerangles import convert_eulers

def dynamo2relion4 (input_table_file, table_map_file, output_star_file, binFactor):
 	# Modify now with angpix to make sure it is specified correctly
	# Read table file into dataframe
	table = dynamotable.read(input_table_file, table_map_file)

	# Prep data for star file in dict
	data = {}

	# extract xyz into dict with relion style headings
	for axis in ('x', 'y', 'z'):
		heading = f'rlnCoordinate{axis.upper()}'
		shift_axis = f'd{axis}'
		data[heading] = (table[axis] + table[shift_axis])*binFactor

	#data['TomoParticleId'] = np.arange(len(data), dtype=np.int16) + 1

	# extract and convert eulerangles
	eulers_dynamo = table[['tdrot', 'tilt', 'narot']].to_numpy()
	eulers_warp = convert_eulers(eulers_dynamo, source_meta='dynamo',target_meta='warp')
	data['rlnAngleRot'] = eulers_warp[:, 0]
	data['rlnAngleTilt'] = eulers_warp[:, 1]
	data['rlnAnglePsi'] = eulers_warp[:, 2]

	
	# extract and sanitise micrograph names to ensure compatibility with M
	data['rlnTomoName'] = table['tomo_file'].apply(sanitise_imod_tomo_name)

	print(data)
	# convert dict to dataframe
	df = pd.DataFrame.from_dict(data)

	# write out STAR file
	starfile.write(df, output_star_file, overwrite=True)

	# echo to console
	print(f"Done! Converted '{input_table_file}' to RELION/Warp compatible STAR file '{output_star_file}'")

	return
	
def sanitise_imod_tomo_name(micrograph_name: str) -> str:
	"""
	Replaces tomogram name from IMOD reconstructions with corresponding name file if appropriate
	Ensures compatibility with M for subsequent STAR files
	:param micrograph_name:
	:return:
	"""
	micro = re.sub(r"_rec.mrc", "", micrograph_name)
	return re.sub(r"^.*\/", "", micro)
	
	



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

	# Convert Coordinate
	dynamo2relion4(args.tbl, args.tomodoc, args.ostar, float(args.bin))
	
	# Convert tomo description file
	tomodoc_header=["TomoNo", "TomoPath"]
	df_tomolist = pd.read_csv(args.tomodoc, delim_whitespace=True, names=tomodoc_header, index_col=False)
	#print(df_tomolist)

	
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
		
	#print("Writing tomogram description tomograms_descr.star\n")
	#write_star_4(df_descr, "", 'tomograms_descr.star')
	starfile.write(df_descr, args.ostar.replace(".star", "_tomo_descr.star"))
	print("Done! Write " + args.ostar.replace(".star", "_tomo_descr.star"))
	
