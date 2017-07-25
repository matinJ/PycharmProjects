#!/usr/bin/python
# -*- coding: utf-8 -*-
import scipy.sparse as sp
import csr_matrix
import math

def load_matrix(filename):
    f = open(filename)
    m = None
    for line in f:
        row = line.strip().split('\t')
        tmp = sp.csr_matrix(map(float, row))
        total = math.sqrt((tmp*tmp.transpose())[0,0])
        if total>0:
            tmp /= total
        if m == None:
            m = tmp
        else:
            m = csr_matrix.csr_vappend(m, tmp)
        if m.shape[0]%1000 == 0:
            print m.shape
    return m

def load_matrix_2(filename):
    f = open(filename)
    l = []
    t = None
    for line in f:
        row = line.strip().split('\t')
        if t == None:
            t = [0.0]*len(row)
        tmp = t[:]
        total = 0.0
        for i in range(len(row)):
            if not i=='0':
                tmp[i] = float(row[i])
                total += tmp[i]**2
        tmp = sp.csr_matrix(tmp)
        total = math.sqrt(total)
        if total>0:
            tmp /= total
        l.append(tmp)
        if len(l)%1000 == 0:
            print len(l)

    while len(l)>1:
        ll = []
        for i in range(0,len(l),2):
            if (i+1) < len(l):
                ll.append(csr_matrix.csr_vappend(l[i], l[i+1]))
            else:
                ll.append(l[i])
        del l
        l = ll
    return l[0]