#!/usr/bin/env bash


#[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"
#
#cat $input | ba/hadoop_main.py
#cat $input | shipin/hadoop_main.py
#cat $input | tuPian/hadoop_main.py
#cat $input | xiaoShuo/hadoop_main.py
#cat $input | xiazai/hadoop_main.py
#cat $input | yinpin/hadoop_main.py

while read line
do
#    echo ${line}
    # 吧
    echo -E "${line}" | ba/hadoop_main.py
#    # 视频
#    echo ${line} | shipin/hadoop_main.py
#    # 图片
#    echo ${line} | tuPian/hadoop_main.py
#    # 小说
#    echo ${line} | xiaoShuo/hadoop_main.py
#    # 下载
#    echo ${line} | xiazai/hadoop_main.py
#    # 音频
#    echo ${line} | yinpin/hadoop_main.py
##    # 介峰部分
##    cd
##        ...
##    cd
#
done
