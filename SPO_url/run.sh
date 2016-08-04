#!/usr/bin/env bash

#[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"

cd qiandaohu
work_dir=`pwd`
sed -e '2c\work_dir='$work_dir paramaters.conf.temp > paramaters.conf
cd ../

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

    # 介峰部分
    cd qiandaohu/bin
    echo ${line} | ./main.py
    cd ../..

done
