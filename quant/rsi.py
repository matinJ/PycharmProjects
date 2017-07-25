#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def rsi_single(prices, n):
    rsi_indicator = [100.0]
    #lc = prices[0][3]
    sma_1 = [0.0]
    sma_2 = [0.0]
    for i in range(1, len(prices)):
        lc = prices[i-1][3]
        cc = prices[i][3]
        x = max(0.0, cc-lc)
        sma_1.append(x/n + (n-1)*sma_1[-1]/n)
        x = abs(cc-lc)
        sma_2.append(x/n + (n-1)*sma_2[-1]/n)
        if sma_2[-1] == 0:
            rsi_indicator.append(0.0)
        else:
            rsi_indicator.append(100*sma_1[-1]/sma_2[-1])

    return rsi_indicator

def rsi(prices, n0, n1, n2):
    rsi0 = rsi_single(prices, n0)
    rsi1 = rsi_single(prices, n1)
    rsi2 = rsi_single(prices, n2)
    indicator = []
    for i in range(len(rsi0)):
        indicator.append([rsi0[i], rsi1[i], rsi2[i]])

    return indicator

def energy_earn(prices, rsi_indicator):
    cross = []
    holds = 0
    money = prices[0][3]*100
    alpha = 0.01
    offset = 1
    v = [money]
    for i in range(1, len(rsi_indicator)-1):
        if (rsi_indicator[i][1] - rsi_indicator[i][0])*(rsi_indicator[i-1][1] - rsi_indicator[i-1][0])<=0:
            #if rsi_indicator[i-1][1]<=20 and rsi_indicator[i][1] < rsi_indicator[i][0]: # buy
            if rsi_indicator[i][1] < rsi_indicator[i][0] and rsi_indicator[i-1][1]>=rsi_indicator[i-1][2]:
                if holds == 0:
                    holds = int(money/prices[i+offset][3])
                    money -= holds*prices[i+offset][3]*(1+alpha)
            elif rsi_indicator[i-1][1] < rsi_indicator[i-1][0] and rsi_indicator[i-1][1]<=rsi_indicator[i-1][2]: #sell
                #elif rsi_indicator[i-1][1]>=80 and rsi_indicator[i-1][1] < rsi_indicator[i-1][0]: #sell
                if holds > 0:
                    money += holds*prices[i+offset][3]*(1-alpha)
                    holds = 0
                    v.append(money)
    if holds>0:
        money += holds*prices[-1][3]
        v.append(money)
    success = 0.0
    for i in range(1, len(v)):
        if v[i]>v[i-1]:
            success += 1
    return [-success/(len(v)-1 + 0.00000001), -money]

def optimize(prices):
    params = {"n0": {"min":6, "max":90, "value": 6}, "n1":{"min":10, "max":100, "value":10}, "n2":{"min":40, "max":100, "value":40}}
    energy = [sys.maxint, sys.maxint]
    for n0 in range(params["n0"]["min"], params["n0"]["max"]):
        for n1 in range(n0+1, params["n1"]["max"]):
            for n2 in range(n1+1, params["n2"]["max"]):
                energy_tmp = energy_earn(prices, rsi(prices, n0, n1, n2))
                print "n0: %d, n1: %d, n2: %d"%(n0, n1, n2)
                print "energy: %s, energy_tmp: %s"%(str(energy), str(energy_tmp))
                if energy_tmp[1]<energy[1] or (energy[1] == energy_tmp[1] and energy_tmp[0]<energy[0]):
                    params["n0"]["value"] = n0
                    params["n1"]["value"] = n1
                    params["n2"]["value"] = n2
                    energy = energy_tmp
    return params