import sys
from PageClassify import PageClassify

p = PageClassify('prepared')
for line in sys.stdin:
    url = line.strip()
    p.predict(url)