#!tools/python/bin/python
# coding: utf-8
import json
import uuid
import sys
import cPickle
reload(sys)
sys.setdefaultencoding('utf-8')

# 少一些规则
def main():

    MAX_SENT_LENGTH = 400

    for line in sys.stdin:
        line = json.loads(line)
        # 闯关啦~~~

        sent_id = "test_" + str(uuid.uuid1())
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

            # # 判断句子长度
            # sent_length = len(line["depparser"])
            # if sent_length >= MAX_SENT_LENGTH:
            #     continue

            # 不为空
            if s_list == [] or o_list == []:
                continue

            # # 获取SO对应的mention的个数
            # num_mention = len(set(s_list + o_list))
            # if num_mention <= 1 or num_mention >= 5:
            #     continue


            # to mention_list
            # s_list = [("刘德华", "PER", 0, 3), ...] == > [(mention_id, mention_text, sent_id, begin_index, end_index), ...]
            s_mention_list = []
            for s in s_list:
                mention = _get_mention(line, sent_id, tokens, s)
                if mention:
                    s_mention_list.append(mention)

            o_mention_list = []
            for o in o_list:
                mention = _get_mention(line, sent_id, tokens, o)
                if mention:
                    o_mention_list.append(mention)

            # 去重, 真的有重复的 !!!!
            s_mention_list = list(set(s_mention_list))
            o_mention_list = list(set(o_mention_list))

            # 判断so pair 能不能被标注
            for s_mention in s_mention_list:
                for o_mention in o_mention_list:
                    # # 不能相同, surface level
                    # if s_mention[1] == o_mention[1]:
                    #     continue

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

            # print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            #     sent_id, sent_sent, tokens, pos_tags, ner_tags, dep_types, dep_tokens, S_O,
            #     json.dumps(dict_label_info, ensure_ascii=False)
            # )



# s: ("刘德华", "PER", 0, 3)
# return (mention_id, mention_text, sent_id, begin_index, end_index)
def _get_mention(line, sent_id, tokens, s):
    so_mention_text, _,  char_start_index, char_length = s

    sent = line["sentence"]
    before_space_count = space_count(sent, 0, char_start_index)
    in_space_count = space_count(sent, char_start_index, char_start_index + char_length -1)

    #
    char_start_index = char_start_index - before_space_count
    char_length = char_length - in_space_count


    begin_index, end_index = _get_begin_index_and_end_index(tokens, char_start_index, char_length)

    if begin_index and end_index:
        mention_id = "%s_%d_%d" % (sent_id, begin_index, end_index)
        mention_text = " ".join([tokens[index] for index in range(begin_index, end_index + 1)])
        mention_text_ = "".join([tokens[index] for index in range(begin_index, end_index + 1)])



        if set(unicode(mention_text_)) & set(unicode(so_mention_text)) == set([]):
            print "==" * 40
            print so_mention_text, mention_text_
            print " ".join(tokens)
            print line["sentence"]
            print so_mention_text, char_start_index, char_length

        # token对应的mention 与 so 识别的mention, 至少得有交集
        if set(unicode(mention_text_)) & set(unicode(so_mention_text)) :
            return (mention_id, mention_text, sent_id, begin_index, end_index)

    return None


# [char_start_index, char_end_index]
def space_count(sent, char_start_index, char_end_index):
    c = 0
    for w in sent[char_start_index: char_end_index + 1]:
        if w == [" "]:
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

    yield [-1, "test data", "test data"]



if __name__ == "__main__":
    main()
