#!/bin/bash

./Scripts/setup-ssl.sh 3
c_rehash Player-Data/

bits=128

###
### Dataset
###

# for SpO2 data set: copy Xdata_hist.txt and ydata_hist.txt to fs_mpc/data/

# dataset=spo2
dataset=synth_big
# dataset=gisette
# dataset=SD_without
# dataset=spambase

# main program
python ./data_prep.py $dataset
./compile.py -R $bits Programs/Source/source_file.mpc

###
### Passive 3-party computation
###

# For passive 3-party computation do this
./replicated-ring-party.x 0 source_file &
./replicated-ring-party.x 1 source_file &
./replicated-ring-party.x 2 source_file

###
### Active 3-party computation
###

# For active 3-party computation do this
#./sy-rep-ring-party.x 0 source_file &
#./sy-rep-ring-party.x 1 source_file &
#./sy-rep-ring-party.x 2 source_file