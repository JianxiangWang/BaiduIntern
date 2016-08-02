#!/bin/bash

python excel2txt.py 每个P抽2个模型预测为正的SPO进行分析.xlsx
cat 1.txt | iconv -f gb18030 -t utf8 | tail -n +2 >tmp

