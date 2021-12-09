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
from multiprocessing import Pool


def run_newst(baseName, tempCont):
	'''Write newst and run'''
	outCom = open(operation + '.com', 'w')
	for line in tempCont:
		if line.startswith('InputFile'):
			outCom.write('InputFile\t{:s}.mrc\n'.format(baseName))
		elif line.startswith('OutputFile'):
			outCom.write('OutputFile\t{:s}_ali.mrc\n'.format(baseName))
		elif line.startswith('TransformFile'):
			outCom.write('TransformFile\t{:s}.xf\n'.format(baseName))
		#elif line.startswith('BinByFactor'):
		#	outCom.write('BinByFactor\t{:d}.xf\n'.format(binFactor)
		else:
			outCom.write(line)
	outCom.close()
				     
				     
def run_tilt(baseName, tempCont):
	outCom = open('tilt.com', 'w')	
				     
	for line in tempCont:
		if line.startswith('InputProjections'):
			outCom.write('InputProjections\t{:s}_ali.mrc\n'.format(baseName))
		elif line.startswith('OutputFile'):
			outCom.write('OutputFile\t{:s}_full_rec.mrc\n'.format(baseName))
		elif line.startswith('TILTFILE'):
			outCom.write('TILTFILE\t{:s}.tlt\n'.format(baseName))
		#elif line.startswith('THICKNESS'):
		#	outCom.write('THICKNESS\t{:s}\n'.format(thickness)
		elif line.startswith('XTILTFILE'):
			outCom.write('XTILFILE\t{:s}.xtilt\n'.format(baseName))
		else:
			outCom.write(line)
	outCom.close()		
		
def run_newst_3dfind(baseName, tempCont):
	outCom = open('newst_3dfind.com', 'w')	
				     
	for line in tempCont:
		if line.startswith('InputFile'):
			outCom.write('InputFile\t{:s}_3dfind_rec.mrc\n'.format(baseName))
		elif line.startswith('OutputFile'):
			outCom.write('OutputFile\t{:s}_3dfind.mod\n'.format(baseName))
		elif line.startswith('TransformFile'):
			outCom.write('TransformFile\t{:s}.xf\n'.format(baseName))
		else:
			outCom.write(line)
	outCom.close()	
				     
def run_tilt_3dfind(baseName, tempCont):
	outCom = open('tilt_3dfind.com', 'w')	
				     
	for line in tempCont:
		if line.startswith('InputProjections'):
			outCom.write('InputProjections\t{:s}_3dfind_ali.mrc\n'.format(baseName))
		elif line.startswith('OutputFile'):
			outCom.write('OutputFile\t{:s}_3dfind_rec.mrc\n'.format(baseName))
		elif line.startswith('TILTFILE'):
			outCom.write('TILTFILE\t{:s}.tlt\n'.format(baseName))
		#elif line.startswith('THICKNESS'):
		#	outCom.write('THICKNESS\t{:s}\n'.format(thickness)
		elif line.startswith('XTILTFILE'):
			outCom.write('XTILFILE\t{:s}.xtilt\n'.format(baseName))
		else:
			outCom.write(line)
	outCom.close()		     
				    
def run_findbead3d(baseName, tempCont):
	outCom = open('findbeads3d.com', 'w')	
				     
	for line in tempCont:
		if line.startswith('InputFile'):
			outCom.write('InputFile\t{:s}.mrc\n'.format(baseName))
		elif line.startswith('OutputFile'):
			outCom.write('OutputFile\t{:s}_3dfind_ali.mrc\n'.format(baseName))
		else:
			outCom.write(line)
	outCom.close()	

