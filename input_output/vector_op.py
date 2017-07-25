#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

height_weight_age = [70,   # inches,
                     170,   # pounds,
                     40 ]   # years
#向量表示:list容器里的数字看成vectors，3个数字的list对应于3个维度空间的vector：


def vector_add(v, w): #向量相加
    """adds corresponding elements"""
    return [v_i + w_i
            for v_i, w_i in zip(v, w)]

def vector_subtract(v, w): #两个vectors相减就是对应的元素相减：
    """subtracts corresponding elements"""
    return [v_i - w_i
            for v_i, w_i in zip(v, w)]

def vector_sum(vectors):
    """sums all corresponding elements"""
    result = vectors[0]
    for vector in vectors[1:]:
        result = vector_add(result, vector)
    return result

#高阶函数更加简洁的重写这个功能：
def vector_sum(vectors):
    return reduce(vector_add, vectors)

#或者使用偏函数(属于函数式编程的思维):
vector_sum = partial(reduce, vector_add)


#vector乘以一个常值
def scalar_multiply(c, v):
    """c is a number, v is a vector"""
    return [c * v_i for v_i in v]

#相同大小vectors集合的均值：
def vector_mean(vectors):
    """compute the vector whose ith element is the mean of the
    ith elements of the input vectors"""
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))

#点乘
def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i
               for v_i, w_i in zip(v, w))

#计算vector的平方和：
def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)

def magnitude(v):
    return math.sqrt(sum_of_squares(v)) # math.sqrt is square root function

#2个向量距离
def squared_distance(v, w):
    """(v_1 - w_1) ** 2 + ... + (v_n - w_n) ** 2"""
    return sum_of_squares(vector_subtract(v, w))
def distance(v, w):
    return math.sqrt(squared_distance(v, w))

#一种更加聪明的写法(与上面等价)：
def distance(v, w):
    return magnitude(vector_subtract(v, w))
