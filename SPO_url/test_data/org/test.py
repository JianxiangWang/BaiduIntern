# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


fin_1 = open("org.test.data.filtered.urls.ner")
fin_2 = open("org.test.data.filtered.s")
fout = open("org.test.data.filtered.s.ner")

dict_url_to_new_info = {}
for line in fin_1:
    url, info = line.strip().split("\t")
    dict_url_to_new_info[url.strip()] = info.strip()

for line in fin_2:
    p, url, s, label, _ = line.strip().split("\t")
    if url in dict_url_to_new_info:
        info = dict_url_to_new_info[url]
        fout.write("%s\t%s\t%s\t%s\t%s\n" % (p, url, s, label, info))







