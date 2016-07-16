#!/usr/bin/env python
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from deepdive import *
import cPickle

# 读取当前P
fin = open("../../../P")
this_P = fin.read().strip()
fin.close()

''' 加载必要文件 '''
# P --> set([(a, b), ])
dict_P_to_seeds = cPickle.load(open("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/seed.train.cPkl", "rb"))

# P --> [P, P, P]
dict_P_to_similar_P_list = {}
with open("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/P_similar") as fin:
    for line in fin:
        P, T = line.strip().split("-->")
        similar_P_list = T.split(",")
        dict_P_to_similar_P_list[P] = similar_P_list

# P 的引导词, 包含正例的负例的
# p --> 'positive' or 'negative' --> set(["朋友", ...])
dict_P_to_guide_words = cPickle.load(open("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/guide_words.cPkl", "rb"))


@tsv_extractor
@returns(lambda
     S_id   = "text",
     O_id   = "text",
     label  = "int",
     rule_id= "text",
:[])
def supervise(
    S_id    ="text", S_text  ="text", S_begin_index ="int", S_end_index ="int",
    O_id    ="text", O_text  ="text", O_begin_index ="int", O_end_index ="int",
    sent_id         ="text",
    sent_text       ="text",
    tokens          ="text[]",
    pos_tags        ="text[]",
    ner_tags        ="text[]",
    dep_types       ="text[]",
    dep_tokens      ="int[]"
):

    # 当前P
    P = this_P

    MAX_DIST = 10

    ''' 1. 使用种子去标记'''

    # 出现P对应的 S, O ==> 则标记为正例
    if (S_text, O_text) in dict_P_to_seeds[P]:
        yield [S_id, O_id, 1, "pos: from seeds"]

    # 互斥的P 对应的 S O ==> 则标记为负例
    similar_P_list = dict_P_to_similar_P_list[P]
    similar_P_list.append(P)
    for curr_P in dict_P_to_seeds:
        # 不在相似中,就是互斥的
        if curr_P not in similar_P_list:
            if (S_text, O_text) in dict_P_to_seeds[curr_P]:
                yield [S_id, O_id, -1, "neg: from seeds"]
                break

    '''2. 使用引导词去标记'''

    positive_guide_words = dict_P_to_guide_words[P]["positive"]
    negative_guide_words = dict_P_to_guide_words[P]["negative"]

    S_end_idx = min(S_end_index, O_end_index)
    O_start_idx = max(S_begin_index, O_begin_index)
    intermediate_tokens = tokens[S_end_idx+1:O_start_idx]

    # positive guide words
    if len(positive_guide_words.intersection(intermediate_tokens)) > 0:
        yield [S_id, O_id, 1, "pos: positive guide words between"]

    # negative guide words
    if len(negative_guide_words.intersection(intermediate_tokens)) > 0:
        yield [S_id, O_id, -1, "neg: negative guide words between"]

    # 3. S O 之间的距离
    if len(intermediate_tokens) > MAX_DIST:
        yield [S_id, O_id, -1, "neg:far_apart"]
