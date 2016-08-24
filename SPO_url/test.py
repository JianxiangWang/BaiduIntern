#!/usr/bin/env python
#encoding: utf-8
import sys

import bs4
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
import re




for line in sys.stdin:
    line_list = line.strip().split("\t")
    if line_list[0] == "下载" and line_list[3] == "1":
        print line.strip()



