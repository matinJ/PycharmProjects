#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
# import matplotlib.pyplot as plt
from matplotlib.mlab import find
from numpy import *
import matplotlib.pyplot as plt
from numpy.matlib import rand

plt.figure(figsize=(16,12))
n=1000
#rand 均匀分布和 randn高斯分布
x=np.random.randn(1,n)
y=np.random.randn(1,n)
T=np.arctan2(x,y)
plt.scatter(x,y,c=T,s=25,alpha=0.8,marker='o')
#T:散点的颜色
#s：散点的大小
#alpha:是透明程度
plt.show()

# x=rand(50,2)
# print x
# kk=x[:,1]
# ll=x[:,0]
#
# print kk,ll

