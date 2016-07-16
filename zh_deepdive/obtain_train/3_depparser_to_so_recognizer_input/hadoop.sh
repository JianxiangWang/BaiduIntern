#!/bin/bash

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_depparser"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_so_input"

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
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.map.tasks=1000 \
    -jobconf mapred.reduce.tasks=0 \
    -jobconf mapred.job.name="wangjianxiang_depparser_to_so_recognizer_input"
