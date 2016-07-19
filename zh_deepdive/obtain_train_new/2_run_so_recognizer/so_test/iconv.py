#!/bin/env python
# -*- coding:utf8 -*-

import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) != 3:
    print >> sys.stderr, "Usage: %s from_code to_code" % sys.argv[0]
    exit(0)

from_code = sys.argv[1]
to_code = sys.argv[2]

for line in sys.stdin:
    line = line.decode(from_code, errors = 'ignore').strip('\r\n')
    print line.encode(to_code)

