#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Dec 8 2021
Script to run batch imod through the command line
Only use for newst & tilt & tilt_sirt for now

Not done yet.

This is used specifically for K3 in McGill.

@author: Huy Bui, McGill
"""

import argparse, os

def runNewst(tsStack, binFactor
	'''Write newst and run'''

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Batch tomo reconstruct using IMOD')
	parser.add_argument('--i', help='Input Tilt Series',required=True)
	parser.add_argument('--operation', help='Imod operation (newst or tilt or tilt_sirt)',required=True)
	parser.add_argument('--bin', help='Bin factor',required=True)
	
	
	print('Tested with IMOD 4.9 only')
	
	args = parser.parse()
	     
	binFactor = float(args.bin)
