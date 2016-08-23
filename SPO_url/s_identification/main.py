# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 识别 "视频", "评测", "简介", "个人资料"  的 s
def main(fin, fout):
    for line in fin:
        line_list = line.strip().split("\t")
        p = line_list[2]

        s = "NULL"
        if p == "个人资料":
            s = str(get_s_for_gerenziliao(line))
        if p == "简介":
            s = str(get_s_for_jianjie(line))
        if p == "评测":
            s = str(get_s_for_ceping(line))
        if p == "视频":
            s = str(get_s_for_shipin(line))
        if p == "音频":
            s = str(get_s_for_yinpin(line))
        if p == "下载":
            s = str(get_s_for_xiazai(line))

        line_list[1] = s

        fout.write("\t".join(line_list[:-1]) + "\n")

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


# 简介
def get_s_for_jianjie(line):
    line = unicode(line, errors="ignore")

    line_list = line.strip().split("\t")
    ner_list = eval(line_list[-1])
    title = line_list[1].strip()

    S = None

    key_word_list = [u"简介", u"介绍"]

    if ner_list != []:
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
            S = unicode(entity_name, errors="ignore")

    if S is None:

        # 如果title中存在关键字, 且不能识别其中的实体的时候, 使用策略去识别
        key_word_idx = -1
        for key_word in key_word_list:
            if title.find(key_word) != -1:
                key_word_idx = title.find(key_word)

        if key_word_idx != -1:
            # 从关键字往前扫描, 遇到标点空格停止
            i = key_word_idx - 1
            while i >= 0:
                if title[i] in u" ，。！；？":
                    break
                i -= 1
            title = title[i + 1: key_word_idx]

        S = title

    if S.endswith("）"):
        if "（" in S:
            S = S[:S.rfind("（")]
    if S.endswith(")"):
        if "(" in S:
            S = S[:S.rfind("(")]

    # 如果有 【南妹皇后】, 《斗破苍穹》 取中间的
    if u"《" in S and u"》" in S:
        start = S.find(u"《")
        end = S.find(u"》")
        if start < end:
            S = S[start+1: end]

    if u"【" in S and u"】" in S:
        start = S.find(u"【")
        end = S.find(u"】")
        if start < end:
            S = S[start + 1: end]


    # 用去掉一些词
    useless_end_words = [
        u"介绍大全",
        u"介绍",
        u"故事简介",
        u"简介",
    ]

    for end_word in useless_end_words:
        if S.endswith(end_word):
            S = S[:len(S) - len(end_word)]


    return S


# 测评
def get_s_for_ceping(line):
    line = unicode(line, errors="ignore")

    line_list = line.strip().split("\t")
    ner_list = eval(line_list[-1])
    title = line_list[1]

    if ner_list == []:
        return title

    key_word_list = [u"测评", u"评测", u"上手评测", u"上手测评"]
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

    # 如果title中关键字 "测评", "评测", 且不能识别其中的实体的时候, 使用策略去识别
    key_word_idx = -1
    for key_word in key_word_list:
        if title.find(key_word) != -1:
            key_word_idx = title.find(key_word)

    if key_word_idx != -1:
        # 从关键字往前扫描, 遇到标点空格停止
        i = key_word_idx - 1
        while i >= 0:
            if title[i] in u" ，。！；？":
                break
            i -= 1
        title = title[i+1: key_word_idx]

    return title


# 视频
def get_s_for_shipin(line):
    line = unicode(line, errors="ignore")

    line_list = line.strip().split("\t")
    ner_list = eval(line_list[-1])
    title = line_list[1]

    if ner_list != []:
        before_idx = len(title)
        entity_name = None

        for ner in ner_list:
            offset = ner["offset"]
            etype = ner["etype"]

            if offset < before_idx:
                entity_name = ner["name"]

        if entity_name:
            title = unicode(entity_name, errors="ignore")

    if u"【" in title and u"】" in title:
        start = title.find(u"【")
        end = title.find(u"】")
        if start < end:
            title = title[start + 1: end]

    # 用去掉一些词
    useless_end_words = [
        u"的视频",
        u"短视频",
        u"热门视频",
        u"爆笑视频",
        u"搞笑视频",
        u"视频",
    ]
    useless_start_words = [
        u"视频:",
        u"精选"
    ]


    for end_word in useless_end_words:
        if title.endswith(end_word):
            title = title[:len(title) - len(end_word)]

    for start_word in useless_start_words:
        if title.startswith(start_word):
            title = title[len(start_word):]

    return title


# 音频
def get_s_for_yinpin(line):
    line = unicode(line, errors="ignore")

    line_list = line.strip().split("\t")
    ner_list = eval(line_list[-1])
    title = line_list[1].split(" ", 1)[0]

    if ner_list != []:
        before_idx = len(title)
        entity_name = None
        for ner in ner_list:
            offset = ner["offset"]
            etype = ner["etype"]

            if offset < before_idx:
                entity_name = ner["name"]
                break

        if entity_name:
            title = unicode(entity_name, errors="ignore")

    return title


# 下载
def get_s_for_xiazai(line):
    line = unicode(line, errors="ignore")

    line_list = line.strip().split("\t")
    ner_list = eval(line_list[-1])
    title = line_list[1].split(" ", 1)[0]

    if ner_list != []:
        before_idx = len(title)
        entity_name = None
        for ner in ner_list:
            offset = ner["offset"]
            etype = ner["etype"]

            if offset < before_idx:
                entity_name = ner["name"]
                break

        if entity_name:
            title = unicode(entity_name, errors="ignore")

    # 如果有 【南妹皇后】, 《斗破苍穹》 取中间的
    if u"《" in title and u"》" in title:
        start = title.find(u"《")
        end = title.find(u"》")
        if start < end:
            title = title[start + 1: end]

    # 删除一些不必要的词
    useless_words = [
        u"txt",
        u"TXT",
        u"下载"
    ]

    for word in useless_words:
        if word in title:
            title = title.replace(word, "")

    return title

if __name__ == '__main__':
    main(
        open("/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo.someP.ner"),
        open("/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo.someP.pred", "w"),
    )

