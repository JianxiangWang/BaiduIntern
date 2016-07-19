#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import json


def post_process(sentence_info):
    """
    将sentence_info中的mars_ner结果进行后处理，提高识别准确率

    Parameters:
    sentence_info: [input && output], 读入sentence_info中的信息，并修改
            修改mars_ner的效果

    Returns:
    """
    sentence = sentence_info['sentence']
    mars_ner = sentence_info['mars_ner']
    #print >> sys.stderr, sentence
    for predicate in mars_ner:
        temp_s = []
        for s_info in mars_ner[predicate]['s']:
            #print >> sys.stderr, 'sentence: %s' % (json.dumps(s_info, ensure_ascii = False))
            if s_info[1] in [u'VDO', u'SNG', u'NVL']:
                s_beg = s_info[2]
                s_end = s_info[2] + s_info[3]
                #print >> sys.stderr, 'beg_pos: %d\tend_pos: %d' % (s_beg, s_end)
                if s_beg >= 1 and s_end < len(sentence):
                    if sentence[s_beg - 1] in [u'<', u'《'] and \
                            sentence[s_end] in [u'>', u'》']:
                        temp_s.append(s_info)
            else:
                temp_s.append(s_info)
        mars_ner[predicate]['s'] = temp_s
    return

reload(sys)
sys.setdefaultencoding('utf-8')

s_prop_dict = {}
with open(sys.argv[1]) as in_file:
    #电视剧\tVDO\tdianshiju
    for line in in_file:
        line = line.decode('utf-8').rstrip('\r\n')
        field = line.split('\t')
        s_prop_dict[field[0]] = field[1]

so_result = {}
for line in sys.stdin:
    line = line.decode('utf-8').rstrip('\r\n')
    field = line.split('\t')
    so_result = json.loads(field[0])
    sentence = so_result['sentence']
    url = so_result['url']
    pub_time = so_result['publishTime']
    link_time = so_result['linkFoundTime']
    depparser = so_result['depparser']
    des_s_type = []
    for prop in so_result['p_list']:
        local_type = prop.split('_')[0]
        des_s_type.append(s_prop_dict[local_type])
    des_s_type = list(set(des_s_type))
    beg_index = 0
    #存储s的列表
    s_info_list = []
    for word_info in depparser:
        if word_info[5] in des_s_type:
            temp_list = []
            temp_list.append(word_info[1])
            temp_list.append(word_info[5])
            if sentence.find(word_info[1], beg_index) != -1:
                beg_index = sentence.find(word_info[1], beg_index)
                temp_list.append(beg_index)
                beg_index += len(word_info[1])
            else:
                break
            temp_list.append(len(word_info[1]))
            s_info_list.append(temp_list)
    for prop in so_result['mars_ner']:
        prop_domain = prop.split('_')[0]
        if s_prop_dict[prop_domain] in des_s_type and len(so_result['mars_ner'][prop]['s']) == 0:
            temp_list = []
            for item in s_info_list:
                if item[1] == s_prop_dict[prop_domain]:
                    temp_list.append(item)
            so_result['mars_ner'][prop]['s'] = temp_list
    post_process(so_result)
    print json.dumps(so_result, ensure_ascii = False)

