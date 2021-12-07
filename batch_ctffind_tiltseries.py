#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:56:14 2021

Script to run ctffind4 (version 4.1.2) on a batch of tilt series.
It is possible to use wild card to select a subset of tilt series
Usage: batch_ctffind_tiltseries.py --i TiltSeries --angpix 2.12 --Cs 2.7 --voltage 300  -ctffind_exe /storage/software/ctffind4/ctffind --dmin 10000 --dmax 60000

Edit other parameter inside the files
@author: Huy Bui, McGill
"""

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
