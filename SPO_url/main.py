#!python/bin/python
#  encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from jiefeng.PageClassify import PageClassify
from ba.hadoop_main import do_extraction as ba_extraction
from shipin.hadoop_main import do_extraction as shipin_extraction
from tuPian.hadoop_main import do_extraction as tuPian_extraction
from xiaoShuo.hadoop_main import do_extraction as xiaoShuo_extraction
from xiazai.hadoop_main import do_extraction as xiazai_extraction
from yinpin.hadoop_main import do_extraction as yinpin_extraction

# mine
extractions = [
    ba_extraction,
    shipin_extraction,
    tuPian_extraction,
    xiaoShuo_extraction,
    xiazai_extraction,
    yinpin_extraction
]

# 介峰部分
p = PageClassify('prepared')


for line in sys.stdin:
    line_list = line.strip().split("\t")
    url = line_list[0]
    dict_info = json.loads(line_list[-1])

    # go go go!
    for extraction in extractions:
        extraction(url, dict_info)

    # 介峰部分
    p.predict(line.strip())


