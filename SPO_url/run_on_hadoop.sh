#!/usr/bin/env bash


while read line
do
    # 吧
    cat ${line} | ba/hadoop_main.py

done
