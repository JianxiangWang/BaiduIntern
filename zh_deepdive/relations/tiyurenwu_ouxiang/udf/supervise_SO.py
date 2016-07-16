#!/usr/bin/env python
# coding: utf-8
import sys
import pickle
reload(sys)
sys.setdefaultencoding("utf-8")
from deepdive import *



dict_P_to_so_set = pickle.load(
    open("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/relations/tiyurenwu_ouxiang/input/seed.all.data.pkl", "rb"))

curr_P = "明星_好友"
curr_P_so_set = dict_P_to_so_set[curr_P]


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
    # Constants
    Positive_Lead_words = frozenset(["朋友", "好友", "友情", "友谊", "友", "基友", "密友", "老友"])
    Negative_Lead_words = frozenset(["夫妻", "丈夫", "妻子", "老公", "老婆", "母亲", "父亲", "姐姐", "妹妹","哥哥", "弟弟"])
    MAX_DIST = 10

    # Common data objects
    S_end_idx = min(S_end_index, O_end_index)
    O_start_idx = max(S_begin_index, O_begin_index)
    O_end_idx = max(S_end_index, O_end_index)
    intermediate_tokens = tokens[S_end_idx+1:O_start_idx]
    intermediate_ner_tags = ner_tags[S_end_idx+1:O_start_idx]
    tail_lemmas = tokens[O_end_idx+1:]

    # print >> sys.stderr, "===>", " ".join(intermediate_tokens)

    # 使用SPO三元祖进行标记:
    if (S_text, O_text) in curr_P_so_set:
        yield [S_id, O_id, 1, "pos:from KnowledgeBase"]

    # Rule: Candidates that are too far apart
    if len(intermediate_tokens) > MAX_DIST:
        yield [S_id, O_id, -1, "neg:far_apart"]

    # # Rule: Candidates that have a third person in between
    # if 'PER' in intermediate_ner_tags:
    #     yield spouse._replace(label=-1, type='neg:third_person_between')

    # 又一个中间的 S ?

    # Rule: Sentences that contain positive lead words in between
    if len(Positive_Lead_words.intersection(intermediate_tokens)) > 0:
        yield [S_id, O_id, 1, "pos: positive lead words between"]


    # Rule: Sentences that contain negative lead words relations:
    if len(Negative_Lead_words.intersection(intermediate_tokens)) > 0:
        yield [S_id, O_id, -1, "neg: negative lead words between"]
