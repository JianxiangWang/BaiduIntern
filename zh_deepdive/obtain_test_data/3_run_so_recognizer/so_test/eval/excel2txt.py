#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import xlrd

reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: %s excel_file" % sys.argv[0]
    exit(-1)

work_book = xlrd.open_workbook(sys.argv[1])


for i in range(work_book.nsheets):
    file_name = str(i+1) + '.txt'
    with open(file_name, 'wb+') as out_file:
        sh = work_book.sheet_by_index(i)
        for idx_row in range(sh.nrows):
            print >> out_file,  u'\t'.join(map(lambda x:unicode(x.value).strip('\r\n'), sh.row(idx_row))).encode('gb18030')

