#!/bin/bash

INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_data_so_84P_output"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_data_84P_for_deepdive_label_lihe"

hadoop fs -rmr ${OUTPUT}

hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper "mapper_lihe.py" \
    -reducer "NONE" \
    -file "mapper_lihe.py" \
    -file "P_similar" \
    -file "guide_words_for_84P.cPkl" \
    -file "seed_train_for_84P.cPkl" \
    -file "test_so_set_for_84P.cPkl" \
    -cacheArchive "/app/ps/spider/kg-value/wangjianxiang01/tools.tar.gz#." \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf stream.num.map.output.key.fields=10 \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.job.map.capacity=1000 \
    -jobconf mapred.job.reduce.capacity=1000 \
    -jobconf mapred.map.tasks=3000 \
    -jobconf mapred.reduce.tasks=0 \
    -jobconf mapred.job.name="wangjianxiang_sentence_filter_label"





#"-jobconf mapred.output.compress=true \
