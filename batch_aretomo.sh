#!/bin/bash

currdir=$PWD

echo $currdir

for i in TS_*/TS_[0-9][0-9][0-9].mrc
do
	ts=$(basename $i)
	tsbase=${ts%.mrc}
	folder=$(dirname $i)
	cd $folder
	echo "cd $PWD"
	echo "AreTomo -InMRC ${tsbase}.mrc -OutMRC ${tsbase}_rec.mrc -VolZ 2000 -OutBin 4 -PixelSize 3.037 -Kv 300 -Cs 2.7 -ImageDose 4 -TiltCor 1 -AlignZ 1600 -TiltRange -52 68"
	AreTomo -InMRC ${tsbase}.mrc -OutMRC ${tsbase}_rec.mrc -VolZ 2000 -OutBin 4 -PixelSize 3.037 -Kv 300 -Cs 2.7 -ImageDose 4 -TiltCor 1 -AlignZ 1600 -TiltRange -52 68
	echo "cd .."
	cd $currdir
done
