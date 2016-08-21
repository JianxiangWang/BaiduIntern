# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 识别 "视频", "评测", "简介", "个人资料"  的 s
def main(fin):
    for line in fin:
        line_list = line.strip().split("\t")
        p = line_list[2]

        s = "NULL"
        if p == "个人资料":
            s = str(get_s_for_gerenziliao(line))
        if p == "简介":
            s = str(get_s_for_jianjie(line))

        line_list[1] = s

        print "\t".join(line_list[:-1])

# 个人资料
def get_s_for_gerenziliao(line):
    line = unicode(line, errors="ignore")

    line_list = line.strip().split("\t")
    ner_list = eval(line_list[-1])
    title = line_list[1]

    if ner_list == []:
        return title

    key_word = u"个人资料"
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


    if key_word in title:
        before_idx = title.find(key_word) + len(key_word)
    else:
        before_idx = len(title)

    entity_name = None
    for ner in ner_list:
        offset = ner["offset"]
        etype = ner["etype"]

        if offset < before_idx and etype in renwu_etype_list:
            entity_name = ner["name"]

    if entity_name:
        return entity_name

    return title


# 个人资料
def get_s_for_jianjie(line):
    line = unicode(line, errors="ignore")

    line_list = line.strip().split("\t")
    ner_list = eval(line_list[-1])
    title = line_list[1]

    if ner_list == []:
        return title

    key_word_list = [u"简介", "介绍"]
    before_idx_list = [title.find(key_word) + len(key_word) for key_word in key_word_list if key_word in title ]
    if before_idx_list == []:
        before_idx = len(title)
    else:
        before_idx = min(before_idx_list)

    entity_name = None
    for ner in ner_list:
        offset = ner["offset"]
        etype = ner["etype"]

        if offset < before_idx:
            entity_name = ner["name"]

    if entity_name:
        return entity_name

    return title


if __name__ == '__main__':
    main(open("/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo.someP.ner"))

