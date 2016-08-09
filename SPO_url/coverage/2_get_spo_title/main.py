# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(fin):
    for line in fin:
        title = line.strip().split("\t")[1]
        print title

if __name__ == '__main__':
    main(sys.stdin)