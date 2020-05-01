#!/bin/bash
conda env create -f environment.yml
conda activate message-passing-nn
#export PYTHONPATH=path/to/message-passing-nn/
. grid-search-parameters.sh
python message_passing_nn/cli.py grid-search