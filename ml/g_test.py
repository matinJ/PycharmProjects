#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from numpy import genfromtxt


def getData(dataSet):
    m, n = np.shape(dataSet)
    trainData = np.ones((m, n))
    trainData[:,:-1] = dataSet[:,:-1]
    trainLabel = dataSet[:,-1]
    return trainData, trainLabel

def batchGradientDescent(x, y, theta, alpha, m, maxIterations):
    xTrains = x.transpose()
    for i in range(0, maxIterations):
        hypothesis = np.dot(x, theta)
        loss = hypothesis - y
        gradient = np.dot(xTrains, loss) / m #m为样本数
        theta = theta - alpha * gradient
    return theta

def predict(x, theta):
    m, n = np.shape(x)
    xTest = np.ones((m, n+1))
    xTest[:, :-1] = x
    yP = np.dot(xTest, theta)
    return yP

dataPath = r"g_test.csv"
dataSet = genfromtxt(dataPath, delimiter=',')
trainData, trainLabel = getData(dataSet)
m, n = np.shape(trainData)
theta = np.ones(n)
alpha = 0.1
maxIteration = 5000
theta = batchGradientDescent(trainData, trainLabel, theta, alpha, m, maxIteration)
x = np.array([[3.1, 5.5], [3.3, 5.9], [3.5, 6.3], [3.7, 6.7], [3.9, 7.1]])
print predict(x, theta)