#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from numpy.matlib import eye
from sklearn import decomposition

def pca_branch(dataSet):
    dim=1
    pca=decomposition.PCA()
    pca.fit(dataSet)
    ev_list = pca.explained_variance_ratio_
    evr =0.0
    print ev_list
    for j in range(len(ev_list)):
        evr+=ev_list[j]
        if evr >0.9:
            dim+=j
            break
    pca = decomposition.PCA(n_components=2, copy=True, whiten=False)
    print dim
    pca.fit(dataSet)
    data_te = np.mat(eye(12,12,dtype=int))
    low_d = pca.transform(dataSet)
    ddd = pca.transform(data_te)
    print ddd
    print np.shape(low_d)
    return low_d