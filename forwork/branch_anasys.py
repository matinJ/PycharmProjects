#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import os
# lis=[random.randint(0,100) for i in range(200)]
# print lis
# for i in range(max(lis)/10):
#     print i*10,(i+1)*10,len([pp for pp in lis if pp>i*10 and pp<(i+1)*10])
from collections import Counter

import math
from matplotlib import pyplot

arr=[]
# dirN="/Users/Jian/Downloads/age"
# for root, dir,files in os.walk(dirN):
#     for file in files:
#         fd=dirN+"/"+file
#         f = open(fd)
#         for line in f:
#             row = line.rstrip()
#             if int(row)>100 or int(row)<=0:
#                 continue
#             arr.append(int(row))

file = open("/Users/Jian/Downloads/open_date")
for line in file:
    row = line.rstrip().split("\t")
    year = float(row[2])
    if year >23 or year<0:
        continue
    arr.append(int(math.floor(year)))

print max(arr)
dd={}
i_bar=1
for i in range(max(arr) /i_bar ):
    key=i*i_bar
    dd[key]=len([pp for pp in arr if pp>=i*i_bar and pp<(i+1)*i_bar])
print dd

# pyplot.hist(arr,21)
# # pyplot.axis([10, 100, 0, 100])
# pyplot.show()

# decile=lambda grade: grade //10*10
# histogram=Counter(decile(grade) for grade in arr)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        pyplot.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d' % (height))

rects = pyplot.bar([x-i_bar for x in dd.keys()],dd.values(),i_bar)
autolabel(rects)
pyplot.axis([0,25,0,700000])
pyplot.show()