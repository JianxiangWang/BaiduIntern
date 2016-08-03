#!/bin/bash

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/test_new_sents_data_depparser"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/test_new_sents_data_so_input"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper "mapper.py" \
    -reducer "NONE" \
    -file "mapper.py" \
    -file "train_P.txt" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/tools.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf stream.num.map.output.key.fields=6 \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.map.tasks=1 \
    -jobconf mapred.job.map.capacity=300 \
    -jobconf mapred.reduce.tasks=0 \
    -jobconf mapred.job.reduce.capacity=300 \
    -jobconf mapred.job.name="wangjianxiang_1_format_to_so_recognizer_input"


#"-jobconf mapred.output.compress=true \
