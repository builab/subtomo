#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to convert eman3d file to cmm for quick checking
TODO: Better to use ElementTree
HB, McGill, 2021
"""
import pandas as pd
import argparse
import xml.etree.ElementTree as ET

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Write Chimera CMM file from EMAN3D coordinate file')
	parser.add_argument('--i', help='Input EMAN 3D coordinate',required=True)
	parser.add_argument('--o', help='Output Chimera File',required=True)
	parser.add_argument('--bin', help='Bin factor of EMAN Coordinate',required=True)

	args = parser.parse_args()
  
  binFactor = float(args.bin)
  
df = pd.read_csv(docFile, delim_whitespace=True, names=header_list)
