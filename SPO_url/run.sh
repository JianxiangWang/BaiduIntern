#!/usr/bin/env bash

#[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"


while read line
do
  echo ${line}
  echo ${line} | ba/main.py
  echo ${line} | shipin/main.py
done
