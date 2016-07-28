#!/usr/bin/env bash

load_train_script="/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/relations/template_label/get_train_data.py"

for model_path in models_84P/*; do
    model_name=`basename $model_path`

    echo "$model_name ..."
    cp ${load_train_script} $model_path/

    cd $model_path
    python get_train_data.py
    cd ../../

done