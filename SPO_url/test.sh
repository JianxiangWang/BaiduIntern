#!/usr/bin/env bash

[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"
#cat $input | tee >(ba/hadoop_main.py)  | tuPian/hadoop_main.py

mkfifo pipe
cat pipe | (ba/hadoop_main.py) &
mkfifo pipe1
cat pipe1 | (xiaoShuo/hadoop_main.py) &
cat $input | tee pipe pipe1 | tuPian/hadoop_main.py