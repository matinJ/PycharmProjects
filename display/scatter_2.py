#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
from numpy import zeros


def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)         #get the number of lines in the file
    returnMat = zeros((numberOfLines,2))        #prepare matrix to return
    # classLabelVector = []                       #prepare labels return
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:2]
        # classLabelVector.append(str(listFromLine[-1]))
        index += 1
    fr.close()
    # return returnMat,classLabelVector
    return returnMat

# matrix, labels = file2matrix('datingTestSet.txt')
matrix=file2matrix("result.txt")
# print matrix
x=matrix[:,1]
y=matrix[:,0]
T=np.arctan2(x,y)
plt.figure(figsize=(16,12))
plt.scatter(x,y,c='r',s=5,alpha=0.8,marker='.')

plt.show()