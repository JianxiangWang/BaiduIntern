#!python/bin/python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import json
from ba.hadoop_main import do_extraction as ba_extraction
from shipin.hadoop_main import do_extraction as shipin_extraction
from tuPian.hadoop_main import do_extraction as tuPian_extraction
from xiaoShuo.hadoop_main import do_extraction as xiaoShuo_extraction
from xiazai.hadoop_main import do_extraction as xiazai_extraction
from yinpin.hadoop_main import do_extraction as yinpin_extraction
from jiefeng.PageClassify import PageClassify

# mine
extractions = [
    # ba_extraction,
    # shipin_extraction,
    # # tuPian_extraction,
    # xiaoShuo_extraction,
    xiazai_extraction,
    # yinpin_extraction
]

for line in sys.stdin:
        line_list = line.strip().split("\t")
        url = unicode(line_list[0].strip(), errors="ignore")

        str_info = line_list[-1]
        dict_info = json.loads(str_info)

        try:
            soup = BeautifulSoup(dict_info["cont_html"], "html.parser")
        except:
            soup = None

        # go go go!
        for do_extraction in extractions:
            do_extraction(url, dict_info, soup)

        # # 介峰部分
        # p = PageClassify(url, dict_info, soup)
        # p.predict()









