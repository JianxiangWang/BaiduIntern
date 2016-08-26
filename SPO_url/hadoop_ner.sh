#!/bin/bash

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/ner_examples_in"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/ner_examples_out"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/ner_reduced_tool.tar.gz#." \
    -mapper "sh -x run_qdh.sh" \
    -reducer "NONE" \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf stream.num.map.output.key.fields=2 \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.map.tasks=1 \
    -jobconf mapred.job.map.capacity=300 \
    -jobconf mapred.reduce.tasks=0 \
    -jobconf mapred.job.reduce.capacity=300 \
    -jobconf mapred.map.max.attempts=10 \
    -jobconf mapred.max.map.failures.percent="1" \
    -jobconf mapred.job.name="wangjianxiang_qdh_ner"


