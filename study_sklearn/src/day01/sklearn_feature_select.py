#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/4/5 11:39
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : sklearn_feature_select.py
# @Software: PyCharm
import sys, os, time, datetime
import blaze

reload(sys)
sys.setdefaultencoding('utf-8')

def test1():
    '''
    4.1 平均不纯度减少 mean decrease impurity

    随机森林由多个决策树构成。决策树中的每一个节点都是关于某个特征的条件，为的是将数据集按照不同的响应变量一分为二。
    利用不纯度可以确定节点（最优条件），对于分类问题，通常采用基尼不纯度或者信息增益，对于回归问题，通常采用的是方差或
    者最小二乘拟合。当训练决策树的时候，可以计算出每个特征减少了多少树的不纯度。对于一个决策树森林来说，可以算出每个特
    征平均减少了多少不纯度，并把它平均减少的不纯度作为特征选择的值。

    Scores for X0, X1, X2: [0.278, 0.66, 0.062]

    当计算特征重要性时，可以看到X1的重要度比X2的重要度要高出10倍，但实际上他们真正的重要度是一样的。尽管数据量已经很大
    且没有噪音，且用了20棵树来做随机选择，但这个问题还是会存在。

    需要注意的一点是，关联特征的打分存在不稳定的现象，这不仅仅是随机森林特有的，大多数基于模型的特征选择方法都存在这个问题。
    :return:
    '''
    from sklearn.datasets import load_boston
    from sklearn.ensemble import RandomForestRegressor
    # Load boston housing dataset as an example
    boston = load_boston()
    # print boston
    X = boston["data"]
    Y = boston["target"]
    names = boston["feature_names"]
    rf = RandomForestRegressor()
    rf.fit(X, Y)
    print "RandomForestRegressor Features sorted by their score:"
    print sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names),
                 reverse=True)

def test2():
    '''
    4.2 平均精确率减少 Mean decrease accuracy

    另一种常用的特征选择方法就是直接度量每个特征对模型精确率的影响。主要思路是打乱每个特征的特征值顺序，并且度量顺序变
    动对模型的精确率的影响。很明显，对于不重要的变量来说，打乱顺序对模型的精确率影响不会太大，但是对于重要的变量来说，
    打乱顺序就会降低模型的精确率。

    这个方法sklearn中没有直接提供，但是很容易实现，下面继续在波士顿房价数据集上进行实现。

    在这个例子当中，LSTAT和RM这两个特征对模型的性能有着很大的影响，打乱这两个特征的特征值使得模型的性能下降了73%和57%。
    注意，尽管这些我们是在所有特征上进行了训练得到了模型，然后才得到了每个特征的重要性测试，这并不意味着我们扔掉某个或
    者某些重要特征后模型的性能就一定会下降很多，因为即便某个特征删掉之后，其关联特征一样可以发挥作用，让模型性能基本上不变。
    :return:
    '''
    import numpy as np
    from sklearn.datasets import load_boston
    from sklearn.ensemble import RandomForestRegressor

    from sklearn.cross_validation import ShuffleSplit
    from sklearn.metrics import r2_score
    from collections import defaultdict

    boston = load_boston()
    X = boston["data"]
    Y = boston["target"]
    names = boston["feature_names"]

    rf = RandomForestRegressor()
    scores = defaultdict(list)

    # crossvalidate the scores on a number of different random splits of the data
    for train_idx, test_idx in ShuffleSplit(len(X), 100, .3):
        X_train, X_test = X[train_idx], X[test_idx]
        Y_train, Y_test = Y[train_idx], Y[test_idx]
        r = rf.fit(X_train, Y_train)
        acc = r2_score(Y_test, rf.predict(X_test))
        for i in range(X.shape[1]):
            X_t = X_test.copy()
            np.random.shuffle(X_t[:, i])
            shuff_acc = r2_score(Y_test, rf.predict(X_t))
            scores[names[i]].append((acc - shuff_acc) / acc)
    print "Features sorted by their score:"
    print sorted([(round(np.mean(score), 4), feat) for
                  feat, score in scores.items()], reverse=True)

