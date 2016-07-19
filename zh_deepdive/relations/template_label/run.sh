#!/usr/bin/env bash

# 1. load data
./load_data.py

# 2. deepdive
deepdive compile && deepdive run

# 3. evaluation
./evaluation.py