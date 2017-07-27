#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.datasets import load_iris

iris = load_iris()
# print iris
print iris['target'].shape
rf = RandomForestRegressor() #默认参数设置
rf.fit(iris.data[:150],iris.target[:150]) #模型训练

#随机挑选两个预测不相同的样本
instance=iris.data[[100,109]]
print instance
print 'instance 0 prediction:', rf.predict(instance[0])
print 'instance 1 prediction:' ,rf.predict(instance[1])
print iris.target[100],iris.target[109]


#这段代码将会提示我们各个特征的贡献，可以让我们知道部分内部的结构
from sklearn.cross_validation import cross_val_score, ShuffleSplit
X = iris["data"]
Y = iris["target"]
print Y
names = iris["feature_names"]
rf = RandomForestRegressor()
scores = []
for i in range(X.shape[1]):
    score = cross_val_score(rf, X[:, i:i+1], Y, scoring="r2",
                            cv=ShuffleSplit(len(X), 3, .3))
    scores.append((round(np.mean(score), 3), names[i]))
print sorted(scores, reverse=True)