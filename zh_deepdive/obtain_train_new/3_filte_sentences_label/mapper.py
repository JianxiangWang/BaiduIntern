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
dict_P_to_seeds = cPickle.load(open("seed_train_for_84P.cPkl", "rb"))

# P --> [P, P, P]
dict_P_to_similar_P_list = {}
with open("P_similar") as fin:
    for line in fin:
        P, T = line.strip().split("-->")
        similar_P_list = T.split(",")
        dict_P_to_similar_P_list[P] = similar_P_list

# P 的引导词, 包含正例的负例的.
# p --> 'positive' or 'negative' --> set(["朋友", ...])
dict_P_to_guide_words = cPickle.load(open("guide_words_for_84P.cPkl", "rb"))

# test集的 so 集合
test_so_set = cPickle.load(open("test_so_set_for_84P.cPkl", "rb"))


def main():

    MAX_SENT_LENGTH = 400

    for line in sys.stdin:
        line = json.loads(line)
        # 闯关啦~~~

        sent_id = str(uuid.uuid1())
        sent_text = line["sentence"]
        markup = line["depparser"]

        tokens      = [item[1] for item in markup]
        pos_tags    = [item[4] for item in markup]
        ner_tags    = [item[5] for item in markup]
        dep_types   = [item[-1] for item in markup]
        dep_tokens  = [item[-2] for item in markup]


        # 一些标注信息
        dict_label_info = {}

        wanted = False
        for P in line["mars_ner"]:

            s_list, o_list = line["mars_ner"][P]["s"], line["mars_ner"][P]["o"]

            s_list = map(tuple, s_list)
            o_list = map(tuple, o_list)

            # 判断句子长度
            sent_length = len(line["depparser"])
            if sent_length >= MAX_SENT_LENGTH:
                continue

            # 不为空
            if s_list == [] or o_list == []:
                continue

            # 获取SO对应的mention的个数
            num_mention = len(set(s_list + o_list))
            if num_mention <= 1 or num_mention >= 5:
                   continue


            # to mention_list
            # s_list = [("刘德华", "PER", 0, 3), ...] == > [(mention_id, mention_text, sent_id, begin_index, end_index), ...]
            s_mention_list = []
            for s in s_list:
                mention = _get_mention(sent_text, sent_id, tokens, s)
                if mention:
                    s_mention_list.append(mention)

            o_mention_list = []
            for o in o_list:
                mention = _get_mention(sent_text, sent_id, tokens, o)
                if mention:
                    o_mention_list.append(mention)

            # 去重, 真的有重复的 !!!!
            s_mention_list = list(set(s_mention_list))
            o_mention_list = list(set(o_mention_list))


            # 判断so pair 能不能被标注
            for s_mention in s_mention_list:
                for o_mention in o_mention_list:
                    # 不能相同, surface level
                    if s_mention[1] == o_mention[1]:
                        continue

                    # s,o 不能在 test 集合中
                    if (str(s_mention[1]), str(o_mention[1])) in test_so_set:
                        continue


                    # 标注, 一个候选集合可能被多条规则选中
                    for label, rule, info in label_for_current_P(
                            tokens,
                            s_mention[1], s_mention[-2], s_mention[-1],
                            o_mention[1], o_mention[-2], o_mention[-1],
                            P
                    ):
                        wanted = True

                        if P not in dict_label_info:
                            dict_label_info[P] = {}
                            dict_label_info[P]["mentions"] = []
                            dict_label_info[P]["candidates"] = {}

                        # mention
                        dict_label_info[P]["mentions"].append(s_mention)
                        dict_label_info[P]["mentions"].append(o_mention)
                        #
                        S_id = s_mention[0]
                        S_text = s_mention[1]
                        O_id = o_mention[0]
                        O_text = o_mention[1]
                        k = "|~|".join([S_id, S_text, O_id, O_text])
                        if k not in dict_label_info[P]["candidates"]:
                            dict_label_info[P]["candidates"][k] = {}
                            dict_label_info[P]["candidates"][k]["label_info"] = []
                            dict_label_info[P]["candidates"][k]["label"] = 0
                        dict_label_info[P]["candidates"][k]["label_info"].append([label, rule, unicode(info)])
                        dict_label_info[P]["candidates"][k]["label"] += label


            # 去重复
            if P in dict_label_info:
                dict_label_info[P]["mentions"] = list(set(dict_label_info[P]["mentions"]))



        # 闯关成功! format ...
        if wanted:

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

            print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                sent_id, sent_sent, tokens, pos_tags, ner_tags, dep_types, dep_tokens, S_O,
                json.dumps(dict_label_info, ensure_ascii=False)
            )



