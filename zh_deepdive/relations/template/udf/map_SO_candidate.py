#! /usr/bin/env python
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from deepdive import *

# 读取当前P
fin = open("../../../P")
this_P = fin.read().strip()
fin.close()



def _get_begin_index_and_end_index(tokens, char_start_index, char_length):

    char_end_index = char_start_index + char_length - 1

    begin_index = None
    end_index = None

    offset = 0
    for index, token in enumerate(tokens):
        curr_token_char_range = list(range(offset, offset + len(unicode(token))))

        if char_start_index in curr_token_char_range:
            begin_index = index

        if char_end_index in curr_token_char_range:
            end_index = index

        if begin_index and end_index:
            break

        offset += len(unicode(token))

    return begin_index, end_index

# s ==> ["刘德华", "PER", 41, 3]
def _get_mention(sent_id, tokens, s):
    so_mention_text, _,  char_start_index, char_length = s
    begin_index, end_index = _get_begin_index_and_end_index(tokens, char_start_index, char_length)

    if begin_index and end_index:
        mention_id = "%s_%d_%d" % (sent_id, begin_index, end_index)
        mention_text = " ".join([tokens[index] for index in range(begin_index, end_index + 1)])
        mention_text_ = "".join([tokens[index] for index in range(begin_index, end_index + 1)])

        # token对应的mention 与 so 识别的mention, 至少得有交集
        if set(unicode(mention_text_)) == set(unicode(so_mention_text)) :
            return mention_id, mention_text

    return None, None


@tsv_extractor
@returns(
    lambda
    S_mention_id     = "text",
    S_mention_text   = "text",
    O_mention_id     = "text",
    O_mention_text   = "text",
    :[])
def extract(
        sent_id    = "text",
        tokens     = "text[]",
        so         = "text",
):

    dict_so = json.loads(so)
    # json 是 unicode
    P = unicode(this_P)
    s_list, o_list = dict_so[P]["s"], dict_so[P]["o"]

    s_list = map(tuple, s_list)
    o_list = map(tuple, o_list)

    # 不为空
    if s_list != [] and o_list != []:
        # 获取SO对应的mention的个数
        num_mention = len(set(s_list + o_list))
        if num_mention > 1 and num_mention  < 5:
            for s in s_list:
                for o in o_list:
                    if s == o:
                        continue
                    # 生成一个 candidate
                    S_mention_id, S_mention_text = _get_mention(sent_id, tokens, s)
                    O_mention_id, O_mention_text = _get_mention(sent_id, tokens, o)

                    if S_mention_id and O_mention_id:
                        yield [
                            S_mention_id,
                            S_mention_text,
                            O_mention_id,
                            O_mention_text,
                        ]