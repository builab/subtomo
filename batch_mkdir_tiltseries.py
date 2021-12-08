#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8, 2021

@author: Huy Bui, McGill
"""
import argparse, os, glob

if __name__=='__main__':
 parser = argparse.ArgumentParser(description='Batch ctffind4 of many tilt series')
	parser.add_argument('--i', help='Input Tilt Series',required=True)
