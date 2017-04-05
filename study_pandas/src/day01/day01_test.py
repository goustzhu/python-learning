#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/3/22 17:40
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : base_test.py
# @Software: PyCharm
import sys, os, time, datetime
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

def test1():
    # list_data = [('a',12), ('b',14), ('c',13), ('d',14), ('e',5), ('f',6), ('g',7),
    #              ('a',8), ('b',19), ('c',10), ('d',11), ('e',12), ('f',13), ('g',14),
    #              ('a',15), ('b',16), ('c',17), ('d',18), ('e',21), ('f',20)]
    # df_data = pd.DataFrame(list_data, columns=['name', 'age'])
    list_data = [5.2, 7.3, 9.2, 3.6, 5.5, 8.8, 4.6, 3.9, 4.4, 5.2, 6.1,
                 4.2, 4.2, 3.9, 4.5, 5.0, 4.4, 16, 5.8, 6.3, 8.5, 5.3, 6.6, 5.8, 6.1]
    df_data = pd.DataFrame(list_data, columns=[ 'age'])
    # desc_data = df_data['age'].describe()
    a_min, d_min, d_max, a_max = df_data['age'].quantile([ 0, 0.1, 0.9, 1])
    print a_min, d_min, d_max, a_max
    print df_data[(df_data['age']>=d_min) & (df_data['age']<=d_max)]

def test2():
    list_data = [('a',12), ('b',14), ('c',13), ('d',14), ('e',5), ('f',6), ('g',7),
                 ('a',8), ('b',19), ('c',10), ('d',11), ('e',12), ('f',13), ('g',14),
                 ('a',15), ('b',16), ('c',17), ('d',18), ('e',21), ('f',20)]
    df_data = pd.DataFrame(list_data, columns=['name', 'age'])
    df_group_by = df_data.groupby(by=['name'], as_index=False).count()
    print df_group_by
    # for name in df_group_by:

if __name__=='__main__':
    print 'begin'.center(100, '-')
    test2()
    print ' end '.center(100, '-')
