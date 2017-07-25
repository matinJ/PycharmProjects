#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import operator

def file2matrix(filename):
    fr = open(filename)
    arrayOlines = fr.readlines()
    numberOflines  =len(arrayOlines)
    returnMat = zeros((numberOflines,3))
    classLabelVector=[]
    index = 0
    for line in arrayOlines:
        line = line.strip() #去掉开头换行符
        listFromline = line.split('\t')
        returnMat[index,:] = listFromline[0:3]
        classLabelVector.append(int(listFromline[-1]))
        index+=1
    return returnMat,classLabelVector

#归一化特征
def autoNorm(dataSet):
    #将每列的最小值放在minVals中
    minVals = dataSet.min(0)
    #将每列的最大值放在maxVals中
    maxVals = dataSet.max(0)
    #计算可能的取值范围
    ranges=maxVals-minVals
    #创建新的返回矩阵
    normDataSet = zeros(shape(dataSet))
    #得到数据集的行数  shape方法用来得到矩阵或数组的维数
    m = dataSet.shape[0]
    #tile:numpy中的函数。tile将原来的一个数组minVals，扩充成了m行1列的数组
    #矩阵中所有的值减去最小值
    normDataSet = dataSet - tile(minVals,(m,1))
    #矩阵中所有的值除以最大取值范围进行归一化
    normDataSet = normDataSet/tile(ranges,(m,1))
    #返回归一矩阵 取值范围 和最小值
    return normDataSet,ranges,minVals

def classify (inx,dataSet,labels,k):
    #得到数据集的行数  shape方法用来得到矩阵或数组的维数
    dataSetSize = dataSet.shape[0]
    #tile:numpy中的函数。tile将原来的一个数组，扩充成了dataSetSize行1列的数组。diffMat得到了目标与训练数值之间的差值。
    diffMat = tile(inx,(dataSetSize,1))-dataSet
    #计算差值的平方
    sqDiffMat = diffMat**2
    #计算差值平方和
    sqDistances = sqDiffMat.sum(axis = 1)
    #计算距离
    distances = sqDistances**0.5
    #得到排序后坐标的序号  argsort方法得到矩阵中每个元素的排序序号
    sortedDistIndicies = distances.argsort()
    classcount = {}
    for i in range(k):
        #找到前k个距离最近的坐标的标签
        voteIlabel = labels[sortedDistIndicies[i]]
        #在字典中设置键值对： 标签：出现的次数
        classcount [voteIlabel] = classcount.get(voteIlabel,0)+1 #如果voteIlable标签在classcount中就得到它的值加1否则就是0+1
    # 对字典中的类别出现次数进行排序，classCount中存储的事 key-value，其中key就是label，value就是出现的次数
    # 所以key=operator.itemgetter(1)选中的是value，也就是对次数进行排序 reverse = True表示降序排列
    sortedClassCount = sorted(classcount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
print group
aaa = [[1,2,3],[2,3,4]]
print group**2
print aaa
print array(aaa).max(axis=1)
print array(aaa)**2
print array(aaa).argsort()
labels = ['A','A','B','B']
print classify([0.1,0.1],group,labels,3)
