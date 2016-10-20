#!python/bin/python
import sys


def main():
    k = int(sys.argv[1])
    c = 0

    for line in sys.stdin:
        (r, x) = line.strip().split('\t', 1)
        print x
        c += 1
        if c == k:
            break


if __name__ == '__main__':
    main()