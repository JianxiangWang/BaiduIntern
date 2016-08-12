import sys

import json


def main(parse_file, url):

    for line in open(parse_file):
        line_list = line.strip().split("\t")
        this_url = line_list[1].strip()
        dict_info_str = line_list[-1].strip()

        if this_url.strip() == url:
            dict_info = json.loads(dict_info_str)
            print dict_info["cont_html"]


if __name__ == '__main__':
    parse_file = sys.argv[1]
    url = sys.argv[2]
    main(parse_file, url)