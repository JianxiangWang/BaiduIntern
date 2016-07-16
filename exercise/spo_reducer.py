#!/usr/bin/env python2.7
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from itertools import groupby

def read_mapper_output(file, separator='\t'):
    for line in file:
        # (spo, "sent|~|fromUrl|~|confidence")
        yield line.rstrip().split(separator, 1)

def main(separator='\t'):
    data = read_mapper_output(sys.stdin, separator=separator)

    for spo, group in groupby(data, lambda x: x[0]):
        # 遍历每一组
        visited = set()
        results = []
        for _, x in group:
            sentence, fromUrl, confidence = x.split("|~|")

            if sentence in visited:
                continue
            visited.add(sentence)

            results.append("|~|".join([sentence, fromUrl, confidence]))

        #
        print "%s\t%s" % (spo, "|#|".join(results))


if __name__ == "__main__":
    main()
