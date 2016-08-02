#!/bin/bash
#INPUT_FORMAT:
#sentence, url, publish_time, link_found_time, depparser_result, domain_p_list

#if [[ $# -ne 1 ]];then
#    echo "Usage: $0 input_file_url"
#    exit -1
#fi
#input_file="$1"
local_temp_dir="yubingyang"
mkdir ${local_temp_dir}
local_file="${local_temp_dir}/tmp"
#ftp数据存到本地
#wget ${input_file} -O ${local_file}
cat - >${local_file}
cat ${local_file} | cut -f 1 | ./Python-2.7.7/bin/python iconv.py utf8 gb18030 >${local_temp_dir}/tmp2
#基础ner识别
./test/testwordner -f ${local_temp_dir}/tmp2 -d ./test/worddict/ -n ./test/nerdict -l 1 -t 1 >${local_temp_dir}/tmp3
cat ${local_temp_dir}/tmp3 | ./Python-2.7.7/bin/python iconv.py gb18030 utf8 >${local_temp_dir}/tmp4
#awk 'BEGIN{FS="\t";OFS="\t"}{if(ARGIND==1){dict[FNR]=$1}else{if(FNR in dict){print dict[FNR],$0}else{print "line not match" >> "/dev/stderr"}}}' ${local_temp_dir}/tmp ${local_temp_dir}/tmp4 >${local_temp_dir}/tmp5
#python merge_sent_ner_test.py ${local_temp_dir}/tmp5 ${local_temp_dir}/tmp >${local_temp_dir}/tmp6
#合并ner结果
./Python-2.7.7/bin/python merge_sent_ner_test.py ${local_temp_dir}/tmp4 ${local_file} >${local_temp_dir}/tmp5
#统一进行ner决策
cat ${local_temp_dir}/tmp5 | ./Python-2.7.7/bin/python mars_ner.py >${local_temp_dir}/tmp6
cat ${local_temp_dir}/tmp6 | ./Python-2.7.7/bin/python buchong_s.py s_prop

