#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from collections import Counter
from matplotlib import pyplot as plt


from numpy import shape
from scipy.spatial.distance import correlation


def inverse_normal_cdf(p,mu=0,sigma=1,tolerance=0.00001):
    #二分法获得特定概率近似值(代替逆函数)
    #非标准型,先调整单位使服从标准型
    mid_z = 0
    if mu!=0 or sigma !=1:
        return mu+sigma*inverse_normal_cdf(p,tolerance=tolerance)
    low_z, low_p=-10.0, 0
    hi_z, hi_p = 10.0, 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z)/2
        mid_p = normal_cdf(mid_z)
        if mid_p < p:
            low_z,low_p = mid_z, mid_p
        elif mid_p >p:
            hi_z, hi_p = mid_z,mid_p
        else:
            break
    return mid_z

#标准正态函数的累计正太分布
def normal_cdf(x,mu=0,sigma=1):
    return (1 + math.erf((x - mu)/math.sqrt(2)/sigma))/2

def bucketize(point, bucket_size):
    """floor the point to the next lower multiple of bucket_size"""
    return bucket_size * math.floor(point / bucket_size)
def make_histogram(points, bucket_size):
    """buckets the points and counts how many in each bucket"""
    return Counter(bucketize(point, bucket_size) for point in points)
def plot_histogram(points, bucket_size, title=""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title(title)
    plt.show()

random.seed(0)
# uniform between -100 and 100
uniform = [200 * random.random() - 100 for _ in range(10000)]

# normal distribution with mean 0, standard deviation 57
normal = [57 * inverse_normal_cdf(random.random())
          for _ in range(10000)]

#两个数据集(uniform和normal)均值都接近0并且标准差接近58，然而他们有不同的分布：
plot_histogram(uniform, 10, "Uniform Histogram")
plot_histogram(normal, 10, "Normal Histogram")


def random_normal():
    """returns a random draw from a standard normal distribution"""
    return inverse_normal_cdf(random.random())

xs = [random_normal() for _ in range(1000)]
ys1 = [ x + random_normal() / 2 for x in xs]
ys2 = [-x + random_normal() / 2 for x in xs]

plt.scatter(xs, ys1, marker='.', color='black', label='ys1')
plt.scatter(xs, ys2, marker='.', color='gray', label='ys2')
plt.xlabel('xs')
plt.ylabel('ys')
plt.legend(loc=9)
plt.title("Very Different Joint Distributions")
plt.show()

#多维数据--相关性矩阵
def correlation_matrix(data):
    _, num_columns = shape(data) #shape函数读取矩阵长度
    def matrix_entry(i, j):
        return correlation(get_column(data, i), get_column(data, j))
    return make_matrix(num_columns, num_columns, matrix_entry)

def make_matrix(num_rows, num_cols, entry_fn):
    return [[entry_fn(i,j)
             for j in range(num_cols)]
            for i in range(num_rows)]
def get_column(A, j):
    return [A_i[j]
            for A_i in A]

data = [[6,7,3,2,1,10],
        [1,6,8,1,8,23],
        [6,7,9,9,11,21],
        [2,1,6,8,8,23],
        [5,6,7,8,1,21]]

_, num_columns = shape(data)
fig, ax = plt.subplots(num_columns, num_columns)

for i in range(num_columns):
    for j in range(num_columns):

        # scatter column_j on the x-axis vs column_i on the y-axis
        if i != j: ax[i][j].scatter(get_column(data, j), get_column(data, i))

        # unless i == j, in which case show the series name
        else: ax[i][j].annotate("series " + str(i), (0.5, 0.5),
                            xycoords='axes fraction',
                            ha="center", va="center")

        # then hide axis labels except left and bottom charts
        if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
        if j > 0: ax[i][j].yaxis.set_visible(False)

# fix the bottom right and top left axis labels, which are wrong because
# their charts only have text in them
ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
ax[0][0].set_ylim(ax[0][1].get_ylim())

plt.show()