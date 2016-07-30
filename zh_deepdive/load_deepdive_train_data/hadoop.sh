#!/bin/bash

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_data_84P_for_deepdive_label_lihe_tagged"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_data_84P_for_deepdive_label_lihe_formatted"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper "cat" \
    -reducer "mapper.py" \
    -file "mapper.py" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/tools.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf stream.num.map.output.key.fields=10 \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.job.map.capacity=1000 \
    -jobconf mapred.job.reduce.capacity=1000 \
    -jobconf mapred.map.tasks=10 \
    -jobconf mapred.reduce.tasks=1000 \
    -jobconf mapred.job.name="wangjianxiang_load_deepdive_data"





#"-jobconf mapred.output.compress=true \
