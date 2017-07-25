#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from sklearn.cluster import KMeans
import numpy as np
import sys
from load_matrix import *

if __name__ == '__main__':
    stock_code = set()
    client_id = set()
    for f in sys.argv[1:]:
        with open(f) as df:
            for line in df:
                row = line.split('\t')
                client_id.add(row[0])
                stock_code.add(row[1])

    #we get all stock codes and all client ids
    files = sys.argv[1:]
    #    r = []
    #output client ids
    cf = open("clientids", "w")
    for c in client_id:
        cf.write(c + "\n")
    cf.close()

    for f in files:
        print "processing: ", f
        fc = {}
        with open(f) as df:
            for line in df:
                row = line.rstrip().split('\t')
                if not fc.has_key(row[0]):
                    fc[row[0]] = {}
                fc[row[0]][row[1]] = row[2:]
        #
        rf = open(f + ".r", "w")
        for c in client_id:
            if not fc.has_key(c):
                rf.write("\t0\t0"*len(stock_code) +"\n")
                continue
            for sc in stock_code:
                if not fc[c].has_key(sc):
                    rf.write("\t0\t0")
                    continue
                rf.write("\t" + fc[c][sc][0] + "\t" + fc[c][sc][1])
            rf.write("\n")
        del fc
        rf.close()

        #cluster