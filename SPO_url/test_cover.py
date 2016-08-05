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
        dict_url_to_spo[url].append((s, p, o))
    fin.close()

    #
    all_urls = set(dict_url_to_page_type.keys())
    spo_urls = set(dict_url_to_spo.keys())

    # SPO 提取数
    print "==========SPO提取数============"
    print num_extract

    # 覆盖率
    print "===========覆盖率=============="
    print "%d / %d = %.2f%%" % (len(spo_urls & all_urls), len(all_urls), float(len(spo_urls & all_urls)) / len(all_urls) * 100)
    # 未覆盖
    no_page_type_num = 0
    dict_page_type_count = {}
    for url in all_urls - spo_urls:
        for page_type in dict_url_to_page_type[url]:
            if page_type not in dict_page_type_count:
                dict_page_type_count[page_type] = 0
            dict_page_type_count[page_type] += 1

        # 没有page type 的
        if dict_url_to_page_type[url] == []:
            no_page_type_num += 1

    print "====未覆盖的 page type 统计======"
    for page_type in dict_page_type_count:
        print page_type, dict_page_type_count[page_type]
    print "无page type: %d" % (no_page_type_num)







if __name__ == '__main__':
    main("data/org.all", "data/org.all.spo")