#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import heapq

def wr_single(prices, l):
    wr_indicator = []
    heap_high = []
    heap_low = []
    for i in range(len(prices)):
        heapq.heappush(heap_high, -prices[i][1])
        heapq.heappush(heap_low, prices[i][2])
        if i>=l:
            heap_high.remove(-prices[i-l][1])
            heap_low.remove(prices[i-l][2])
            heapq.heapify(heap_high)
            heapq.heapify(heap_low)
            while len(heap_high)<l:
                heap_high.heappush(-prices[i-l][1])
            while len(heap_low)<l:
                heap_low.heappush(prices[i-l][2])
        rsvt = 100
        if -heap_high[0] > heap_low[0]:
            rsvt = (prices[i][3] - heap_low[0])*100./(-heap_high[0]-heap_low[0])
        wr_indicator.append(100 - rsvt)

    return wr_indicator

def wr(prices, n0, n1):
    wr0 = wr_single(prices, n0)
    wr1 = wr_single(prices, n1)
    indicator = []

    for i in range(len(wr0)):
        indicator.append([wr0[i], wr1[i]])

    return indicator

def energy_earn(prices, wr_indicator):
    holds = 0
    money = prices[0][3]*100
    alpha = 0.01
    offset = 1
    v = [money]
    for i in range(0, len(wr_indicator)-1):
        if holds==0 and wr_indicator[i]>=80:
            holds = int(money/prices[i+offset][3])
            money -= holds*prices[i+offset][3]*(1+alpha)
        elif holds>0 and wr_indicator[i]<=20:
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
    print v
    return [-success/(len(v)-1 + 0.00000001), -money]

def optimize(prices):
    params = {"n0": {"min": 3, "max": 50, "value": 3}, "n1": {"min": 3, "max": 50, "value": 3}}
    energy = [sys.maxint, sys.maxint]
    for n0 in range(params["n0"]["min"], params["n0"]["max"]):
        wr0 = wr_single(prices, n0)
        #calc buy/sell point
        energy_tmp = energy_earn(prices, wr_single(prices, n0))
        print "energy: %s, energy_tmp: %s"%(str(energy), str(energy_tmp))
        if energy_tmp[1]<energy[1] or (energy[1] == energy_tmp[1] and energy_tmp[0]<energy[0]):
            params["n0"]["value"] = n0
            energy = energy_tmp
    return params
