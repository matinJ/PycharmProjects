#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Iterable
import os
from __builtin__ import isinstance

import time

__author__ = 'Jian'
# print('hello,world')
# d = {'a': 1, 'd': 2, 'c': 3}
# for key in d:
#     print key

print isinstance('abc', Iterable)
print isinstance([1,2,3], Iterable)
print isinstance(123, Iterable)

for i,value in enumerate(['A','B','C']):
    print i, value

#lie chu wen jian he mulu
print [d for d in os.listdir('.')]

d = {'x': 'A', 'y': 'B', 'z': 'C' }
for k, v in d.iteritems():
   print k, '=', v

arraylist=[3,4,1,2,5,8,0]
for ii in arraylist:
    print ii,

print time.localtime()
print time.time()
