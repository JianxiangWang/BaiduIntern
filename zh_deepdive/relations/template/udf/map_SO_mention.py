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

@tsv_extractor
@returns(
    lambda
    mention_id     = "text",
    mention_text   = "text",
    sent_id        = "text",
    begin_index    = "int",
    end_index      = "int",
    :[])
def extract(
        sent_id    = "text",
        tokens     = "text[]",
        so         = "text",
):

    dict_so = json.loads(so)
    # json 是 unicode
    P = unicode(this_P)

    so_sets = set([])
    s_list, o_list = dict_so[P]["s"], dict_so[P]["o"],
    for so_mention, _, char_start_index, length in s_list + o_list:
        so_sets.add((so_mention, char_start_index, length))

    # 每一个生成一个mention对象
    for so_mention, char_start_index, char_length in so_sets:

        begin_index, end_index = _get_begin_index_and_end_index(tokens, char_start_index, char_length)

        if begin_index and end_index:
            mention_id = "%s_%d_%d" % (sent_id, begin_index, end_index)
            mention_text = " ".join([tokens[index] for index in range(begin_index, end_index + 1)])
            mention_text_ = "".join([tokens[index] for index in range(begin_index, end_index + 1)])

            # token对应的mention 与 so 识别的mention, 至少得有交集
            if set(unicode(mention_text_)) == set(unicode(so_mention)) :

                yield [
                    mention_id,
                    mention_text,
                    sent_id,
                    begin_index,
                    end_index
                ]



