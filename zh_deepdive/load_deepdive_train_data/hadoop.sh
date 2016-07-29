#!/bin/bash

INPUT="/app/ps/spider/kg-value/lihe08/SPOMining/replace_trainData_experiment_all_trainData/jianxiang_trainData"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/deepdive_train_data_84P"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper "cat" \
    -reducer "load_deepdive_data.py" \
    -file "load_deepdive_data.py" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/tools.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf stream.num.map.output.key.fields=7 \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.job.map.capacity=1000 \
    -jobconf mapred.job.reduce.capacity=1000 \
    -jobconf mapred.map.tasks=1 \
    -jobconf mapred.reduce.tasks=1000 \
    -jobconf mapred.job.name="wangjianxiang_load_deepdive_data"





#"-jobconf mapred.output.compress=true \
