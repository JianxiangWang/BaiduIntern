#!/usr/bin/env bash

INPUT=${1}

./classify2readable `wdbtools-pc/getone.sh ${INPUT} PageClassify realtime | grep -a "^PageClassify" | awk '{print $NF}'`