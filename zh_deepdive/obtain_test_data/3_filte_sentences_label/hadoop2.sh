#!/bin/bash

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_test_data_so_output"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_test_data_for_deepdive_label2"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper "mapper3.py" \
    -reducer "NONE" \
    -file "mapper3.py" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/tools.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf stream.num.map.output.key.fields=9 \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.map.tasks=1000 \
    -jobconf mapred.job.map.capacity=400 \
    -jobconf mapred.reduce.tasks=0 \
    -jobconf mapred.job.reduce.capacity=400 \
    -jobconf mapred.job.name="wangjianxiang_sentence_filter_label"





#"-jobconf mapred.output.compress=true \
