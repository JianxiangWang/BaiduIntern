#!/usr/bin/env bash


INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_for_deepdive"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_for_deepdive_merged"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper cat \
    -reducer cat \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf stream.num.map.output.key.fields=8 \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.map.tasks=1000 \
    -jobconf mapred.job.map.capacity=300 \
    -jobconf mapred.reduce.tasks=1 \
    -jobconf mapred.job.reduce.capacity=300 \
    -jobconf mapred.job.name="wangjianxiang_merge"
