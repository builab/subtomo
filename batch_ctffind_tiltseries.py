#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:56:14 2021

Script to run ctffind4 (version 4.1.2) on a batch of tilt series.
It is possible to use wild card to select a subset of tilt series
Usage: batch_ctffind_tiltseries.py --i TS_01/TS_01.mrc --angpix 2.12 --Cs 2.7 --voltage 300  -ctffind_exe /storage/software/ctffind4/ctffind --dmin 10000 --dmax 60000
Usage: batch_ctffind_tiltseries.py --i TS*/TS*.mrc --angpix 2.12 -ctffind_exe /storage/software/ctffind4/ctffind 

Edit other parameter inside the files
@author: Huy Bui, McGill
"""
import argparse, os


def run_ctffind(tsPath, tsName, angpix, cs, voltage, amp
  """Calculate the psi from the tangent"""
	

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Batch ctffind4 of many tilt series')
	parser.add_argument('--i', help='Input Tilt Series',required=True)
	parser.add_argument('--angpix', help='Pixel size of the tilt series',required=True)
  parser.add_argument('--ctffind_exe', help='Path to Ctffind executable',required=True)
	parser.add_argument('--cs', help='Spherical abberation',required=False, default=2.7)
	parser.add_argument('--voltage', help='Voltage of Microscope',required=False, default=300)
  parser.add_argument('--amp', help='Amplitude contrast',required=False, default=0.07)
  parser.add_argument('--tile', help='Tile',required=False, default=512)
	parser.add_argument('--dmin', help='Minimum defocus (Angstrom)',required=False,default=5000)
  parser.add_argument('--dmax', help='Maximum defocus (Angstrom)',required=False,default=60000)
  
  args = parser.parse_args()
  tsList = args.i.split(' ')
  
  currentDir = os.getcwd()
  
  for tiltseries in tsList:
    tsName = os.path.basename(tiltseries)
    tsPath = os.path()
    
    os.chdir(tsPath)


ctffind <<EOF
01.mrc
no
output.mrc
2.12
300
2.7
0.07
512
50
5
15000
60000
100
no
no
no
no
no
EOF
