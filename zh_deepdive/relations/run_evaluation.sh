#!/usr/bin/env bash

evaluation_script="/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/relations/template_label/evaluation.py"

for model_path in models_84P/*; do
    model_name=`basename $model_path`

    echo "$model_name ..."
    cp ${evaluation_script} $model_path/

    cd $model_path
    python evaluation.py
    cd ../../

done