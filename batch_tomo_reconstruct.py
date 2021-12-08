#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Dec 8 2021
Script to run batch imod through the command line
Only use for newst & tilt & tilt_sirt for now

@author: Huy Bui, McGill
"""
if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Batch ctffind4 of many tilt series')
	parser.add_argument('--i', help='Input Tilt Series',required=True)
	parser.add_argument('--angpix', help='Pixel size of the tilt series',required=True)
	parser.add_argument('--ctffind_exe', help='Path to Ctffind executable',required=True)
