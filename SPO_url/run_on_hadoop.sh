#!/usr/bin/env bash


while read -r line
do
#    echo ${line}
    # 吧
    echo -E "${line}" | ba/hadoop_main.py
    # 视频
    echo -E ${line} | shipin/hadoop_main.py
    # 图片
    echo -E ${line} | tuPian/hadoop_main.py
    # 小说
    echo -E ${line} | xiaoShuo/hadoop_main.py
    # 下载
    echo -E ${line} | xiazai/hadoop_main.py
    # 音频
    echo -E ${line} | yinpin/hadoop_main.py
##    # 介峰部分
##    cd
##        ...
##    cd
#
done
