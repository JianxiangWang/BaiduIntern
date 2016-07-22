# coding: utf-8
import pprint
import json
import sys
import codecs

import pypinyin

reload(sys)
sys.setdefaultencoding('utf-8')



def _get_begin_index_and_end_index(tokens, char_start_index, char_length):

    char_end_index = char_start_index + char_length - 1

    begin_index = None
    end_index = None

    offset = 0
    for index, token in enumerate(tokens) :
        curr_token_char_range = list(range(offset, offset + len(unicode(token))))

        if char_start_index in curr_token_char_range:
            begin_index = index

        if char_end_index in curr_token_char_range:
            end_index = index

        if begin_index and end_index:
            break

        offset += len(unicode(token))

    return begin_index, end_index

# [char_start_index, char_end_index]
def space_count(sent, char_start_index, char_end_index):
    c = 0
    for w in sent[char_start_index: char_end_index + 1]:
        if w == " ":
            c += 1
    return c

# 博士 ，中国人民大学外语学院
# 领会 词 单词 索引 表 作者 介绍 王长喜 ， 著名 英语教学 与 研究 专家 ， 北京外国语大学 博士 ， 中国人民大学外语学院 教授
# 领会词单词索引表 作者介绍 王长喜，著名英语教学与研究专家，北京外国语大学博士，中国人民大学外语学院教授
# 博士 37 2

tokens = "领会 词 单词 索引 表 作者 介绍 王长喜 ， 著名 英语教学 与 研究 专家 ， 北京外国语大学 博士 ， 中国人民大学外语学院 教授".split(" ")
sent = "领会词单"


print len(unicode(sent))

# print space_count(sent, 0, 37)
#
#
# begin_index, end_index =  _get_begin_index_and_end_index(tokens, 35, 2)
#
# for w in tokens[begin_index: end_index+1]:
#     print w
