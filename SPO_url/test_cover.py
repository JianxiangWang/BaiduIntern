# encoding: utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(url_parsed_file, url_predict_file):

    # 1.
    dict_url_to_page_type = {}
    fin = open(url_parsed_file)
    for line in fin:
        line_list = line.strip().split("\t")
        url = line_list[0]
        dict_info = json.loads(line_list[-1])
        dict_url_to_page_type[url] = dict_info["page_type"]
    fin.close()

    # 2.
    num_extract = 0

    dict_url_to_spo = {}
    fin = open(url_predict_file)
    for line in fin:
        num_extract += 1
        line_list = line.strip().split("\t")
        url, s, p, o = line_list[0], line_list[1], line_list[2], line_list[3]
        if url not in dict_url_to_spo:
            dict_url_to_spo[url] = []
        dict_url_to_spo[url].appped((s, p, o))
    fin.close()

    # 覆盖率
    print "%d / %d = %.2f%%" % (len(set(dict_url_to_page_type.keys()) & set(dict_url_to_spo.keys())),
                                len(dict_url_to_page_type),
                                len(set(dict_url_to_page_type.keys()) & set(dict_url_to_spo.keys())) / float(len(dict_url_to_page_type))
    )

if __name__ == '__main__':
    main("data/org.all", "data/org.all.spo")