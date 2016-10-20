#!/bin/bash

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/vip_se_qdh_url_info_no_ner"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/vip_se_qdh_url_info_no_ner_domain_counter"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -file "mapper.py" \
    -file "reducer.py" \
    -mapper "mapper.py" \
    -reducer "reducer.py" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/python.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf stream.num.map.output.key.fields=1 \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.map.tasks=300 \
    -jobconf mapred.job.map.capacity=300 \
    -jobconf mapred.reduce.tasks=1 \
    -jobconf mapred.job.reduce.capacity=300 \
    -jobconf mapred.map.max.attempts=10 \
    -jobconf mapred.max.map.failures.percent="1" \
    -jobconf mapred.job.name="wangjianxiang_counter"


