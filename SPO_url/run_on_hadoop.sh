#!/usr/bin/env bash


[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"

#cat $input | ba/hadoop_main.py
cat $input | shipin/hadoop_main.py
cat $input | tuPian/hadoop_main.py
cat $input | xiaoShuo/hadoop_main.py
cat $input | xiazai/hadoop_main.py
cat $input | yinpin/hadoop_main.py

