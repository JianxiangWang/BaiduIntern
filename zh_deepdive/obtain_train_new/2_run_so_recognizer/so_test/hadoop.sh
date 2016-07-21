#!/bin/bash


INPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_data_so_input"
OUTPUT="/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_data_so_84P_output"


hadoop fs -rmr ${OUTPUT}
hadoop streaming \
    -input "${INPUT}"  \
    -output "${OUTPUT}" \
    -mapper 'sh -x mapper.sh' \
    -reducer "NONE" \
    -file "mapper.sh" \
    -file "iconv.py" \
    -file "merge_sent_ner_test.py" \
    -file "mars_ner.py" \
    -file "s_prop" \
    -file "o_prop" \
    -file "buchong_s.py" \
    -cacheArchive "/app/ps/spider/kg-value/yubingyang/relation/new_module/so_recognizer/tools/Python-2.7.7.tar.gz#." \
    -cacheArchive "/app/ps/spider/kg-value/yubingyang/relation/new_module/so_recognizer/tools/test.tar.gz#." \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -jobconf stream.num.map.output.key.fields=3 \
    -jobconf num.key.fields.for.partition=3 \
    -jobconf stream.memory.limit=2000 \
    -jobconf mapred.job.priority="VERY_HIGH" \
    -jobconf mapred.map.tasks=10 \
    -jobconf mapred.job.map.capacity=300 \
    -jobconf mapred.reduce.tasks=0 \
    -jobconf mapred.job.reduce.capacity=300 \
    -jobconf mapred.textoutputformat.ignoreseparator=true \
    -jobconf mapred.compress.map.output=true \
    -jobconf mapred.output.compress=true \
    -jobconf mapred.job.name="yubingyang_so_recognizer"

#INPUT="/app/ps/spider/kg-value/yubingyang/relation/confidence/so_recog/buchong_s/merge_depparser_sorec"
##OUTPUT="/app/ps/spider/kg-value/yubingyang/relation/confidence/so_recog/buchong_s/buchong_s"
#OUTPUT="$2"
#
#${HADOOP_BIN} dfs -rmr ${OUTPUT}
#${HADOOP_BIN} streaming \
#    -input "${INPUT}"  \
#    -output "${OUTPUT}" \
#    -mapper './Python-2.7.7/bin/python buchong_s.py s_prop' \
#    -reducer "NONE" \
#    -file "buchong_s.py" \
#    -file "s_prop" \
#    -cacheArchive "/app/ps/spider/kg-value/yubingyang/relation/old_module/output/Python-2.7.7.tar.gz#." \
#    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
#    -jobconf stream.num.map.output.key.fields=2 \
#    -jobconf num.key.fields.for.partition=1 \
#    -jobconf mapred.job.priority="VERY_HIGH" \
#    -jobconf mapred.map.tasks=1 \
#    -jobconf mapred.job.map.capacity=300 \
#    -jobconf mapred.reduce.tasks=0 \
#    -jobconf mapred.job.reduce.capacity=300 \
#    -jobconf mapred.min.split.size=5000000000 \
#    -jobconf mapred.output.compress=true \
#    -jobconf mapred.textoutputformat.ignoreseparator=true \
#    -jobconf mapred.job.name="yubingyang_spo_so_recog_buchong_2"


exit $?

#    -jobconf mapred.compress.map.output=true \
#    -jobconf mapred.output.compress=true \

