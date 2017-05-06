#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/3/26 13:32
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : exec01.py
import sys, os, time, datetime
from blaze import *

reload(sys)
sys.setdefaultencoding('utf-8')

def test1():
    d = data([(1, 'Alice', 100),
         (2, 'Bob', -200),
         (3, 'Charlie', 300),
         (4, 'Denis', 400),
         (5, 'Edith', -500)],
        fields=['id', 'name', 'balance'])
    # print d.peek()
    # print d.dshape

    print d[d.balance<0].name.peek()

def test2():
    # iris = data(utils.example('iris.csv'))
    iris = data('sqlite:///%s::iris' % (utils.example('iris.db')))
    print iris.peek()
    bl_goupy = by(iris.species, min=iris.petal_width.min(), max=iris.petal_width.max())
    print bl_goupy.peek()


if __name__=='__main__':
    print 'begin'.center(100, '-')
    test2()
    print ' end '.center(100, '-')