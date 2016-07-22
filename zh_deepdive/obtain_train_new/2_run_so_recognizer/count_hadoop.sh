#!/bin/bash


INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_data_so_84P_output"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_data_so_84P_output_count"

hadoop fs -rmr ${OUTPUT}
hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper 'count_mapper.py' \
    -reducer "count_reducer.py" \
    -file "count_mapper.py" \
    -file "count_reducer.py" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/tools.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.map.tasks=1000 \
    -jobconf mapred.job.map.capacity=400 \
    -jobconf mapred.reduce.tasks=100 \
    -jobconf mapred.job.reduce.capacity=400 \
    -jobconf mapred.job.name="wangjianxiang_sentence_filter_label"


exit $?