# s: ("刘德华", "PER", 0, 3)
# return (mention_id, mention_text, sent_id, begin_index, end_index)
def _get_mention(sent_text, sent_id, tokens, s):

    # 需要修改 char_start_index, char_length, 因为他计算了空格
    so_mention_text, _,  char_start_index, char_length = s

    before_space_count = space_count(sent_text, 0, char_start_index)
    in_space_count = space_count(sent_text, char_start_index, char_start_index + char_length -1)

    #
    char_start_index -= before_space_count
    char_length -= in_space_count


    begin_index, end_index = _get_begin_index_and_end_index(tokens, char_start_index, char_length)

    if begin_index and end_index:
        mention_id = "%s_%d_%d" % (sent_id, begin_index, end_index)
        mention_text = " ".join([tokens[index] for index in range(begin_index, end_index + 1)])
        mention_text_ = "".join([tokens[index] for index in range(begin_index, end_index + 1)])

        # token对应的mention 与 so 识别的mention, 至少得有交集
        if set(unicode(mention_text_)) == set(unicode(so_mention_text)) :
            return (mention_id, mention_text, sent_id, begin_index, end_index)

    return None

# [char_start_index, char_end_index]
def space_count(sent, char_start_index, char_end_index):
    c = 0
    for w in sent[char_start_index: char_end_index + 1]:
        if w == " ":
            c += 1
    return c

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
    tokens = map(str, tokens)
    S_text = str(S_text)
    O_text = str(O_text)
    P = str(P)

    print P


    MAX_DIST = 10

    ''' 1. 使用种子去标记'''

    # print "tokens", type(tokens[0])
    # print "S_text", type(S_text)
    # print "O_text", type(O_text)
    # print "P", type(P)


    # 出现P对应的 S, O ==> 则标记为正例
    if (S_text, O_text) in dict_P_to_seeds[P]:
        yield [1, "pos: from seeds", " ".join((S_text, P, O_text))]

    # 互斥的P 对应的 S O ==> 则标记为负例
    similar_P_list = dict_P_to_similar_P_list[P]
    similar_P_list.append(P)
    for curr_P in dict_P_to_seeds:
        # 不在相似中,就是互斥的
        if curr_P not in similar_P_list:
            if (S_text, O_text) in dict_P_to_seeds[curr_P]:
                yield [-1, "neg: from seeds", " ".join((S_text, curr_P, O_text))]
                break

    '''2. 使用引导词去标记'''

    positive_guide_words = dict_P_to_guide_words[P]["positive"]
    negative_guide_words = dict_P_to_guide_words[P]["negative"]

    S_end_idx = min(S_end_index, O_end_index)
    O_start_idx = max(S_begin_index, O_begin_index)
    intermediate_tokens = tokens[S_end_idx+1:O_start_idx]

    # positive guide words
    positive_words = positive_guide_words.intersection(intermediate_tokens)
    if len(positive_words) > 0:
        yield [1, "pos: positive guide words between", " ".join(positive_words)]

    # negative guide words
    negative_words = negative_guide_words.intersection(intermediate_tokens)
    if len(negative_words) > 0:
        yield [-1, "neg: negative guide words between", " ".join(negative_words)]

    # 3. S O 之间的距离
    if len(intermediate_tokens) > MAX_DIST:
        yield [-1, "neg:far_apart", str(MAX_DIST)]



if __name__ == "__main__":
    main()
