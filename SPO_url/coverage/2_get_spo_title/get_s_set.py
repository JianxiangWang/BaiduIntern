#  encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(fin):

    s_set = set()

    for line in fin:
        line_list = line.strip().split("\t")
        if len(line_list) == 1:
            continue

        # 获取第一个NER识别结果
        r = line_list[1][1:-1].strip()
        for x in r.split("  "):
            k, v = x.split(" : ", 1)

            if k == "name":
                s_set.add(v)
                break

    for s in sorted(s_set):
        print s

if __name__ == '__main__':
    main(sys.stdin)
