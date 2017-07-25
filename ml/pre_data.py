#!/usr/bin/python
# -*- coding: utf-8 -*-
import random


def split_data(data, prop):
    resutls = [],[]
    for row in data:
        resutls[0 if random.random()<prop else 1].append(row)

def accuracy(tp, fp, fn, tn):
    correct = tp + tn
    total = tp + fp + fn +tn
    return correct/total #准确率

def precision(tp, fp, fn, tn):
    return tp/(tp+fp) #查准率

def recall(tp, fp, fn, tn):
    return tp/(tp+fn) #查全率,召回率

def f1_score(tp, fp, fn, tn):
    p = precision(tp, fp, fn, tn)
    r = recall(tp, fp, fn, tn)
    return 2*p*r/(p+r)  # F1得分,是查准率和查全率的调和平均值,必落在两者中间

