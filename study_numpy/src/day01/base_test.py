#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/3/22 17:26
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : base_test.py
# @Software: PyCharm
import sys, os, time, datetime
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8')

def test1():
    list_data = [21,1,2,3,4,5,6,7,8,9,10]
    np_data = np.array(list_data)
    np_data = np.sort(np_data)
    print np_data
    print np_data[int(0.1*len(np_data)):int(0.9*len(np_data))]

if __name__=='__main__':
    print 'begin'.center(100, '-')
    test1()
    print ' end '.center(100, '-')
