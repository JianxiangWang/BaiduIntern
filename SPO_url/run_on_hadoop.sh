#!/usr/bin/env bash


while read -r line
do
    # 吧
    echo -nE "${line}" | ba/hadoop_main.py
    # 视频
    echo -nE "${line}" | shipin/hadoop_main.py
    # 图片
    echo -nE "${line}" | tuPian/hadoop_main.py
    # 小说
    echo -nE "${line}" | xiaoShuo/hadoop_main.py
    # 下载
    echo -nE "${line}" | xiazai/hadoop_main.py
    # 音频
    echo -nE "${line}" | yinpin/hadoop_main.py
done
