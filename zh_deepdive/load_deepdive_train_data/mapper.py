#!tools/python/bin/python
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json

def main():

    for line in sys.stdin:

        line_list = line.strip().split("\t")
        sent_id, _, tokens, pos_tags, ner_tags, dep_types, dep_tokens,\
        S_O, dict_label_info_string = line_list

        dict_SO = json.loads(S_O)
        dict_T ={}
        for P in dict_SO:
            for name, T, offset, length in dict_SO[P]["s"] + dict_SO[P]["s"]:
                   dict_T[(name, offset, length)] = T

        # to_token_list
        tokens = unicode(tokens)
        token_list = tokens[1:-1].split(",")
        sent_text = " ".join(token_list)



        dict_label_info = json.loads(dict_label_info_string)

        # 过滤一下SO识别
        dict_so = json.loads(S_O)
        dict_so_new = {}
        for P in dict_so:
            if P in dict_label_info:
                dict_so_new[P] = dict_so[P]
        dict_so_new_string = json.dumps(dict_so_new, ensure_ascii=False)

        # 加载每个P的正负样本:
        for P in dict_label_info:
            for s_o in dict_label_info[P]["candidates"]:
                # 作为训练数据
                if dict_label_info[P]["candidates"][s_o]["wanted"] == 1:
                    S_id, S_text, O_id, O_text = s_o.split("|~|")
                    label = dict_label_info[P]["candidates"][s_o]["label"]

                    S_start_index, S_end_index = S_id.split("_")[-2:]
                    O_start_index, O_end_index = O_id.split("_")[-2:]

                    S_offset, S_length = get_char_offset(token_list, int(S_start_index), int(S_end_index))
                    O_offset, O_length = get_char_offset(token_list, int(O_start_index), int(O_end_index))

                    if (S_text, S_offset, S_length) not in dict_T:
                        continue
                    S_T = dict_T[(S_text, S_offset, S_length)]

                    if (O_text, O_offset, O_length) not in dict_T:
                        continue
                    O_T = dict_T[(O_text, O_offset, O_length)]

                    s = [S_text, S_T, S_offset, S_length]
                    o = [O_text, O_T, O_offset, O_length]


                    #  正例
                    if label > 0:
                        out_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (sent_text,
                                                                   json.dumps(s),
                                                                   P,
                                                                   json.dumps(o),
                                                                   "1",
                                                                    dict_so_new_string,
                                                                    dict_label_info_string,

                                                                 )
                        print out_line

                    if label < 0:
                        out_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (sent_text,
                                                                   json.dumps(s),
                                                                   P,
                                                                   json.dumps(o),
                                                                   "-1",
                                                                    dict_so_new_string,
                                                                    dict_label_info_string,

                                                                 )

                        print out_line








def get_char_offset(token_list, token_start_index, token_end_index):
    offset = 0
    for token in token_list[:token_start_index]:
        offset += len(token) + 1
    length = 0
    for token in token_list[token_start_index: token_end_index]:
        length += len(token) + 1
    length += len(token_list[token_end_index])

    return offset, length





# def get_char_offset(sent_text, token_list, token_start_index, token_end_index):
#     start_offset = -1
#     for token in token_list[:token_start_index+1]:
#         start_offset = sent_text.find(token, start_offset + 1)
#
#     end_offset = -1
#     for token in token_list[:token_end_index+1]:
#         end_offset = sent_text.find(token, end_offset + 1)
#     end_offset += len(token_list[token_end_index])
#
#     length = end_offset - start_offset
#
#     return start_offset, length

if __name__ == '__main__':
    main()