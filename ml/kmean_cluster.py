#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

import math
import matplotlib.pyplot as plt

class KMeans:
    def __init__(self, k):
        self.k = k
        self.means = None
    def classify(self, input):
        return min(range(self.k),
                   key=lambda  i: squared_distance(input, self.means[i]))
    def train(self, inputs):
        self.means = random.sample(inputs, self.k)
        assignments = None
        while True:
            new_assignments = map(self.classify, inputs)
            if assignments == new_assignments:
                return
            assignments = new_assignments
            for i in range(self.k):
                i_points = [p for p, a in zip(inputs, assignments) if a==i]
                if i_points:
                    self.means[i] = vector_mean(i_points)


def vector_mean(vectors):
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))
def scalar_multiply(c,v):
    return [c * v_i for v_i in v]
def vector_sum(vectors):
    return reduce(vector_add,vectors)
def vector_add(v, w):
    return [v_i + w_i
            for v_i, w_i in zip(v,w)]
def squared_distance(v, w):
    return math.sqrt(sum((v_i-w_i)**2
                     for v_i,w_i in zip(v,w)))


def squared_clustering_errors(inputs, k):
    clusterer = KMeans(k)
    clusterer.train(inputs)
    means = clusterer.means
    assignments = map(clusterer.classify, inputs)
    return sum(squared_distance(input, means[cluster])
               for input, cluster in zip(inputs, assignments) )


# list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# slice = random.sample(list, 5) #从list中随机获取5个元素，作为一个片断返回
# print slice

inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]
random.seed(0)
test = KMeans(3)
test.train(inputs)
x0 = [xi for xi,_ in inputs]
y0 = [yi for _,yi in inputs]

x_means = [xi for xi,_ in test.means]
y_means = [yi for _,yi in test.means]

print test.means

plt.scatter(x0,y0)
plt.scatter(x_means,y_means,color ='r')
plt.show()

# ks = range(1, len(inputs) +1)
# errors = [squared_clustering_errors(inputs, k) for k in ks]
# plt.plot(ks, errors)
# plt.xticks(ks)
# plt.xlabel("k")
# plt.ylabel("误差平方和")
# plt.title("总误差与聚类数目")
# plt.show()