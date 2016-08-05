#!/usr/bin/env bash

[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"
cat $input | tee >(ba/hadoop_main.py)  | tuPian/hadoop_main.py
