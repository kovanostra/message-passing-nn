#!/bin/bash

export CUDA_HOME=/usr/local/cuda
export MACOSX_DEPLOYMENT_TARGET=10.11
export CC=clang
export CXX=clang++
python setup.py install
