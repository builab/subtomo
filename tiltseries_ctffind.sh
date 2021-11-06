#!/bin/bash
# Usage: bash tiltseries_ctffind.sh tilt_series_file pixel_size
# Example: bash tiltseries_ctffind.sh TS_01.mrc 2.12
# The output is TS_01_output.txt
# Not yet perfect replacement inside the CTF output file

tomo=$1
pixelsize=$2

newstack -split 1 -append mrc $tomo  temp_ 

tomo=${tomo/.mrc}

rm ${tomo}_output_test.txt

for micro in temp_*.mrc
do

view=${micro/.mrc}
view=${view#temp_}

ctffind<<EOF
$micro
${view}_output.mrc
$pixelsize
300
2.7
0.07
512
30
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

# Replace the first number to view number
sed -i "s/^1/$view/g" ${view}_output.txt

# Write to the output
grep -v '#' ${view}_output.txt >> ${tomo}_output_test.txt

done;

rm temp_*.mrc
