#!/bin/bash


INPUT="/app/ps/spider/wdm-site-offline/relation-extraction/dom_extraction/qiandaohu2"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/qiandaohu_urls"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper "mapper.py" \
    -reducer "reducer.py" \
    -file "mapper.py" \
    -file "reducer.py" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/python.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.map.tasks=300 \
    -jobconf mapred.job.map.capacity=400 \
    -jobconf mapred.reduce.tasks=100 \
    -jobconf mapred.job.reduce.capacity=400 \
    -jobconf mapred.job.name="wangjianxiang_qdh_urls"

#    -file "main.py" \

