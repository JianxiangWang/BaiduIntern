#! /usr/bin/env python
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from deepdive import *

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
    # {"体育人物_偶像": {"s": [["崔浩", "PER", 0, 2]], "o": [["崔浩", "PER", 0, 2]]}}

    dict_so = json.loads(so)

    so_sets = set([])
    for P in dict_so:
        s_list, o_list = dict_so[P]["s"], dict_so[P]["o"],
        for so_mention, _, char_start_index, length in s_list + o_list:
            so_sets.add((so_mention, char_start_index, length))



    errorToken = 0
    # [[0, 1], [2], [3, 4]]
    tokens_char_indices = []
    offset = 0
    for token in tokens:
        if token != None:
            tokens_char_indices.append(list(range(offset, offset + len(unicode(token)))))
            offset += len(unicode(token))
        else:
            errorToken = 1

    if errorToken == 1:
        print >>sys.stderr, 'Error Tokens:', sent_id, tokens
    else:
        # 每一个生成一个mention对象
        for so_mention, char_start_index, length in so_sets:

            # 最后的token是谁
            char_end_index = char_start_index + length - 1

            begin_index = None
            end_index = None
            for index, item in enumerate(tokens_char_indices):
                if char_start_index in item:
                    begin_index = index
                if char_end_index in item:
                    end_index = index

                if begin_index and end_index:
                    break

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