def run_tilt_3dfind_reproject(baseName, tempCont):
	outCom = open('tilt_3dfind_reproject.com', 'w')	
				     
	for line in tempCont:
		if line.startswith('InputFile'):
			outCom.write('InputFile\t{:s}_3dfind_ali.mrc\n'.format(baseName))
		elif line.startswith('OutputFile'):
			outCom.write('OutputFile\t{:s}_erase.fid\n'.format(baseName))
		elif line.startswith('TILTFILE'):
			outCom.write('TILTFILE\t{:s}.tlt\n'.format(baseName))
		elif line.startswith('ProjectModel'):
			outCom.write('ProjectModel\t{:s}_3dfind.mod\n'.format(baseName))
		else:
			outCom.write(line)
	outCom.close()	
				     
def run_golderaser(baseName, tempCont):
	outCom = open('golderaser.com', 'w')	
				     
	for line in tempCont:
		if line.startswith('InputFile'):
			outCom.write('InputFile\t{:s}_ali.mrc\n'.format(baseName))
		elif line.startswith('OutputFile'):
			outCom.write('OutputFile\t{:s}_erase_ali.mrc\n'.format(baseName))
		elif line.startswith('ModelFile'):
			outCom.write('ModelFile\t{:s}_erase.fid\n'.format(baseName))			     
		else:
			outCom.write(line)
	outCom.close()
				     
def run_trimvol(baseName, tempCont):
	outCom = open('golderaser.com', 'w')
	outCom.write('$trimvol -f -rx {:s}_full_rec.mrc {:s}_rec.mrc'.format(baseName, baseName))
	outCom.close()
  	

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Batch tomo reconstruct using IMOD')
	parser.add_argument('--i', help='Input Tilt Series',required=True)
	parser.add_argument('--operation', help='Imod operation (newst/tilt/newst_3dfind/tilt_3dfind/findbeads3d/tilt_3dfind_reproject/golderaser/trimvol)',required=True)
	#parser.add_argument('--bin', help='Bin factor',required=True)			     
	parser.add_argument('--template', help='Template file from 1 reconstruction',required=True)
	parser.add_argument('--noproc', help='Number of processors',required=False, default=1)

	#parser.add_argument('--xsize', help='X size of image',required=True)	
	#parser.add_argument('--ysize', help='Y size of image',required=True)			     
	
	print('Only tested with IMOD 4.9 and 4.11.8 only')
	
	args = parser.parse_args()
	     	
	tempfile = open(args.template, 'r')
	tempCont = tempfile.readlines()
	operation = args.operation
	
	currentDir = os.getcwd()

	tsList = glob.glob(args.i)
	for tiltseries in tsList:
		tsName = os.path.basename(tiltseries)
		if not tiltseries.endswith('.mrc'):
			print('Processing ' + tiltseries + ': ERROR! Only mrc file supported')
			break
		baseName = tsName.replace('.mrc','')
		tsPath = os.path.dirname(tiltseries)
		print('Change dir to ' + tsPath)
		os.chdir(tsPath)
		print('Processing ' + tiltseries + ' ...')
		if operation == 'newst':
			run_newst(baseName, tempCont)
			system('submfg newst.com')
		elif operation == 'tilt':
			run_tilt(baseName, tempCont)
			system('submfg tilt.com')
		if operation == 'newst_3dfind':
			run_newst_3dfind(baseName, tempCont)
			system('submfg newst_3dfind.com')
		elif operation == 'tilt_3dfind':
			run_tilt_3dfind(baseName, tempCont)
			system('submfg tilt_3dfind.com')
		if operation == 'newst_3dfind':
			run_findbeads3d(baseName, tempCont)
			system('submfg findbeads3d.com')
		elif operation == 'tilt_3dfind_reproject':
			run_tilt_3dfind_reproject(baseName, tempCont)
			system('submfg tilt_3dfind_reproject.com')
		elif operation == 'golderaser':
			run_tilt_3dfind_reproject(baseName, tempCont)
			system('submfg golderaser.com')
		elif operation == 'trimvol':
			run_trimvol(baseName, tempCont)
			system('submfg trimvol.com')
		else:
			print('Unknown option')
			exit(1)
		os.chdir(currentDir)
