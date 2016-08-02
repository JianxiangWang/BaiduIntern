#!/usr/bin/env bash

[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"

# 吧
cat $input | ba/main.py
cat $input | shipin/main.py