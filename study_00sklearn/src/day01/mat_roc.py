#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/3/28 8:54
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : mat_roc.py
import sys, os, time, datetime

reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np
import matplotlib.pyplot as plt

def plotROC(predScore, labels):
    point = (1.0, 1.0) #由于下面排序的索引是从小到大，所以这里从(1,1)开始绘制
    ySum = 0.0
    numPos = np.sum(np.array(labels)==1.0)
    numNeg = len(labels)-numPos
    yStep = 1/np.float(numPos)
    xStep = 1/np.float(numNeg)
    sortedIndex = predScore.argsort() #对predScore进行排序，的到排序索引值
    fig = plt.figure()
    fig.clf()
    ax = plt.subplot(111)
    for index in sortedIndex.tolist()[0]:
        if labels[index] == 1.0: #如果正样本各入加1，则x不走动，y往下走动一步
            delX = 0
            delY = yStep
        else:                   #否则，x往左走动一步，y不走动
            delX = xStep
            delY = 0
            ySum += point[1]     #统计y走动的所有步数的和
        ax.plot([point[0], point[0] - delX], [point[1], point[1] - delY],c='b')
        point = (point[0] - delX, point[1] - delY)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False positive rate'); plt.ylabel('True positive rate')
    plt.title('ROC Curve')
    ax.axis([0, 1, 0, 1])
    plt.show()
    #最后，所有将所有矩形的高度进行累加，最后乘以xStep得到的总面积，即为AUC值
    print "the Area Under the Curve is: ", ySum * xStep

if __name__=='__main__':
    print 'begin'.center(100, '-')
    label = [1, 1, -1, -1]
    pre =np.array( [0.1, 0.4, 0.35, 0.8])
    plotROC(pre, label)
    print ' end '.center(100, '-')