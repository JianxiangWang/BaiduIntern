#!python/bin/python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
from heapq import heappush, heapreplace

def main():
    k = int(sys.argv[1])
    H = []

    for line in sys.stdin:
        x = line.strip().split("\t")[0]
        r = random.random()
        if len(H) < k:
            heappush(H, (r, x))
        elif r > H[0][0]:
            heapreplace(H, (r, x))

    for (r, x) in H:
        # by negating the id, the reducer receives the elements from highest to lowest
        print '%f\t%s' % (-r, x)



if __name__ == '__main__':
    main()