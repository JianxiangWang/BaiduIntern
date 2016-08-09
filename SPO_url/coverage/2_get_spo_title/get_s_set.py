#  encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(to_file):

    fin1 = open("spo_titles.ner")
    fin2 = open("../1_get_all_urls/qiandaohu_spo2")


    s_set = set()
    for line1, line2 in zip(fin1, fin2):

        # 获取 P
        P = line2.strip().split("\t")[2]
        if P in ["新闻", "图片"]:
            continue

        line_list = line1.strip().split("\t")
        if len(line_list) == 1:
            # s = line1.strip().replace("query = ", "")
            # s_set.add(s)
            continue

        # 获取第一个NER识别结果
        r = line_list[1][1:-1].strip()
        for x in r.split("  "):
            try:
                k, v = x.split(" : ", 1)
            except:
                continue

            if k == "name":
                s_set.add(v)
                break

    fout = open(to_file, "w")
    for s in sorted(s_set):
        fout.write("%s\n" % s)

if __name__ == '__main__':
    main("qdh.s.no_tupian_xinwen")
