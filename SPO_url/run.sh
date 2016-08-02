#!/usr/bin/env bash

#[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"

while read line
do
    # 吧
    echo ${line} | ba/main.py
    # 视频
    echo ${line} | shipin/main.py
    # 图片
    echo ${line} | tuPian/main.py
    # 小说
    echo ${line} | xiaoShuo/main.py
    # 下载
    echo ${line} | xiazai/main.py
    # 音频
    echo ${line} | yinpin/main.py
done
