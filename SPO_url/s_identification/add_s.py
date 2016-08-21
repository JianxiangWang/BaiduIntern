#encoding: utf-8

# main("吧", "吧", "ba.test.data")
# main("视频", "视频", "shipin.test.data")
# main("小说", "小说", "xiaoshuo.test.data")
# main("下载", "下载", "xiazai.test.data")
# main("歌曲", "音频", "yinpin.test.data")
# main("评测", "评测", "pingce.test.data")
# main("简介", "简介", "jianjie.test.data")
# main("个人资料", "个人资料", "gerenziliao.test.data")
# main("百科", "百科", "baike.test.data")
# main("微博", "微博", "weibo.test.data")
# main("商品", "商品", "shangpin.test.data")


# 获取url到s的字典
def get_dict_url_to_p_to_s(org_file):
    end_words_list = [
        "吧",
        "视频",
        "小说",
        "下载",
        "歌曲",
        "评测",
        "简介",
        "个人资料",
        "百科",
        "微博",
        "商品",
    ]

    dict_url_to_p_to_s  = {}

    with open(org_file) as fin:
        for line in fin:
            line_list = line.strip().split("\t")
            query = line_list[0].strip()
            url = line_list[1].strip()
            label = line_list[2].strip()

            for end_word in end_words_list:
                if query.endswith(end_word) and "fakeurl" not in url:
                    P = end_word
                    S = query.replace(end_word, "")
                    dict_url_to_p_to_s[(url, P)] = S

    return dict_url_to_p_to_s

# 对于org标注的数据,加S
def add_S_for_org_annotation(org_file, org_test_data, to_file):
    dict_url_to_p_to_s = get_dict_url_to_p_to_s(org_file)

    with open(org_test_data) as fin, open(to_file, "w") as fout:
        for line in fin:
            line_list = line.strip().split("\t")
            P, url, label, json_str = line.strip().split("\t")
            P = P.strip()
            url = url.strip()

            S = "NULL"
            if (url, P) in dict_url_to_p_to_s:
                S = dict_url_to_p_to_s[(url, P)]

            fout.write("%s\t%s\t%s\t%s\t%s\n" % (P, url, S, label, json_str))


if __name__ == '__main__':
    add_S_for_org_annotation(
        "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/data/org",
        "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered",
        "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.s",
    )




