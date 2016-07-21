#!/usr/bin/env bash

# 1. load data
#./load_data.py
./load_data_top_negative.py

# 2. deepdive
deepdive compile
echo ":wq"| deepdive run

# 3. evaluation
./evaluation.py