#!tools/python/bin/python
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json

def main():

    for line in sys.stdin:

        line_list = line.strip().split("\t")

        sent_id, sent_text, tokens, pos_tags, ner_tags, dep_types, dep_tokens,\
        S_O, depparser, dict_label_info_string = line_list

        dict_label_info = json.loads(dict_label_info_string)


        # 加载每个P的正负样本:
        for P in dict_label_info:
            for s_o in dict_label_info[P]["candidates"]:
                # 作为训练数据
                if dict_label_info[P]["candidates"][s_o]["wanted"] == 1:
                    s_string, o_string = s_o.split("|~|")

                    s_list = s_string.split("|_|")
                    s_list[-2] = int(s_list[-2])
                    s_list[-1] = int(s_list[-1])

                    o_list = o_string.split("|_|")
                    o_list[-2] = int(o_list[-2])
                    o_list[-1] = int(o_list[-1])


                    #  正例
                    label = dict_label_info[P]["candidates"][s_o]["label"]
                    if label > 0:
                        out_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (sent_text,
                                                                   json.dumps(s_list, ensure_ascii=False),
                                                                   P,
                                                                   json.dumps(o_list, ensure_ascii=False),
                                                                   "1",
                                                                    S_O,
                                                                   depparser,
                                                                    dict_label_info_string,

                                                                 )
                        print out_line

                    if label < 0:
                        out_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (sent_text,
                                                                   json.dumps(s_list, ensure_ascii=False),
                                                                   P,
                                                                   json.dumps(o_list, ensure_ascii=False),
                                                                   "-1",
                                                                    S_O,
                                                                   depparser,
                                                                   dict_label_info_string,

                                                                 )

                        print out_line


if __name__ == '__main__':
    main()