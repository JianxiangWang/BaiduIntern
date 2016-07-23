#!/bin/sh

cd tools
source load_var.sh
python/bin/python iconv.py utf-8 gb18030 | python/bin/python depparser_uni_client_sync.py | python/bin/python iconv.py gb18030 utf8