#!tools/python/bin/python
# coding: utf-8
import json
import uuid
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    for line in sys.stdin:
        line = json.loads(line)
        # mars_ner, 遍历, 判断是不是每一个s, o 都是 []
        # 是,则过滤掉
        flag = 0
        for P in line["mars_ner"]:

            s, o = line["mars_ner"][P]["s"], line["mars_ner"][P]["o"]
            if s != [] and o != []:
                flag = 1
                break
        # 需要的
        if flag == 1:
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

            S_O = json.dumps(line["mars_ner"], ensure_ascii=False)

            sent_sent = " ".join(new_tokens)

            print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                sent_id, sent_sent, tokens, pos_tags, ner_tags, dep_types, dep_tokens, S_O
            )



if __name__ == "__main__":
    main()
