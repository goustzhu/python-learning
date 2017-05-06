#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/3/28 8:38
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : recommend_result.py
import sys, os, time, datetime

reload(sys)
sys.setdefaultencoding('utf-8')

def test1():
    import numpy as np
    from sklearn import metrics
    y = np.array([1, 1, 2, 2])
    pred = np.array([0.1, 0.4, 0.35, 0.8])
    fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=2)
    metrics.auc(fpr, tpr)

if __name__=='__main__':
    print 'begin'.center(100, '-')
    test1()
    print ' end '.center(100, '-')