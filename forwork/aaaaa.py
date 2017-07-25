#!/usr/bin/python
# -*- coding: utf-8 -*-
from sys import stdout
from numpy import random
# Tn=0
# Sn=[]
# n =int(raw_input('n=:\n'))
# a =int(raw_input('a=:\n'))
# for count in range(n):
#     Tn +=a
#     a=a*10
#     Sn.append(Tn)
#     # print Tn
# Sn=reduce(lambda  x,y: x+y,Sn)
# # print Sn

# sum=[]
# sum.append(100)
# for i in range(1,11):
#     sum.append((float)(sum[i-1]/2))
#     if(i==10):
#         print sum[i]
# print sum
# sum=reduce(lambda x,y: x+y, sum)
# print sum
#
# for i in range(2,11):
#     print i

# sum =1
# for i in range(9,0,-1):
#     sum +=1
#     sum*=2
# print sum
#
# def fact(j):
#     sum =0
#     if j==0:
#         sum=1
#     else:
#         sum=j*fact(j-1)
#     return sum
# for i in range(5):
#     print '%d!=%d' %(i,fact(i))

# a=[9,6,5,4,1]
# N=len(a)
# print a
# for i in range(len(a)/2):
#     a[i],a[N-i-1]=a[N-i-1],a[i]
#     print a

#定义一个类实现静态
# def varfun():
#     a=0
#     print 'a=%d' %a
#     a+=1
# if __name__=="__main__":
#     for i in range(3):
#         varfun()
#
# import time
#
# class Staticvar:
#     var=5
#     def varfun(self):
#         self.var+=1
#         print self.var
#
# print Staticvar.var
# a=Staticvar()
# start= time.clock()
# for j in range(3):
#     a.varfun()
# end = time.clock()
# b=time.time()
# print end-start
# print b
import decimal


def as_num(x):
    y='{:.2f}'.format(x) # 5f表示保留5位小数点的float型
    return(y)
a=1.2204153430015009E11
print as_num(a)


# def add(s,x):
#     return s+x
# def gen():
#     for i in range(4):
#         yield i
# base = gen()
# print base
# # for n in [1,10]:
# #     print n
# for n in range(2):
#     base =(add(i,n) for i in base)
# print list(base)

for j in range(6):
    print random.rand(j,2)