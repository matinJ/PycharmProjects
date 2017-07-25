#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import numpy as np
from sklearn import metrics
from sklearn import preprocessing
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB


def load_data():
    url="http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
    raw_data=urllib.urlopen(url)
    dataSet = np.loadtxt(raw_data,delimiter=",")
    return dataSet[:,0:7], dataSet[:,8]


def normalized(X):
    normalized_X = preprocessing.normalize(X)
    standardized_X = preprocessing.scale(X)
    return normalized_X, standardized_X

def Feature_select(X,y):
    model = ExtraTreesClassifier()
    model.fit(X,y)
    print (model.feature_importances_)

def logisticReg(X,y):
    model = LogisticRegression()
    model.fit(X,y)
    print (model)
    expected = y
    predicted = model.predict(X)
    print (metrics.classification_report(expected,predicted))
    print (metrics.confusion_matrix(expected,predicted))

def bayes(X,y):
    model = GaussianNB()
    model.fit(X,y)
    expected  =y
    predicted = model.predict(X)
    print(metrics.classification_report(expected,predicted))
    print(metrics.confusion_matrix(expected,predicted))

