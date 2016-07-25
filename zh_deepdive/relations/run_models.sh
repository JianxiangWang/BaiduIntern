#!/usr/bin/env bash

log_file="/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/relations/run.log"
rm ${log_file}

for model_path in models_84P/*; do
    model_name=`basename $model_path`
    cd $model_path

    echo "=====================================" >> ${log_file}
    curr_time=$(date +"%Y-%m-%d %T")
    echo "$curr_time $model_name is running..." >> ${log_file}

    sh -x run.sh

    curr_time=$(date +"%Y-%m-%d %T")
    echo "$curr_time $model_name finished..." >> ${log_file}

    cd ../../
done
