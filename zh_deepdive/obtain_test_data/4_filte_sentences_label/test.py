# encoding: utf-8

import json
import uuid




# 统计一下, so 全部为 []的个数
def main(in_file):

    count = 0

    for line in open(in_file):
        line = json.loads(line)

        sent_id = "test_" + str(uuid.uuid1())
        sent_text = line["sentence"]
        markup = line["depparser"]

        tokens      = [item[1] for item in markup]
        pos_tags    = [item[4] for item in markup]
        ner_tags    = [item[5] for item in markup]
        dep_types   = [item[-1] for item in markup]
        dep_tokens  = [item[-2] for item in markup]

        flag = 0
        for P in line["mars_ner"]:
            s_list, o_list = line["mars_ner"][P]["s"], line["mars_ner"][P]["o"]

            # 不为空
            if s_list != [] and o_list != []:

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

                # 不为空
                if s_mention_list != [] and o_mention_list != []:
                    flag = 1


        if flag == 0:
            print sent_text
            count += 1

    print count

# s: ("刘德华", "PER", 0, 3)
# return (mention_id, mention_text, sent_id, begin_index, end_index)
def _get_mention(sent_text, sent_id, tokens, s):

    # 需要修改 char_start_index, char_length, 因为他计算了空格
    so_mention_text, _,  char_start_index, char_length = s

    before_space_count = space_count(sent_text, 0, char_start_index)
    in_space_count = space_count(sent_text, char_start_index, char_start_index + char_length -1)

    #
    char_start_index = char_start_index - before_space_count
    char_length = char_length - in_space_count


    begin_index, end_index = _get_begin_index_and_end_index(tokens, char_start_index, char_length)

    if begin_index and end_index:
        mention_id = "%s_%d_%d" % (sent_id, begin_index, end_index)
        mention_text = " ".join([tokens[index] for index in range(begin_index, end_index + 1)])
        mention_text_ = "".join([tokens[index] for index in range(begin_index, end_index + 1)])

        # token对应的mention 与 so 识别的mention, 至少得有交集
        if set(unicode(mention_text_)) & set(unicode(so_mention_text)) :
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

if __name__ == '__main__':
    main("part-00000")
