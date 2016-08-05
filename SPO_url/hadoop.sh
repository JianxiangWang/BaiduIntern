#!/bin/bash

# 先打包, 上传至 hadoop ...
tar zcvf qdh.tar.gz ba shipin tuPian xiaoShuo xiazai yinpin qiandaohu_hadoop
hadoop fs -rm /app/ps/spider/kg-value/wangjianxiang01/qdh.tar.gz
hadoop fs -put qdh.tar.gz /app/ps/spider/kg-value/wangjianxiang01/

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_url/test_urls_in"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_url/test_urls_output"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper "run_on_hadoop.sh" \
    -reducer "NONE" \
    -file "run.sh" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/python.tar.gz#." \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/qdh.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf stream.num.map.output.key.fields=4 \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.map.tasks=2 \
    -jobconf mapred.job.map.capacity=400 \
    -jobconf mapred.reduce.tasks=0 \
    -jobconf mapred.job.reduce.capacity=400 \
    -jobconf mapred.job.name="wangjianxiang_sentence_filter"


#"-jobconf mapred.output.compress=true \
