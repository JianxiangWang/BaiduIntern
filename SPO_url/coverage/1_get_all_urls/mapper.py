#!python/bin/python
#  encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# import ujson as json
import json

# 我 i
for line in sys.stdin:
    line_list = line.strip().split("\t")

    url = line_list[0].strip()
    url = unicode(url, errors="ignore")

    try:
        dict_info = json.loads(line_list[-1])
        page_type = dict_info["page_type"]
        print "%s\t%s" % (url, json.dumps(page_type, ensure_ascii=False))
    except:
        continue


