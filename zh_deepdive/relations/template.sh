#!/usr/bin/env bash

TEMPLATE_DIR="$1"
DESTINATION_DIR="$2"


# cp
cp -r ${TEMPLATE_DIR} ${DESTINATION_DIR}

# input
cd ${DESTINATION_DIR}/input
rm -rf sentences.tsv
ln -s /home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_for_deepdive sentences.tsv

# udf
cd ${DESTINATION_DIR}/udf
chmod +x *.py

# run
rm -rf ${DESTINATION_DIR}/run