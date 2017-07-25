#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from numpy import *
import operator

dataS=np.random.randint(5,size=(10,3))
b=[1,0,1,1,0,0,1,1,0,1]
data=[1.0,2.2,3.1]
dataSet=np.c_[dataS,b]
print dataSet

# def predict(dataSet, data, k):
dataSize =  dataS.shape[0]
css = tile(data,(dataSize,1))-dataS
sqlMat=css**2
distance=(sqlMat.sum(axis=1))**0.5
print distance
sorteddistance = distance.argsort()
print sorteddistance
classcount={}
for i in range(4):
    votelabel=b[sorteddistance[i]]
    classcount[votelabel]=classcount.get(votelabel,0)+1

print classcount
sortclass = sorted(classcount.items(),key=operator.itemgetter,reverse=True)
print sortclass[0][0]


