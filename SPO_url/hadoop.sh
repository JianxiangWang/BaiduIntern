#!/bin/bash

# 先打包, 上传至 hadoop ...
tar zcf qdh.tar.gz ba shipin tuPian xiaoShuo xiazai yinpin jiefeng main.py
hadoop fs -rm /app/ps/spider/kg-value/wangjianxiang01/qdh.tar.gz
hadoop fs -put qdh.tar.gz /app/ps/spider/kg-value/wangjianxiang01/

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_url/test_urls_in"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_url/test_urls_output"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper "main.py" \
    -reducer "NONE" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/qdh.tar.gz#." \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/python.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf stream.num.map.output.key.fields=4 \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.map.tasks=300 \
    -jobconf mapred.job.map.capacity=400 \
    -jobconf mapred.reduce.tasks=0 \
    -jobconf mapred.job.reduce.capacity=400 \
    -jobconf mapred.job.name="wangjianxiang_qdh"

#    -file "main.py" \

