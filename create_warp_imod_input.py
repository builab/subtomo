#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 2022 by Huy Bui, McGill University
Generate IMOD folder structure for WARP
You need to run in the main folder of the tilt series.
The script will look for the mdoc file under the regular expression enter
python create_warp_imod_input.py [tilt_series_pattern]
E.g. python create_warp_imod_input.py "FAP256*"
@author: kbui2
"""


import glob, sys
import os

if __name__=='__main__':

	pattern = sys.argv[1]
	
	mdocfiles = glob.glob(pattern + '/*.mrc.mdoc')

	for mdoc in mdocfiles:
		print(mdoc)

	
