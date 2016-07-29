#!/bin/bash

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_data_so_84P_output"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/deepdive_train_data_84P"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper "load_deepdive_data.py" \
    -reducer "NONE" \
    -file "load_deepdive_data.py" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/tools.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf stream.num.map.output.key.fields=7 \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.job.map.capacity=1000 \
    -jobconf mapred.job.reduce.capacity=1000 \
    -jobconf mapred.map.tasks=300 \
    -jobconf mapred.reduce.tasks=0 \
    -jobconf mapred.job.name="wangjianxiang_load_deepdive_data"





#"-jobconf mapred.output.compress=true \
