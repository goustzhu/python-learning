#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/6/6 22:59
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : TestCommon.py
import sys, os, time, datetime
from study_99other.spider_0731 import CommonUtil

reload(sys)
sys.setdefaultencoding('utf-8')

def test1():
    url = 'http://floor.0731fdc.com/?page=1&tsort=tdesc#sortname'
    result = CommonUtil.request_url(url)
    print result

def test():
    text = u'星城映象三期中小户型VIP2000抵5000\\'


if __name__=='__main__':
    print datetime.datetime.now(), 'begin'.center(80, '-')
    test()
    print datetime.datetime.now(), ' end '.center(80, '-')