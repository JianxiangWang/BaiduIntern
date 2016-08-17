import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json


def main(fin, url):
    for line in fin:
        line_list = line.strip().split("\t")
        this_url = line_list[0].strip()
        dict_info_str = line_list[-1].strip()

        if this_url.strip() == url:
            dict_info = json.loads(dict_info_str)
            print dict_info["cont_html"]


if __name__ == '__main__':
    # parse_file = sys.argv[1]
    # cmd:
    # cat test_data/org/org.test.data.filtered | awk -F '\t' '{print $2, "\t", $4}' | python get_html_file.py "http://cang.qq.com/"
    url = sys.argv[1]
    main(sys.stdin, url)