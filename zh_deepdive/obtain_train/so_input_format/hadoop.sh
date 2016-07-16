#!/bin/bash

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_so_recognizer_input"

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper 'mapper.py' \
    -reducer "NONE" \
    -file "train_P.txt" \
    -file "mapper.py" \
    -D mapred.job.priority="VERY_HIGH" \
    -D stream.num.map.output.key.fields=4 \
    -D mapred.reduce.tasks=0 \
    -D mapred.compress.map.output=true \
    -D mapred.output.compress=true \
    -D mapred.map.tasks=1000 \
    -D mapred.job.name="wangjianxiang_lalalala~"

