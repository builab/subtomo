#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Dec 8 2021
Script to run batch imod through the command line
Only use for newst & tilt & tilt_sirt for now


This is used specifically for K3 in McGill. Imod 4.11.8

@author: Huy Bui, McGill
"""

import argparse, os, glob

def run_com(operation, tsName, tempCont)
	'''Write newst and run'''
	outCom = open('newst.com', 'w')
	while outCom:
		
	
	

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Batch tomo reconstruct using IMOD')
	parser.add_argument('--i', help='Input Tilt Series',required=True)
	parser.add_argument('--operation', help='Imod operation (newst or tilt or tilt_sirt)',required=True)
	parser.add_argument('--bin', help='Bin factor',required=True)
	parser.add_argument('--template', help='Template file from 1 reconstruction',required=True)
	
	print('Only tested with IMOD 4.9 and 4.11.8 only')
	
	args = parser.parse()
	     
	binFactor = float(args.bin)
	
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
