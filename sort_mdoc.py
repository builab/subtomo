#!/usr/bin/python
# # -*- coding: utf-8 -*-

# require mdocfile from Alister Burt
# pip install mdocfile

# 2023/08/24, Huy Bui
# Note: if your mdoc file has more entry, you need to put in similarly in the current section

import sys
import mdocfile
from pathlib import Path
from mdocfile.data_models import Mdoc, MdocGlobalData, MdocSectionData


inputmdoc = sys.argv[1]

df = mdocfile.read(inputmdoc)

df2 = df.sort_values('TiltAngle', ignore_index=True)

df2['ZValue'] = df2.index

outputmdoc = inputmdoc.replace(".mdoc", "_sorted.mdoc")

print(f'Writing {outputmdoc}')

global_data = MdocGlobalData (
	DataMode = df2['DataMode'].iloc[0],
	ImageSize = df2['ImageSize'].iloc[0],
	PixelSpacing = df2['PixelSpacing'].iloc[0],
	Voltage = df2['Voltage'].iloc[0]
)


mdoc = Mdoc(
    titles=df2['titles'].iloc[0],
    global_data=global_data,
    section_data=[	]
)

for ind in df2.index:
	current_section = MdocSectionData(
    	ZValue=df2['ZValue'].iloc[ind],
   		TiltAngle=df2['TiltAngle'].iloc[ind],
    	StagePosition=df2['StagePosition'].iloc[ind],
    	ExposureDose=df2['ExposureDose'].iloc[ind],
    	SubFramePath=df2['SubFramePath'].iloc[ind],
    	DateTime=df2['DateTime'].iloc[ind],
    	NumSubFrames=df2['NumSubFrames'].iloc[ind],
	)
	mdoc.section_data.append(current_section)

with open(outputmdoc, mode='w+') as file:
	file.write(mdoc.to_string())


