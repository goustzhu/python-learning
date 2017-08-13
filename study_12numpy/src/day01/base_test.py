#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/3/22 17:26
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : base_test.py
# @Software: PyCharm
import sys, os, time, datetime
import numpy as np
import scipy as sp
from scipy import stats

reload(sys)
sys.setdefaultencoding('utf-8')

def test1():
    list_data = [21,1,2,3,4,5,6,7,8,9,10]
    np_data = np.array(list_data)
    np_data = np.sort(np_data)
    print np_data
    print np_data[int(0.1*len(np_data)):int(0.9*len(np_data))]

def test():
    np_data = np.array([12.6, 13.4, 12.8, 13.2])
    mean = np.mean(np_data)
    std = np.std(np_data)
    alpha = 0.05
    z_score = stats.norm.pdf(alpha)
    print mean, std, z_score

if __name__=='__main__':
    print 'begin'.center(100, '-')
    test()
    print ' end '.center(100, '-')
