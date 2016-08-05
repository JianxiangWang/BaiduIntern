import json
import sys

from ba.hadoop_main import do_extraction as ba_extraction
from shipin.hadoop_main import do_extraction as shipin_extraction


for line in sys.stdin:
    line_list = line.strip().split("\t")
    url = line_list[0]
    dict_info = json.loads(line_list[-1])

    ba_extraction(url, dict_info)
    shipin_extraction(url, dict_info)

