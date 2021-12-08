#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8, 2021

All .mrc & mrc.mdoc file should be in 1 folder
Move .mrc file into folders

@author: Huy Bui, McGill
"""
import argparse, os, glob

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Organize tilt series into folders')
	parser.add_argument('--i', help='Input Tilt Series Wild Card',required=True)
	
	args = parser.parse_args()
	tsList = glob.glob(args.i)
	for tiltseries in tsList:
		if not tiltseries.endswith('.mrc'):
			print('Processing ' + tiltseries + ': ERROR! Only mrc file supported')
			break
		tsName = tiltseries.replace('.mrc', '')
		mrcDoc = tiltseries.replace('.mrc', '.mrc.mdoc')
		os.mkdir(tsName)
		# Move tilt series
		print('mv ' + tiltseries + ' ' + os.path.join(tsName, tiltseries))
		shutil.move(tiltseries, os.path.join(tsName, tiltseries))\
		print('mv ' + mrcDoc + ' ' + os.path.join(tsName, mrcDoc))
		shutil.move(mrcDoc, os.path.join(tsName, mrcDoc))



