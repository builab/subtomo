# Scripts used for subtomogram averaging

## Convert Axoneme Align Project To Input Relion 4 Star File

#### convert_dmt_aa2relion4.py --i list_doublet_ida_v1.txt --ostar input.star --angpix pixelSize --bin binFactor

The script will read the doc and star files noted in the list to convert to relion.

The output star file can be used as the input for Relion 4.0

NOTE: This script still doesn't convert the shift.

e.g. convert_dmt_aa2relion4.py --i list_doublet_ida_v1.txt --ostar input.star --angpix 8.48 --bin 4
