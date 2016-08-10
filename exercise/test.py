#!/usr/bin/env python
# coding: utf-8
import sys
from time import sleep
reload(sys)
sys.setdefaultencoding('utf-8')


def A(x):

    def B():
        print x

    B()

A(1)

