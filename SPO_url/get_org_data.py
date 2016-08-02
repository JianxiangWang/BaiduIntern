# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


fout1 = open("data/org.positive", "w")
fout2 = open("data/org.positive.urls", "w")

dict_P_to_urls = {}
for line in open("data/org"):
    line_list = line.strip().split("\t")
    title = line_list[0]
    url = line_list[1]
    label = line_list[2]

    if label != "1":
        continue
    if url.startswith("http://fakeurl"):
        continue


    if title.endswith("图片"):
        if "图片" not in dict_P_to_urls:
            dict_P_to_urls["图片"] = []
        dict_P_to_urls["图片"].append(url)


    if title.endswith("吧"):
        if "吧" not in dict_P_to_urls:
            dict_P_to_urls["吧"] = []
        dict_P_to_urls["吧"].append(url)

    if title.endswith("小说"):
        if "小说" not in dict_P_to_urls:
            dict_P_to_urls["小说"] = []
        dict_P_to_urls["小说"].append(url)

    if title.endswith("下载"):
        if "下载" not in dict_P_to_urls:
            dict_P_to_urls["下载"] = []
        dict_P_to_urls["下载"].append(url)

    if title.endswith("歌曲") or title.endswith("主题曲"):
        if "音频" not in dict_P_to_urls:
            dict_P_to_urls["音频"] = []
        dict_P_to_urls["音频"].append(url)

    if title.endswith("视频") or title.endswith("电影") or title.endswith("电视剧") or title.endswith("综艺"):
        if "视频" not in dict_P_to_urls:
            dict_P_to_urls["视频"] = []
        dict_P_to_urls["视频"].append(url)


for P in sorted(dict_P_to_urls.keys()):
    for url in dict_P_to_urls[P]:
        fout1.write("%s\t%s\n" % (P, url))
        fout2.write(url + "\n")

fout1.close()
fout2.close()



