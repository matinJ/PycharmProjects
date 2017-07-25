#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

#梯度下降

def step(v, direction, step_size):
    return [v_i + step_size * direction_i
            for v_i, direction_i in zip(v, direction)]

# 定义偏导估计函数
def partial_difference_quotient(f,v,i,h):
    """compute the i-th partial difference quotient of f at v"""
    w = [v_j + (h if j==i else 0)
         for j,v_j in enumerate(v)]
    return (f(w)-f(v))/h

# 定义梯度估计函数
def estimate_gradient(f,v,h=0.00001):
    return [partial_difference_quotient(f,v,i,h)
            for i,_ in enumerate(v)]

def sum_of_square_gradient(v):
    return [2 * v_i for v_i in v]

#### 减法定义
def vector_substract(v,w):
    return [v_i - w_i
            for v_i,w_i in zip(v,w)]

### 向量的点乘
def dot(v,w):
    return sum(v_i * w_i
               for v_i,w_i in zip(v,w))

### 向量的平房和
def sum_of_squares(v):
    """v_1*v_1+v_2*v_2+...+v_n*v_n"""
    return dot(v,v)

### 向量的距离
def distance(v,w):
    return sum_of_squares(vector_substract(v,w))

###向量乘标量
def scalar_multiply(c,v):
    return [c * v_i for v_i in v]

#生成矩阵
def make_matrix(num_rows, num_cols, entry_fn):
    return [[entry_fn(i,j)
             for j in range(num_cols)]
            for i in range(num_rows)]

def safe(f):
    def safe_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return float('inf')
    return safe_f

#最小化
def minimize_batch(target_fn, gradient_fn, theta_0, tolerance = 0.000001):
    step_sizes = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
    theta = theta_0
    target_fn = safe(target_fn)
    value = target_fn(theta)
    while True:
        gradient = gradient_fn(theta)
        next_thetas = [step(theta, gradient, -step_size)
                       for step_size in step_sizes]
        #选择最小化目标函数的theta
        next_theta = min(next_thetas, key = target_fn)
        next_value = target_fn(next_theta)
        if abs(value - next_value) < tolerance:
            return theta, value
        else:
            theta, value = next_theta, next_value


#随机序列
def in_random_order(data):
    """generator that returns the elements of data in random order"""
    indexes = [i for i,_ in enumerate(data)] #生成索引列表
    random.shuffle(indexes)
    for i in indexes:
        yield data[i]

def minimize_stochastic(target_fn,gradient_fn,x,y,theta_0,alpha_0=0.01):
    data = zip(x,y)
    theta = theta_0
    alpha = alpha_0   # 初始化步长
    min_theta, min_value = None,float("inf")
    iterations_with_no_improvment = 0

    #当迭代100次均没有提升，则停止
    while iterations_with_no_improvment < 100:
        value = sum(target_fn(x_i,y_i,theta) for x_i,y_i in data)

        if value < min_value:
            #found a new minimum,remember it
            min_theta,min_value = theta,value
            iterations_with_no_improvment = 0
            alpha= alpha_0
        else:
            iterations_with_no_improvment+=1
            alpha *=0.9

        #沿着梯度移动一步
        for x_i,y_i in in_random_order(data):
            gradient_i = gradient_fn(x_i,y_i,theta)
            theta = vector_substract(theta,scalar_multiply(alpha,gradient_i))

    return min_theta

def negate(f):
    return lambda *args, **kwargs: -f(*args, **kwargs)

def negate_all(f):
    return lambda *args, **kwargs:[-y for y in f(*args, **kwargs)]

def maximize_stochastic(target_fn, gradient_fn,x,y,theta_0, alpha_0=0.01):
    return minimize_stochastic(negate(target_fn),negate_all(gradient_fn),x,y,theta_0,alpha_0)

v = [random.randint(-10,10) for i in range(3)]
tolerance = 0.0000001
iter = 1
max_iter =10000
while True:
    gradient = sum_of_square_gradient(v)
    next_v = step(v, gradient, -0.01)
    if distance(next_v, v) < tolerance or iter > max_iter:
        break
    v = next_v
    iter += 1
print v, iter



# max_iter = 1000
# iter = 1
# theta_0 = [random.randint(-10,10) for i in range(3)]
# while True:
#     theta,value = minimize_batch(target_fn = sum_of_squares,gradient_fn = sum_of_square_gradient,theta_0 = theta_0,tolerance = 0.0001)
#     print theta,value
#     if (iter > max_iter) or (value == sum_of_squares(theta_0)):
#         break
#     theta_0 = theta
#     iter+=1
# print theta_0,iter

