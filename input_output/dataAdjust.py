#!/usr/bin/python
# -*- coding: utf-8 -*-
from functools import partial

import math
from numpy import shape, mean

from scipy.ndimage import standard_deviation

from input_output.explore_data import get_column, make_matrix
from ml.step_1 import dot

from ml.kmean_cluster import vector_sum

from ml.step_1 import scalar_multiply

from ml.step_1 import safe

from ml.step_1 import step

from ml.step_1 import maximize_stochastic

from input_output.vector_op import vector_subtract


def scale(data_matrix): #计算每列的均值和标准差
    num_rows,num_cols = shape(data_matrix)
    means = [mean(get_column(data_matrix,j))
             for j in range(num_cols)]
    stdevs = [standard_deviation(get_column(data_matrix,j))
              for j in range(num_cols)]
    return means,stdevs

def rescale(data_matrix): #用结果创建新的矩阵
    means, stdevs = scale(data_matrix)
    def rescaled(i, j):
        if stdevs[j] >0:
            return (data_matrix[i][j] - means[j])/stdevs
        else:
            return data_matrix[i][j]

    num_rows, num_cols = shape(data_matrix)
    return make_matrix(num_rows,num_cols,rescaled)

def de_mean_matrix(A): #將數據轉換為每個維度和為零的形式
    nr, nc = shape(A)
    column_menas, _ =scale(A)
    return make_matrix(nr,nc,lambda i,j: A[i][j]-column_menas[j])

def sum_of_sqares(v): #计算一个向量的平方和
    return dot(v,v)

def magnitude(w): #计算向量长度
    return math.sqrt(sum_of_sqares(w))

def direction(w): #w為一個非零向量
    mag =magnitude(w)
    return [w_i / mag for w_i in w]

def directional_variance_i(x_i, w): #計算w方向的方差
    return dot(x_i, direction(w))**2

def directional_variance(X,w):
    return  sum(directional_variance_i(x_i,w) for x_i in X)

def directioanal_variance_gradient_i(x_i, w):
    projection_length = dot(x_i, direction(w))
    return [2* projection_length * x_ij for x_ij in x_i]

def directional_variance_gradient(X,w):
    return vector_sum(directional_variance_i(x_i, w) for x_i in X)

def minimize_batch(target_fn, gradient_fn, theta_0, tolerance=0.000001):
    """use gradient descent to find theta that minimizes target function"""
    step_sizes = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
    theta = theta_0 # set theta to initial value
    target_fn = safe(target_fn) # safe version of target_fn
    value = target_fn(theta) #我们试图最小化的值

    while True:
        gradient = gradient_fn(theta)
        next_thetas = [step(theta, gradient, -step_size)
                       for step_size in step_sizes]
        # choose the one that minimizes the error function
        next_theta = min(next_thetas, key=target_fn)
        next_value = target_fn(next_theta)

        # stop if we're "converging"
        if abs(value - next_value) < tolerance:
            return theta
        else:
            theta, value = next_theta, next_value

def negate(f):
    return lambda *args, **kwargs: -f(*args, **kwargs)

def negate_all(f):
    return lambda *args, **kwargs:[-y for y in f(*args, **kwargs)]

def maximize_batch(target_fn, gradient_fn, theta_0,tolerance=0.000001):
    return minimize_batch(negate(target_fn), negate_all(gradient_fn), theta_0, tolerance)

def first_principal_component(X): #用梯度下降第一主成分
    guess = [1 for _ in X[0]]
    unscaled_maximizer = maximize_batch(
        partial(directional_variance, X),
        partial(directional_variance_gradient, X),
        guess)
    return direction(unscaled_maximizer)

def first_principal_component_sgd(X): #隨機梯度
    guess = [1 for _ in X[0]]
    unscaled_maximizer = maximize_stochastic(
        lambda x,_,w: directional_variance_i(X,w),
        lambda x,_,w: directional_variance_gradient(X,w),
        X,
        [None for _ in X], #假的'y'
        guess
    )
    return direction(unscaled_maximizer)

def project(v,w): #投影
    projection_length = dot(v,w)
    return scalar_multiply(projection_length,w)

def remove_projection_from_vector(v,w): #移除
    return vector_subtract(v, project(v,w))

def remove_projection(X, w):
    return [remove_projection_from_vector(x_i, w) for x_i in X]

def principal_component_analysis(X, num_components): #通过迭代找到任意数目的主成分
    components = []
    for _ in range(num_components):
        component = first_principal_component(X)
        components.append(component)
        X = remove_projection(X, component)
    return components

def transform_vector(v,components):
    return [dot(v,w) for w in components]

def transform(X, components): #将数据转换成主成分低维空间的点
    return [transform_vector(x_i, components) for x_i in X]

