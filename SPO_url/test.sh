#!/usr/bin/env bash

[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"
#cat $input | tee >(ba/hadoop_main.py)  | tuPian/hadoop_main.py

mkfifo pipe pipe1 pipe2 pipe3 pipe4 pipe5

cat pipe0 | (ba/hadoop_main.py) &
cat pipe1 | (shipin/hadoop_main.py) &
cat pipe2 | (tuPian/hadoop_main.py) &
cat pipe3 | (xiaoShuo/hadoop_main.py) &
cat pipe4 | (xiazai/hadoop_main.py) &

cat $input | tee pipe0 pipe1 pipe2 pipe3 pipe4 | yinpin/hadoop_main.py