#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Dec 8 2021
Script to run batch imod through the command line
Only use for newst & tilt & tilt_sirt for now
For now, use a default template but should be flexible in the future for generating different bin tomo

This is used specifically for K3 in McGill. Imod 4.11.8

@author: Huy Bui, McGill
"""

import argparse, os, glob

def run_newst(operation, tsName, tempCont):
	'''Write newst and run'''
	outCom = open(operation + '.com', 'w')
	baseName = tsName.replace('.mrc','')
	for line in tempCont:
		if line.startswith('InputFile'):
			outCom.write('InputFile\t{:s}.mrc\n'.format(baseName)
		elif line.startswith('OutputFile'):
			outCom.write('OutputFile\t{:s}_ali.mrc\n'.format(baseName)
		elif line.startswith('TransformFile'):
			outCom.write('TransformFile\t{:s}.xf\n'.format(baseName)
		#elif line.startswith('BinByFactor'):
		#	outCom.write('BinByFactor\t{:d}.xf\n'.format(binFactor)
		else:
			outCom.write(line)
	outCom.close()
				     
				     
def run_tilt(operation, tsName, tempCont):
	outCom = open('tilt.com', 'w')	
	baseName = tsName.replace('.mrc','')
				     
	for line in tempCont:
		if line.startswith('InputProjections'):
			outCom.write('InputProjections\t{:s}_ali.mrc\n'.format(baseName)
		elif line.startswith('OutputFile'):
			outCom.write('OutputFile\t{:s}_full_rec.mrc\n'.format(baseName)
		elif line.startswith('TILTFILE'):
			outCom.write('TILTFILE\t{:s}.tlt\n'.format(baseName)
		#elif line.startswith('THICKNESS'):
		#	outCom.write('THICKNESS\t{:s}\n'.format(thickness)
		elif line.startswith('XTILTFILE'):
			outCom.write('XTILFILE\t{:s}.xtilt\n'.format(baseName)
		else:
			outCom.write(line)
	outCom.close()		
		
	
	

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Batch tomo reconstruct using IMOD')
	parser.add_argument('--i', help='Input Tilt Series',required=True)
	parser.add_argument('--operation', help='Imod operation (newst or tilt or tilt_sirt)',required=True)
	parser.add_argument('--bin', help='Bin factor',required=True)			     
	parser.add_argument('--template', help='Template file from 1 reconstruction',required=True)
	#parser.add_argument('--xsize', help='X size of image',required=True)	
	#parser.add_argument('--ysize', help='Y size of image',required=True)			     
	
	print('Only tested with IMOD 4.9 and 4.11.8 only')
	
	args = parser.parse()
	     
	binFactor = int(args.bin)
	
	tempfile = open(args.template, 'r')
	tempCont = tempfile.readlines()
	
	currentDir = os.getcwd()

	tsList = glob.glob(args.i)
	for tiltseries in tsList:
		tsName = os.path.basename(tiltseries)
		if not tiltseries.endswith('.mrc'):
			print('Processing ' + tiltseries + ': ERROR! Only mrc file supported')
			break
		tsPath = os.path.dirname(tiltseries)
		print('Change dir to ' + tsPath)
		os.chdir(tsPath)
		print('Processing ' + tiltseries + ' ...')
		run_newst(tsName, tempCont)
		os.chdir(currentDir)
