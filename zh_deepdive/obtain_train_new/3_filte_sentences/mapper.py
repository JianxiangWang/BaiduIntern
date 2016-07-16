#!tools/python/bin/python
# coding: utf-8
import json
import uuid
import sys
import cPickle
reload(sys)
sys.setdefaultencoding('utf-8')


''' 加载必要文件 '''
# P --> set([(a, b), ])
dict_P_to_seeds = cPickle.load(open("seed.train.cPkl", "rb"))

# P --> [P, P, P]
dict_P_to_similar_P_list = {}
with open("P_similar") as fin:
    for line in fin:
        P, T = line.strip().split("-->")
        similar_P_list = T.split(",")
        dict_P_to_similar_P_list[P] = similar_P_list

# P 的引导词, 包含正例的负例的
# p --> 'positive' or 'negative' --> set(["朋友", ...])
dict_P_to_guide_words = cPickle.load(open("guide_words.cPkl", "rb"))


def main():

    MAX_SENT_LENGTH = 400

    for line in sys.stdin:
        line = json.loads(line)
        # 闯关啦~~~
        wanted = False
        for P in line["mars_ner"]:
            s_list, o_list = line["mars_ner"][P]["s"], line["mars_ner"][P]["o"]

            s_list = map(tuple, s_list)
            o_list = map(tuple, o_list)

            # 不为空
            if s_list != [] and o_list != []:
                # 获取SO对应的mention的个数
                num_mention = len(set(s_list + o_list))
                if num_mention > 1 and num_mention  < 5:
                    # 判断句子长度
                    sent_length = len(line["depparser"])
                    if sent_length < MAX_SENT_LENGTH:
                        # 对每一对SO, 判断能否被当前P标注成功
                        for s in s_list:
                            for o in o_list:
                                # s, o 不是 同一个
                                if s != o:
                                    if label_success(line["depparser"], s, P, o):
                                        wanted = True
                                        break
                            if wanted:
                                break
            if wanted:
                break

        # 闯关成功! format ...
        if wanted:
            sent_id = uuid.uuid1()
            markup = line["depparser"]

            tokens = [item[1] for item in markup]
            pos_tags = [item[4] for item in markup]
            ner_tags = [item[5] for item in markup]
            dep_types = [item[-1] for item in markup]
            dep_tokens = [item[-2] for item in markup]

            # , -> ','
            # "  -> ''
            # \ -> 空
            # } => 》
            # { => 《
            dict_change = {
                ",": "COMMA",
                "\"": "QUOTATION",
                "\\": "*",
                "{": "《",
                "}": "》",
            }

            new_tokens = []
            for x in tokens:
                if x in dict_change:
                    x = dict_change[x]

                new_tokens.append(x)

            tokens     = "{%s}" % (",".join(new_tokens))
            pos_tags   = "{%s}" % (",".join(pos_tags))
            ner_tags   = "{%s}" % (",".join(ner_tags))
            dep_types  = "{%s}" % (",".join(dep_types))
            dep_tokens = "{%s}" % (",".join(map(str, dep_tokens)))

            if len(tokens.split(",")) != len(pos_tags.split(",")):
                continue
            if len(tokens.split(",")) != len(ner_tags.split(",")):
                continue
            if len(tokens.split(",")) != len(dep_types.split(",")):
                continue
            if len(tokens.split(",")) != len(dep_tokens.split(",")):
                continue

            tokens = tokens.replace("\"", "'")
            tokens = "{" + tokens[1:-1].replace("{", "《").replace("}", "》") +"}"
            if tokens == "{}":
                continue

            S_O = json.dumps(line["mars_ner"], ensure_ascii=False)

            sent_sent = " ".join(new_tokens)

            print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                sent_id, sent_sent, tokens, pos_tags, ner_tags, dep_types, dep_tokens, S_O
            )




# 判断能否被标注成功
def label_success(markup, s, P, o):
    tokens = [item[1] for item in markup]
    S_text = s[0]
    O_text = o[0]

    # 确定 S_begin_index, S_end_index
    S_begin_index, S_end_index = _get_begin_index_and_end_index(tokens, s[2], s[3])
    O_begin_index, O_end_index = _get_begin_index_and_end_index(tokens, o[2], o[3])

    if S_begin_index and S_end_index and O_begin_index and O_end_index:
        depparser_S_text = "".join([tokens[index] for index in range(S_begin_index, S_end_index + 1)])
        depparser_O_text = "".join([tokens[index] for index in range(O_begin_index, O_end_index + 1)])

        # depparser 对应的 SO 是不是 与 SO 识别的一致, 不一致 不要
        if S_text == depparser_S_text and O_text == depparser_O_text:

            label, rule = \
                label_for_current_P(tokens, S_text, S_begin_index, S_end_index, O_text, O_begin_index, O_end_index, P)

            if label and rule:
                return True

    return False


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


def label_for_current_P(tokens,
                        S_text, S_begin_index, S_end_index,
                        O_text, O_begin_index, O_end_index, P):

    # unicode to str
    P = str(P)

    MAX_DIST = 10

    ''' 1. 使用种子去标记'''

    # 出现P对应的 S, O ==> 则标记为正例
    if (S_text, O_text) in dict_P_to_seeds[P]:
        return [1, "pos: from seeds"]

    # 互斥的P 对应的 S O ==> 则标记为负例
    similar_P_list = dict_P_to_similar_P_list[P]
    similar_P_list.append(P)
    for curr_P in dict_P_to_seeds:
        # 不在相似中,就是互斥的
        if curr_P not in similar_P_list:
            if (S_text, O_text) in dict_P_to_seeds[curr_P]:
                return [-1, "neg: from seeds"]

    '''2. 使用引导词去标记'''

    positive_guide_words = dict_P_to_guide_words[P]["positive"]
    negative_guide_words = dict_P_to_guide_words[P]["negative"]

    S_end_idx = min(S_end_index, O_end_index)
    O_start_idx = max(S_begin_index, O_begin_index)
    intermediate_tokens = tokens[S_end_idx+1:O_start_idx]

    # positive guide words
    if len(positive_guide_words.intersection(intermediate_tokens)) > 0:
        return [1, "pos: positive guide words between"]

    # negative guide words
    if len(negative_guide_words.intersection(intermediate_tokens)) > 0:
        return [-1, "neg: negative guide words between"]

    # 3. S O 之间的距离
    if len(intermediate_tokens) > MAX_DIST:
        return [-1, "neg:far_apart"]


    # 不能标记
    return [None, None]



if __name__ == "__main__":
    main()
