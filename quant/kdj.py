#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import heapq

def kdj(prices, l=9, m=3, n=3):
    kdj_indicator = []
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
        rsvt = 0
        if -heap_high[0] > heap_low[0]:
            rsvt = (prices[i][3] - heap_low[0])*100./(-heap_high[0]-heap_low[0])
        if i>0:
            kt = rsvt/m + (m-1)*kdj_indicator[i-1][0]/m
            dt = kt/n + (n-1)*kdj_indicator[i-1][1]/n
            jt = 3*kt - 2*dt
        else:
            kt = rsvt*1.0
            dt = kt
            jt = rsvt
        kdj_indicator.append([kt, dt ,jt])
        #if i==38:
        #    print heap_high
        #    print heap_low
        #    print prices[i]
        #    print prices[i-l]
        #    print kdj_indicator[i-1]

    return kdj_indicator


def energy_earn(prices, kdj_indicator):
    cross = []
    holds = 0
    money = prices[0][3]*100
    alpha = 0.01
    offset = 1
    v = [money]
    for i in range(1, len(kdj_indicator)-1):
        if (kdj_indicator[i][1] - kdj_indicator[i][0])*(kdj_indicator[i-1][1] - kdj_indicator[i-1][0])<=0:
            if kdj_indicator[i-1][1]<=30 and kdj_indicator[i][1] < kdj_indicator[i][0]: # buy
                if holds == 0:
                    holds = int(money/prices[i+offset][3])
                    money -= holds*prices[i+offset][3]*(1+alpha)
            elif kdj_indicator[i-1][1]>=70 and kdj_indicator[i-1][1] < kdj_indicator[i-1][0]: #sell
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
    params = {"l": {"min":2, "max":40, "value": 2}, "m":{"min":2, "max":20, "value":2}, "n":{"min":2, "max":20, "value":2}}
    energy = [sys.maxint, sys.maxint]
    for l in range(params["l"]["min"], params["l"]["max"]):
        for m in range(params["m"]["min"], params["m"]["max"]):
            for n in range(params["n"]["min"], params["n"]["max"]):
                energy_tmp = energy_earn(prices, kdj(prices, l, m, n))
                print "l: %d, m: %d, n: %d"%(l, m, n)
                print "energy: %s, energy_tmp: %s"%(str(energy), str(energy_tmp))
                if energy_tmp[1]<energy[1] or (energy[1] == energy_tmp[1] and energy_tmp[0]<energy[0]):
                    params["l"]["value"] = l
                    params["m"]["value"] = m
                    params["n"]["value"] = n
                    energy = energy_tmp
    return params

if __name__ == '__main__':
    price_file = sys.argv[1]
    if len(sys.argv)>2:
        result_file = sys.argv[2]
    else:
        result_file = price_file + ".r"
    prices = []
    trade_date = []
    stock_code = "stock_code"
    for line in open(price_file):
        row = line.split("\t")
        prices.append([float(row[2]), float(row[3]), float(row[4]), float(row[5])])
        trade_date.append(row[0])
        stock_code=row[1]

    params = optimize(prices)
    print params
    kdj_indicator = kdj(prices)
    kdj_new = kdj(prices, params["l"]["value"], params["m"]["value"], params["n"]["value"])
    fw = open(result_file, "w")
    for i in range(len(trade_date)):
        fw.write(trade_date[i].replace("-","") + "\t" + stock_code + "\t" + str(prices[i][0]) +"," + str(prices[i][3]) +"," + str(prices[i][2]) +"," + str(prices[i][1]) +"," + ",".join(map(str, kdj_indicator[i])) + "," + ",".join(map(str, kdj_new[i])) +"\n")

    fw.close()
    #for indicator in kdj_indicator:
    #    print indicator