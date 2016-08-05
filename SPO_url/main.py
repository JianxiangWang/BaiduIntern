#!python/bin/python

import json
import sys
from ba.hadoop_main import do_extraction as ba_extraction
from shipin.hadoop_main import do_extraction as shipin_extraction
from tuPian.hadoop_main import do_extraction as tuPian_extraction
from xiaoShuo.hadoop_main import do_extraction as xiaoShuo_extraction
from xiazai.hadoop_main import do_extraction as xiazai_extraction
from yinpin.hadoop_main import do_extraction as yinpin_extraction

#
extractions = [
    ba_extraction,
    shipin_extraction,
    tuPian_extraction,
    xiaoShuo_extraction,
    xiazai_extraction,
    yinpin_extraction
]

for line in sys.stdin:
    line_list = line.strip().split("\t")
    url = line_list[0]
    dict_info = json.loads(line_list[-1])

    # go go go!
    for extraction in extractions:
        extraction(url, dict_info)


