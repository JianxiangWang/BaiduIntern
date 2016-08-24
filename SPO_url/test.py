#!/usr/bin/env python
#encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json

for line in sys.stdin:
    url, json_str = line.strip().split("\t")
    dict_json = json.loads(json_str)

    url = unicode(url, errors="ignore")
    print u"%s\t%s" % (url, dict_json["realtitle"])


