#!/bin/bash
# Script used for copying the ctffind to each tilt series folder
# The assumption that the warp_ctf folder is the same level as each tilt series

for i in *_output.txt;
do
	# Removing the ending .mrc from i
	tsdir=${i/_output.txt}
    echo "cp ${i} ../${base_name}";
    cp ${i} ../${base_name}
done
