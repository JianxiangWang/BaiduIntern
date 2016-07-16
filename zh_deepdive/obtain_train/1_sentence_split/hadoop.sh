#!/bin/bash

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_sentence_split"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper "mapper.py" \
    -reducer "NONE" \
    -file "mapper.py" \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf stream.num.map.output.key.fields=7 \
    -jobconf mapred.map.tasks=1000 \
    -jobconf mapred.job.map.capacity=300 \
    -jobconf mapred.reduce.tasks=0 \
    -jobconf mapred.job.reduce.capacity=300 \
    -jobconf mapred.job.name="wangjianxiang_sentence_split"
#    -jobconf mapred.compress.map.output=true \
#    -jobconf mapred.output.compress=true \

