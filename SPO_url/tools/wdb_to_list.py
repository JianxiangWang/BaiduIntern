import sys


def main():
    s = []
    flag = 0
    for line in sys.stdin:
        line = line.strip()

        if line == "--- beg ---":
            flag = 1
            continue
        if line == "--- end ---":
            break

        if flag == 1:
            s.append(line)

    print "[" + ", ".join(['%s' % x for x in s]) + "]"
