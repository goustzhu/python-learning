#!/usr/bin/Python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/4 16:05
# @Author  : goustzhu
# @Site    : 
# @File    : PlotCrossValidatedPredictions.py
# @Software: PyCharm
'''
 link: http://scikit-learn.org/stable/auto_examples/plot_cv_predict.html#sphx-glr-auto-examples-plot-cv-predict-py
'''
import sys, os, time, datetime

reload(sys)
sys.setdefaultencoding('utf-8')

def test1():
    from sklearn import datasets
    from sklearn.model_selection import cross_val_predict
    from sklearn import linear_model
    import matplotlib.pyplot as plt

    lr = linear_model.LinearRegression()
    boston = datasets.load_boston()
    y = boston.target

    # cross_val_predict returns an array of the same size as `y` where each entry
    # is a prediction obtained by cross validation:
    predicted = cross_val_predict(lr, boston.data, y, cv=10)

    fig, ax = plt.subplots()
    ax.scatter(y, predicted)
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.show()

if __name__=='__main__':
    print 'begin'.center(100, '-')
    test1()
    print ' end '.center(100, '-')
