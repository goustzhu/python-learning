#!/usr/bin/Python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/4 16:50
# @Author  : goustzhu <goustzhu@gmail.com>
# @Site    : 
# @File    : GeneralizedLinearModels.py
# @Software: PyCharm
'''
1.1. Generalized Linear Models
 @y 预测值
 y(w,x) = w_0+w_1*x_1+...+w_n*x_n
 其中，w=[w_0, w_1,..., w_n] 模型系数， x=[x_1,..., x_n] 为样本数据
 其中 w_1,..., w_n 记作为 coef_, w_0 记作为 intercept_
'''
import sys, os, time, datetime

reload(sys)
sys.setdefaultencoding('utf-8')

def test1():
    '''
    1.1.1. Ordinary Least Squares
        LinearRegression fits a linear model with coefficients w = (w_1, ..., w_p)
        to minimize the residual sum of squares between the observed responses in the dataset,
        and the responses predicted by the linear approximation. Mathematically it solves a problem of the form:
                            min||Xw-y||^2
    :return:
    '''
    from sklearn import linear_model
    reg = linear_model.LinearRegression()
    reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
    print reg, reg.coef_, reg.intercept_

def test2():
    '''
    1.1.2. Ridge Regression
        Ridge regression addresses some of the problems of Ordinary Least Squares by imposing a penalty
        on the size of coefficients. The ridge coefficients minimize a penalized residual sum of squares,
                        min||Xw-y||^2+ \alpha||w||^2
        Here, \alpha >= 0 is a complexity parameter that controls the amount of shrinkage:
        the larger the value of \alpha, the greater the amount of shrinkage and thus the coefficients become more robust to collinearity.
    RidgeCV implements ridge regression with built-in cross-validation of the alpha parameter.
        The object works in the same way as GridSearchCV except that it defaults to Generalized Cross-Validation (GCV),
        an efficient form of leave-one-out cross-validation:
    :return:
    '''
    from sklearn import linear_model
    # reg = linear_model.Ridge(alpha=.5)
    reg = linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0])
    reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
    print reg, reg.coef_, reg.intercept_

def test3():
    '''
    1.1.3. Lasso
    The Lasso is a linear model that estimates sparse coefficients. It is useful in some contexts due to its tendency
        to prefer solutions with fewer parameter values, effectively reducing the number of variables upon which the
        given solution is dependent. For this reason, the Lasso and its variants are fundamental to the field of
        compressed sensing. Under certain conditions, it can recover the exact set of non-zero weights
        (see Compressive sensing: tomography reconstruction with L1 prior (Lasso)).
    Mathematically, it consists of a linear model trained with \ell_1 prior as regularizer.
        The objective function to minimize is:
                    min(1/2n)||Xw-y||^2+ \alpha ||w||
    :return:
    '''
    from sklearn import linear_model
    reg = linear_model.Lasso(alpha=0.2)
    # reg.fit([[0,0],[1,1]],[0,1])
    reg.fit([[0, 0], [1, 1], [2, 2], [3, 3]], [0, 1, 2, 3])
    print reg, reg.coef_, reg.intercept_
    result = reg.predict([[2,2]])
    print result

if __name__=='__main__':
    print 'begin'.center(100, '-')
    test3()
    print " end ".center(100, '-')
