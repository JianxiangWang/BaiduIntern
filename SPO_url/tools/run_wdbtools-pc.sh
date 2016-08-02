#!/usr/bin/env bash

INPUT=${1}

CWD=/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/tools

${CWD}/classify2readable `${CWD}/wdbtools-pc/getone.sh ${INPUT} PageClassify realtime | grep -a "^PageClassify" | awk '{print $NF}'` | python ${CWD}/wdb_to_list.py