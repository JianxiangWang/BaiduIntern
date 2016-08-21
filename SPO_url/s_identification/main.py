#encoding: utf-8

# 识别 "视频", "评测", "简介", "个人资料"  的 s
def main(fin):
    for line in fin:
        line_list = line.strip().split("\t")
        p = line_list[2]

        s = "NULL"
        if p == "个人资料":
            s = get_s_for_gerenziliao(line)

        line_list[1] = s

        print "\t".join(line_list)

# 个人资料
def get_s_for_gerenziliao(line):
    line = unicode(line)

    line_list = line.strip().split("\t")
    ner_list = eval(line_list[-1])
    title = line_list[1]

    if ner_list == []:
        return title

    key_word = u"个人资料"

    if key_word in title:
        before_idx = title.find(key_word) + 4
    else:
        before_idx = len(title)

    # 离关键字最近的那个实体, 人物
    renwu_etype_list = [
        "1000", "1001",
        "1002", "1003",
        "1004", "1005",
        "1006", "1007",
        "1008", "1009",
        "1010", "1011",
        "1012"
    ]

    entity_name = None
    for ner in ner_list:
        offset = ner["offset"]
        etype = ner["etype"]

        if offset < before_idx and etype in renwu_etype_list:
            entity_name = ner["name"]

    if entity_name:
        return entity_name

    return title


if __name__ == '__main__':
    main(open("/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo.someP.ner"))