def testblaze():
    from sklearn import datasets
    iris = datasets.load_iris()
    iris_data = iris['data']
    iris_cols = iris['feature_names']
    bz_data = blaze.DataFrame(iris_data, columns=iris_cols)
    print bz_data
    print iris_cols

def test3():
    '''
    5.1 稳定性选择 Stability selection

    稳定性选择是一种基于二次抽样和选择算法相结合较新的方法，选择算法可以是回归、SVM或其他类似的方法。它的主要思想是在不
    同的数据子集和特征子集上运行特征选择算法，不断的重复，最终汇总特征选择结果，比如可以统计某个特征被认为是重要特征的
    频率（被选为重要特征的次数除以它所在的子集被测试的次数）。理想情况下，重要特征的得分会接近100%。稍微弱一点的特征得
    分会是非0的数，而最无用的特征得分将会接近于0。

    sklearn在随机lasso和随机逻辑回归中有对稳定性选择的实现。
    :return:
    '''
    from sklearn.linear_model import RandomizedLasso
    from sklearn.datasets import load_boston
    boston = load_boston()

    # using the Boston housing data.
    # Data gets scaled automatically by sklearn's implementation
    X = boston["data"]
    Y = boston["target"]
    names = boston["feature_names"]

    rlasso = RandomizedLasso(alpha=0.025)
    rlasso.fit(X, Y)

    print "Features sorted by their score:"
    print sorted(zip(map(lambda x: round(x, 4), rlasso.scores_),
                     names), reverse=True)

def test4():
    '''
    5.2 递归特征消除 Recursive feature elimination (RFE)

    递归特征消除的主要思想是反复的构建模型（如SVM或者回归模型）然后选出最好的（或者最差的）的特征（可以根据系数来选），
    把选出来的特征放到一遍，然后在剩余的特征上重复这个过程，直到所有特征都遍历了。这个过程中特征被消除的次序就是特征的排序。
    因此，这是一种寻找最优特征子集的贪心算法。

    RFE的稳定性很大程度上取决于在迭代的时候底层用哪种模型。例如，假如RFE采用的普通的回归，没有经过正则化的回归是不稳定的，
    那么RFE就是不稳定的；假如采用的是Ridge，而用Ridge正则化的回归是稳定的，那么RFE就是稳定的。

    Sklearn提供了RFE包，可以用于特征消除，还提供了RFECV，可以通过交叉验证来对的特征进行排序。
    :return:
    '''
    from sklearn.feature_selection import RFE
    from sklearn.datasets import load_boston
    from sklearn.linear_model import LinearRegression

    boston = load_boston()
    X = boston["data"]
    Y = boston["target"]
    names = boston["feature_names"]

    # use linear regression as the model
    lr = LinearRegression()
    # rank all features, i.e continue the elimination until the last one
    rfe = RFE(lr, n_features_to_select=1)
    rfe.fit(X, Y)

    print "Features sorted by their rank:"
    print sorted(zip(map(lambda x: round(x, 4), rfe.ranking_), names))

def test5():
    '''

    :return:
    '''
    import numpy as np
    from sklearn.metrics import mean_squared_error
    from sklearn.datasets import make_friedman1
    from sklearn.ensemble import GradientBoostingRegressor

    X, y = make_friedman1(n_samples=1200, random_state=0, noise=1.0)
    X_train, X_test = X[:200], X[200:]
    y_train, y_test = y[:200], y[200:]
    est = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,
                                    max_depth=1, random_state=0, loss='ls').fit(X_train, y_train)
    print mean_squared_error(y_test, est.predict(X_test))

if __name__=='__main__':
    print 'begin'.center(100, '-')
    test5()
    print ' end '.center(100, '-')
