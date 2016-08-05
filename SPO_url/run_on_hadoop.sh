#!/usr/bin/env bash


while read -r line
do
#    echo ${line}
    # 吧
    echo -E "${line}" | ba/hadoop_main.py
    # 视频
#
done
