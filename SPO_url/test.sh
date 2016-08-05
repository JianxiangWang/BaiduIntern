#!/usr/bin/env bash

[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"
#cat $input | tee >(ba/hadoop_main.py)  | tuPian/hadoop_main.py

mkfifo pipe1 pipe2 pipe3 pipe4 pipe5

cat pipe1 | (ba/hadoop_main.py) &
cat pipe2 | (shipin/hadoop_main.py) &
cat pipe3 | (tuPian/hadoop_main.py) &
cat pipe4 | (xiaoShuo/hadoop_main.py) &
cat pipe5 | (xiazai/hadoop_main.py) &
cat pipe6 | (python qiandaohu_hadoop/bin/main.py) &

cat $input | tee pipe1 pipe2 pipe3 pipe4 pipe5 pipe6| yinpin/hadoop_main.py

