import sys
reload(sys)
sys.setdefaultencoding('utf-8')

for line in sys.stdin:
    print type(line.encode("utf-8"))