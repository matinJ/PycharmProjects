#!/usr/bin/python
# -*- coding: utf-8 -*-
from numpy import zeros, shape, tile
from sklearn.cluster import KMeans
from sklearn import decomposition
import deal_data
import numpy as np
from matplotlib import pyplot as plt
import pca

def normalSize(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normMatrix = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normMatrix = dataSet - tile(minVals,(m,1))
    normMatrix = normMatrix / tile(ranges, (m,1))
    return normMatrix
#
# if __name__ == '__main__':
#     X=deal_data.makeMatrix()
#     branch_No = X[:,0]
#     X=np.delete(X,[0,1,10],axis=1)
#     X_n=normalSize(X)
#     kmeans = KMeans(10).fit(X_n)
#     label = kmeans.labels_
#     # print label
#     label = np.array(label).T
#     label = np.column_stack((label,branch_No))
#     label = np.column_stack((label,X))
#     label= label[np.lexsort(label[:,::-1].T)] #按第一列顺序排序
#     print label
#     lset = set(label[:,0])
#     # for i in lset:
#     #     print "第%d类" %i
#     #     for j in range(len(label)):
#     #         if label[j][0]==i:
#     #             print label[j]
#     for i in label:
#         for j in i:
#             print j,
#         print


def file2Matrix(file):
    fr = open(file)
    array = fr.readlines()
    num = len(array)
    returnMat = zeros((num,31))
    index = 0
    for line in array:
        line = line.strip().split()
        returnMat[index,:] = line[0:31]
        index+=1
    return returnMat

def analysis_result(data):
    for e in range(29):
         colors = ['b','g','r','k','c','m','y','#e24fff','#524C90','#845868','b','g','r','k','c','m','y','#e24fff','#524C90','#845868','b','g','r','k','c','m','y','#e24fff','#524C90','#845868','b','g','r','k','c','m','y','#e24fff','#524C90','#845868']
         deminsion =['0-16','16-24','24-32','32-40','40-48','48-56','56-64','64+','0-1','1-2','2-6','6-10','10-15','15-18','18-23','总资产','总市值','市值占比','投顾签约率','持仓比','利润率',
                     '单日融资融券','日均交易额','总客户数','有效户占比','现金港签约率','小方登录天数']
         n_clusters = 10

         for i in range(n_clusters):
             x=[]
             y=[]
             max_a=0
             min_a=0
             max_b=0
             min_b=0
             for j in range(0,len(data)):
                 if data[j][0] == i:
                     y.append(data[j][e+2])
                     x.append(i)
             plt.scatter(x,y,marker='.',color=colors[i],linewidths=8)
             if max_a < max(x):
                 max_a = max(x)
             if max_b < max(y):
                 max_b = max(y)
             if min_a >min(x):
                 min_a = min(x)
             if min_b >min(y):
                 min_b=min(y)
             plt.axis([min_a-1,max_a+1,min_b,max_b+max_b])
         plt.show()
         print "维度:%s" %deminsion[e]

def analysis_cluster(data,n_cluster):
    xx=['.','x','+','*','s','<','o','_','>',',']
    max_a=0
    max_b=0
    min_a=0
    min_b=0
    for i in range(n_cluster):
        deminsion =['0-16','16-24','24-32','32-40','40-48','48-56','56-64','64+','0-1','1-2','2-6','6-10','10-15','15-18','18-23','总资产','总市值','市值占比','投顾签约率','持仓比','利润率',
                    '单日融资融券','日均交易额','总客户数','有效户占比','现金港签约率','小方登录天数']
        y=[]
        x=[]
        T=0

        for j in range(0,len(data)):
            if data[j][0] == i:
                x.append(data[j][2])
                y.append(data[j][3])

                if max_a < max(x):
                    max_a = max(x)
                if max_b < max(y):
                    max_b = max(y)
                if min_a >min(x):
                    min_a = min(x)
                if min_b >min(y):
                    min_b=min(y)
        # T= np.arctan2(x,y)
        plt.scatter(x,y,s=25,marker=xx[i%10])
    plt.axis([min_a,max_a,min_b,max_b])
    plt.show()

n_cluster=3
data = file2Matrix("/Users/Jian/Downloads/result.txt")
print np.shape(data)
data = np.delete(data,[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,25,30],axis=1)
aa = data[:,0:2]
# print np.shape(data)
data_set=data[:,2:]
print np.shape(data_set)
# print data_set[0][0]
data_set = normalSize(data_set)
data_new = pca.pca_branch(data_set)
kmeans = KMeans(n_cluster,init='k-means++').fit(data_new)
lab = kmeans.labels_
print lab
lab = np.array(lab).T
lab = np.column_stack((lab,aa[:,1:2]))
lab = np.column_stack((lab,data_new))
lab= lab[np.lexsort(lab[:,::-1].T)] #按第一列顺序排序
# print lab
np.savetxt('new.csv', lab, delimiter = ',')
print lab[:,0:2]
# analysis_result(lab)
analysis_cluster(lab,n_cluster)