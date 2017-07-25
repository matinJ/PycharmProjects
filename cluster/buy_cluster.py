#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from sklearn.cluster import KMeans
import numpy as np
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
    cf = open("clientids", "w")
    sf = open("stocks", "w")
    ind=1
    for sc in stock_code:
        sf.write(str(ind) + "\t" + sc + "\n")
        ind+=1
    sf.close()
    for c in client_id:
        cf.write(c + "\n")
    cf.close()
    nc = 1
    for f in files:
        print "processing: ", f
        fc = {}
        with open(f) as df:
            for line in df:
                row = line.rstrip().split('\t')
                if not fc.has_key(row[0]):
                    fc[row[0]] = {}
                fc[row[0]][row[1]] = row[2:3]
        #
        rf = open(f + ".r", "w")
        ind = 0
        for c in client_id:
            ind += 1
            if ind %1000 == 0:
                print ind
            if not fc.has_key(c):
                rf.write("\t0"*len(stock_code) +"\n")
                continue
            for sc in stock_code:
                if not fc[c].has_key(sc):
                    rf.write("\t0")
                    continue
                rf.write("\t" + fc[c][sc][0])
            rf.write("\n")
        del fc
        rf.close()

    #cluster
    print "Output file completed. Now load matrix to memory."
    m = load_matrix_2(f + ".r")
    kmeans = KMeans(n_clusters=600, random_state=0).fit(m)
    print "Clustering finished."
    cluster_file = open("clustering.r", "w")
    ind = 0
    for c in client_id:
        cluster_file.write(c + "\t" + str(kmeans.labels_[ind]) + "\n")
        ind += 1

