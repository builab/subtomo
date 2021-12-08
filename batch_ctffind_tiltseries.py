#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:56:14 2021

Script to run ctffind4 (version 4.1.2) on a batch of tilt series. Change the function run_cttfind according to your ctffind version
It is possible to use wild card to select a subset of tilt series
Usage: batch_ctffind_tiltseries.py --i TS_01/TS_01.mrc --angpix 2.12 --ctffind_exe /storage/software/ctffind4/ctffind --cs 2.7 --voltage 300 --amp 0.07 --minres 50 --maxres 5 --dmin 10000 --dmax 60000
Usage: batch_ctffind_tiltseries.py --i TS*/TS*.mrc --angpix 2.12 -ctffind_exe /storage/software/ctffind4/ctffind 

Edit other parameter inside the files
@author: Huy Bui, McGill
"""
import argparse, os


def run_ctffind(ctffind_exe, tsName, angpix, cs, voltage, amp, tile, minres, maxres, dmin, dmax):
	"""Run ctffind"""
	out = open('ctffind.com', 'w')
	out.write(args.ctffind_exe + ' <<EOF\n')
	out.write('{%s}\n'.format(tsName))
	out.write('no\n')
	out.write('ctffind_output.mrc\n')
	out.write('{%s}\n'.format(angpix))
	out.write('{%s}\n'.format(voltage))
	out.write('{%s}\n'.format(cs))
	out.write('{%s}\n'.format(amp))
	out.write('{%s}\n'.format(tile))
	out.write('{%s}\n'.format(minres))
	out.write('{%s}\n'.format(maxres))
	out.write('{%s}\n'.format(dmin))
	out.write('{%s}\n'.format(dmax))
	out.write('100\n')
	out.write('no\nno\nno\nno\no\nEOF\n')
	out.close()
	

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Batch ctffind4 of many tilt series')
	parser.add_argument('--i', help='Input Tilt Series',required=True)
	parser.add_argument('--angpix', help='Pixel size of the tilt series',required=True)
	parser.add_argument('--ctffind_exe', help='Path to Ctffind executable',required=True)
	parser.add_argument('--cs', help='Spherical abberation',required=False, default=2.7)
	parser.add_argument('--voltage', help='Voltage of Microscope',required=False, default=300)
	parser.add_argument('--amp', help='Amplitude contrast',required=False, default=0.07)
	parser.add_argument('--tile', help='Tile',required=False, default=512)
	parser.add_argument('--minres', help='Minimum resolution',required=False, default=30)
	parser.add_argument('--maxres', help='Maximum resolution',required=False, default=5)
	parser.add_argument('--dmin', help='Minimum defocus (Angstrom)',required=False,default=5000)
	parser.add_argument('--dmax', help='Maximum defocus (Angstrom)',required=False,default=60000)
  
	args = parser.parse_args()
	tsList = args.i.split(' ')
  
	currentDir = os.getcwd()
  
	for tiltseries in tsList:
		tsName = os.path.basename(tiltseries)
		tsPath = os.path()
		os.chdir(tsPath)
		print('Processing ' + tiltseries + ' ...')
		run_ctffind(args.ctffind_exe, tsName, args.angpix, args.cs, args.voltage, args.amp, args.tile, args.minres, args.maxres, args.dmin, args.dmax)
		os.chdir(currentDir)


