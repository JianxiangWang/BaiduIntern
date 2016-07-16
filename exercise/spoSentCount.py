#encoding: utf-8


################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Authors: wangjianxiang(wangjianxiang01@baidu.com)
Date:    2016/06/17 17:23:06
"""

import json
import sys


def do_spo_sent_count(in_file, to_file):
    """
    统计每个spo包含的不同句子数
    :param in_file: 原始输入数据文件
    :param to_file: spo到句子的dict的json文件
    :return: None
    """

    with open(in_file) as fin, open(to_file, "w") as fout:

        dict_spo_to_sent_list = {}
        visited = set()

        for line in fin:
            instance = json.loads(line)

            s, p, o, \
            sentence, fromUrl, confidence \
                = instance["s"], instance["p"], instance["o"], \
                  instance["sentence"], instance["fromUrl"], instance["confidence"]

            # key
            k = "%s %s %s" % (s, p, o)

            # sentence_processing
            _sentence = sentence_processing(sentence)

            # judge the sentence, whether visited
            visited_key = "%s_%s" % (k, _sentence)
            if visited_key in visited:
                continue
            # not visited
            visited.add(visited_key)

            # value
            v = [sentence, fromUrl, confidence]

            if k not in dict_spo_to_sent_list:
                dict_spo_to_sent_list[k] = []
            dict_spo_to_sent_list[k].append(v)

        print("SPO count: %d" % len(dict_spo_to_sent_list))
        # to file
        json.dump(dict_spo_to_sent_list, fout, ensure_ascii=False)


def sentence_processing(sentence):

    en_punctuations = """ !"#&'*+,-..../:;<=>?@[\]^_`|~%""" + "``" + "''"
    ch_punctuations = "``''，。；、：？！∶… …──“”＊「」《》【】"
    nums = "0123456789"
    symbols = en_punctuations + ch_punctuations + nums
    sentence = remove_flanking_symbols(sentence, symbols)

    return sentence


def remove_flanking_symbols(string, symbols):
    i = 0
    while i < len(string) and (string[i] in symbols):
        i += 1
    if i == len(string):
        return ""

    j = len(string) - 1
    while j >= 0 and (string[j] in symbols):
        j -= 1
    return string[i: j + 1]


if __name__ == '__main__':

    in_file = sys.argv[1]
    to_file = sys.argv[2]

    do_spo_sent_count(in_file, to_file)

    # 吴亦凡 合演 王思聪



