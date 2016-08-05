#!/usr/bin/env bash

cd qiandaohu_new
work_dir=`pwd`
sed -e '2c\work_dir='$work_dir paramaters.conf.temp > paramaters.conf
cd ../

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

    # 介峰部分
    cd qiandaohu_new/bin
        echo -nE "${line}" | ./main.py
    cd ../..


done
