#!/usr/bin/env python2.7
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json

def read_input(file):
    for line in file:
        yield json.loads(line.strip(), encoding="utf-8")

def main(separator='\t'):
    data = read_input(sys.stdin)

    for instance in data:
        s, p, o, \
        sentence, fromUrl, confidence \
            = instance["s"], instance["p"], instance["o"], \
              instance["sentence"], instance["fromUrl"], instance["confidence"]

        # key
        key = "%s %s %s" % (s, p, o)

        # value
        sentence = sentence_processing(sentence)
        value = "|~|".join([sentence, fromUrl, confidence])

        print "%s%s%s" % (key, separator, value)




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
    main()
