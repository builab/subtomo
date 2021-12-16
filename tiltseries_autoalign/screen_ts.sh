#!/bin/bash
# Script used for screening quickly that tomo is from -60 to +60

for i in TS*/*.mrc;
do
	# Removing the ending .mrc from i
	basename=${i/.mrc}
        echo "newstack -input $i -output ${basename}_0.jpeg -format jpeg -secs 0 -mode 0 -float 2 -bin 8";
        echo "newstack -input $i -output ${basename}_1.jpeg -format jpeg -secs 20 -mode 0 -float 2 -bin 8";
        echo "newstack -input $i -output ${basename}_2.jpeg -format jpeg -secs 40 -mode 0 -float 2 -bin 8";
done
