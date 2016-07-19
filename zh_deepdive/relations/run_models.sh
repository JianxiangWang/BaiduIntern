#!/usr/bin/env bash

log_file="/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/relations/run.log"
rm ${log_file}

for model_path in models/*; do
    model_name=`basename $model_path`
    cd $model_path
    echo "$model_name is running..." >> ${log_file}
    sh -x run.sh
    echo "$model_name finished..." >> ${log_file}
    cd ../../
done
