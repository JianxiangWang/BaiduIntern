# coding: utf-8
import sys, json, codecs
reload(sys)
sys.setdefaultencoding('utf-8')

fin = codecs.open("P_list", encoding="utf-8")
small_train_data_P_set = set([])
for line in fin:
    small_train_data_P_set.add(line.strip())
fin.close()

# 对于label 为 0的, 去掉 neg:far_apart 这条规则
def main(in_file, to_file):
    fin = open(in_file)
    fout = open(to_file, "w")

    for line in fin:
        line_list = line.strip().split("\t")
        dict_label_info = json.loads(line_list[-1])

        flag = 0

        for P in dict_label_info:
            # 是我要处理的P
            if P in small_train_data_P_set:
                # 遍历candidates
                for s_o in dict_label_info[P]["candidates"]:
                    label = dict_label_info[P]["candidates"][s_o]["label"]
                    label_rule_list = dict_label_info[P]["candidates"][s_o]["label_info"]
                    # 是NULL类型的, 重新生成label
                    if label == 0:
                        # 去掉 neg: far  apart
                        label_rule_list = [[this_label, rule, info] for this_label, rule, info in label_rule_list
                                           if rule != "neg:far_apart"]
                        # 计算新的label
                        label = sum([x for x, _, _ in label_rule_list])

                        # 发生了变化
                        if label != 0:
                            print P, "%d --> %d" % (0, label)
                            print label_rule_list

                        # 给当前的dict重新复制
                        dict_label_info[P]["candidates"][s_o]["label"] = label
                        dict_label_info[P]["candidates"][s_o]["label_info"] = label_rule_list




        line_list[-1] = json.dumps(dict_label_info, ensure_ascii=False)
        fout.write("%s\n" % "\t".join(line_list))


    fin.close()
    fout.close()

# 对于label 为 0的, 去掉所有为负的规则
def main2(in_file, to_file):
    fin = open(in_file)
    fout = open(to_file, "w")

    for line in fin:
        line_list = line.strip().split("\t")
        dict_label_info = json.loads(line_list[-1])

        for P in dict_label_info:
            # 是我要处理的P
            if P in small_train_data_P_set:
                # 遍历candidates
                for s_o in dict_label_info[P]["candidates"]:
                    label = dict_label_info[P]["candidates"][s_o]["label"]
                    label_rule_list = dict_label_info[P]["candidates"][s_o]["label_info"]
                    # 是NULL类型的, 重新生成label
                    if label == 0:
                        # 去掉 neg: far  apart
                        label_rule_list = [[this_label, rule, info] for this_label, rule, info in label_rule_list
                                           if this_label > 0]
                        # 计算新的label
                        label = sum([x for x, _, _ in label_rule_list])

                        # 发生了变化
                        if label != 0:
                            print P, "%d --> %d" % (0, label), label_rule_list

                        # 给当前的dict重新复制
                        dict_label_info[P]["candidates"][s_o]["label"] = label
                        dict_label_info[P]["candidates"][s_o]["label_info"] = label_rule_list


        line_list[-1] = json.dumps(dict_label_info, ensure_ascii=False)
        fout.write("%s\n" % "\t".join(line_list))


    fin.close()
    fout.close()

# 重新定义规则的得分
def main3(in_file, to_file):
    fin = open(in_file)
    fout = open(to_file, "w")

    dict_rule_to_score = {
        "pos: from seeds": 4,
        "neg: from seeds": -4,
        "pos: positive guide words between": 2,
        "neg: negative guide words between": -2,
        "neg:far_apart": -1
    }

    for line in fin:
        line_list = line.strip().split("\t")
        dict_label_info = json.loads(line_list[-1])

        for P in dict_label_info:
            # 遍历candidates
            for s_o in dict_label_info[P]["candidates"]:
                label_rule_list = dict_label_info[P]["candidates"][s_o]["label_info"]
                # 新的
                label_rule_list = list(set([(dict_rule_to_score[rule], rule, info) for this_label, rule, info in label_rule_list]))
                label = sum([x for x, _, _ in label_rule_list])

                dict_label_info[P]["candidates"][s_o]["label"] = label
                dict_label_info[P]["candidates"][s_o]["label_info"] = label_rule_list

        line_list[-1] = json.dumps(dict_label_info, ensure_ascii=False)
        fout.write("%s\n" % "\t".join(line_list))

    fin.close()
    fout.close()


if __name__ == "__main__":
    in_file = "../../data/SPO_train_data_for_deepdive_label"
    to_file = "../../data/SPO_train_data_for_deepdive_label_post_processing_new_rule_score"
    main3(in_file, to_file)


