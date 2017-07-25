#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy
from math import *
import sys

def gaussian_kernal(x, std=2):
    return exp(-(x*x)/(2*std*std))

def macd(array, long_p=26, short_p=12, dea_a=9):
    r = []
    l = len(array)
    ema1 = array[-1]*2/(short_p + 1)
    ema2 = array[-1]*2/(long_p + 1)
    dif = ema1 - ema2
    dea = 0
    macd = 0
    r.append([dif, dea, macd])
    for i in range(1, l):
        ema1 = array[i]*2/(short_p + 1) + ema1*(short_p - 1)/(short_p + 1)
        ema2 = array[i]*2/(long_p + 1) + ema2*(long_p - 1)/(long_p + 1)
        dif = ema1 - ema2
        dea = dif*2/(dea_a + 1) + r[-1][1]*(dea_a - 1)/(dea_a + 1)
        macd = (dif - dea)*2
        #if dif>10000:
        #    print array[i]
        r.append([dif, dea, macd])

    return r

def smooth_price(array, size=3, times=1, std=3):
    kernal = [gaussian_kernal(x, std) for x in range(-size, size+1)]
    total =  sum(kernal)
    for i in range(0, len(kernal)):
        kernal[i] = kernal[i]/total
    for t in range(0, times):
        rc = numpy.convolve(array, kernal)
        #rc = rc[size: -size]
        array = rc
    rc = rc[size*times: -size*times]
    return rc
def energy_func(macd, rc):
    #macd cross point
    cross = []
    cross_type = []
    for i in range(1, len(macd)):
        if macd[i][2]*macd[i-1][2] <= 0:
            cross.append(i)
            cross_type.append(1 if macd[i][2]-macd[i-1][2] >0 else -1)
    energy = 0
    # maximum or minimum
    diff = []
    second_diff = []
    for i in range(2, len(rc)):
        if ((rc[i-1]-rc[i-2])*(rc[i]-rc[i-1])) <= 0:
            diff.append(i-1)
            second_diff.append(rc[i-2]+rc[i]-2*rc[i-1])
    # calc energy
    jj = 0
    i = 0
    alpha=5
    beta=5
    count_a = 0
    count_b = 0
    while i < len(diff):
        for j in range(jj, len(cross)):
            #print "j: %d, i: %d"%(j, i)
            if cross[j]>=diff[i]:
                break;
            energy = energy + alpha
            count_a +=1
        jj=j+1
        if j>= len(cross):
            break;
        flag = False
        while i<len(diff) and diff[i]<=cross[j]:
            i = i+1
            flag = True
            energy = energy + beta
            count_b += 1

        if flag == True:
            i -= 1
            count_b -= 1
            energy = energy - beta
            if cross_type[j]*second_diff[i]<0:
                j += 1
            if j<len(cross):
                energy = energy + (cross[j]-diff[i])

        i = i+1

    return energy

def energy_func1(macd, rc):
    #macd cross point
    cross = []
    cross_type = []
    for i in range(1, len(macd)):
        if macd[i][2]*macd[i-1][2] <= 0 and (macd[i][2]!=0 or macd[i-1][2]!=0):
            cross.append(i)
            cross_type.append(1 if macd[i][2]-macd[i-1][2] >0 else -1)
    energy = 0
    # maximum or minimum
    diff = []
    second_diff = []
    for i in range(2, len(rc)):
        if ((rc[i-1]-rc[i-2])*(rc[i]-rc[i-1])) <= 0 and ((rc[i-1]-rc[i-2])!=0 or (rc[i]-rc[i-1])!=0):
            diff.append(i-1)
            second_diff.append(rc[i-2]+rc[i]-2*rc[i-1])
    # calc energy
    jj = 0
    i = 0
    alpha=0.5
    total = 0
    while i < len(diff):
        j = 0
        for j in range(jj, len(cross)):
            #print "j: %d, i: %d"%(j, i)
            if cross[j]>=diff[i]:
                break
            energy = energy + alpha
        jj=j+1
        flag = False
        #print i, len(diff), j, len(cross)
        while i<len(diff) and (diff[i]<=cross[j]):
            i = i+1
            #print "xxxxxxxxxxxxxxxxxxxxxxxx"
            flag = True
            energy = energy + alpha

        if flag == True:
            i -= 1
            if cross_type[j]*second_diff[i]<0:
                if j<len(cross)-1:
                    j+=1
                if cross_type[j]*second_diff[i]<0:
                    print "check :", j, i, cross[j], diff[i], cross_type[j], second_diff[i]
                    print macd[cross[j]-1][2], macd[cross[j]][2]
                    print rc[diff[i]-1], rc[diff[i]],  rc[diff[i]+1]

                    #else:
                #print "ok........"
                else:
                    total += 1
                    energy = energy + (cross[j]-diff[i]) - alpha
        i = i+1

    return energy #/(total+0.0000001)

def energy_earn(macd, array):
    money = array[0]*100
    v = [money]
    holds = 0
    offset = 1
    alpha = 0.001
    for i in range(1, len(macd)-1):
        if macd[i][2]*macd[i-1][2] <= 0 : # and (macd[i][2]!=0 or macd[i-1][2]!=0):
            if holds==0 and macd[i-1][2] < macd[i][2]:
                holds = int (money/array[i])
                money -= holds*array[i+offset]*(1+alpha)
                #money -= holds*array[i+offset]*alpha
                #v.append(money + holds*array[i+offset])
            elif holds>0 and macd[i-1][2] > macd[i][2]:
                money += array[i+offset]*holds*(1-alpha)
                #money -= array[i+offset]*holds*alpha
                holds = 0
                v.append(money)
    success = 0
    if holds>0:
        v.append(holds*array[-1] + money)
    for i in range(1, len(v)):
        if v[i]>v[i-1]:
            success += 1
    #if success < len(v)/2:
    #    return 0
    #print "money:", v
    return [-1.0*success/(len(v)-1+0.000001), -money-holds*array[-1]][::-1]
    #print "sucess: %d, %d"%(success, len(v))
    #return -money-holds*array[-1]

def optimize(array):
    params = {"long_p": {"value":10,"min":10, "max":50}, "short_p": {"value":5, "min":5, "max":30}, "dea_p": {"value":5, "min":5, "max":20}}
    #energy = sys.maxint
    energy = [sys.maxint, sys.maxint]
    for long_p in range(params["long_p"]["min"],params["long_p"]["max"]):
        for short_p in range(params["short_p"]["min"],params["short_p"]["max"]):
            if short_p >= long_p:
                break
            for dea_p in range(params["dea_p"]["min"],params["dea_p"]["max"]):
                print "====================== long_p: %d, short_p: %d, dea_p: %d"%(long_p,short_p,dea_p)
                #switch different method to evaluate energy
                #energy_tmp = energy_func(macd(array, long_p, short_p, dea_p), smooth_price(array, 5, 3)) + (short_p-12)**2/90.0 + (long_p-26)**2/90.0 + (dea_p-9)**2/5.0
                energy_tmp = energy_earn(macd(array, long_p, short_p, dea_p), array) # + (short_p-12)**2/10.0 + (long_p-26)**2/10.0 + (dea_p-9)**2/10.0
                print "energy: %s, energy_tmp: %s"%(str(energy), str(energy_tmp))
                #if energy_tmp>0 and energy>energy_tmp:
                if energy[0]>energy_tmp[0] or (energy[0] == energy_tmp[0] and  energy[1]>energy_tmp[1]):
                    energy = energy_tmp
                    params["long_p"]["value"] = long_p
                    params["short_p"]["value"] = short_p
                    params["dea_p"]["value"] = dea_p

    return params

def metric(macd1, macd2):
    # old macd and new macd comparasion
    # calc the cross points
    cross1 = []
    cross2 = []
    for i in range(1,len(macd1)):
        if macd1[i][2]*macd1[i-1][2] <= 0:
            cross1.append(i)
        if macd2[i][2]*macd2[i-1][2] <= 0:
            cross2.append(i)
    print cross1
    print cross2
    #
    j = 0
    i = 0
    evaluation = {"missing1": 0, "missing2": 0, "count": 0, "forward": 0}
    while i<len(cross1):
        while j<len(cross2) and cross2[j]<=cross1[i]:
            j += 1
            evaluation["missing1"] += 1
        if j>0 and cross2[j-1]<=cross1[i]:
            evaluation["missing1"] -= 1
            evaluation["count"] += 1
            evaluation["forward"] += (cross1[i] - cross2[j-1])
        if j<len(cross2):
            pass
        else:
            i += 1
            while i<len(cross1):
                i += 1
                evaluation["missing2"] += 1
            break
        while i<len(cross1) and j<len(cross2) and cross1[i]<cross2[j]:
            i += 1
            evaluation["missing2"] += 1
        evaluation["missing2"] -= 1
    return evaluation


if __name__ == "__main__":
    price_file = sys.argv[1]
    result_file = sys.argv[2]
    stock_code = result_file.split("/")[-1]
    closing_price = []
    prices = []
    trade_date = []
    for line in open(price_file):
        row = line.replace("\n","").split("\t")
        closing_price.append(float(row[-1]))
        prices.append([row[-4], row[-1], row[-2], row[-3]])
        trade_date.append(row[0])
    params = optimize(closing_price)
    macd1 = macd(closing_price)
    print "params:", params
    macd_new = macd(closing_price, params["long_p"]["value"],params["short_p"]["value"], params["dea_p"]["value"])
    print "evalation:", metric(macd1, macd_new)
    print "init money: %f", closing_price[0]*100
    #write the result to file
    fw = open(result_file, "w")
    for i in range(len(closing_price)):
        #print trade_date, result_file, closing_price[i], map(str,macd1[i]), map(str,macd_new[i])
        fw.write(trade_date[i].replace("-","") + "\t" + stock_code + "\t" + ",".join(prices[i]) + "," + ",".join(map(str,macd1[i])) +"," +",".join(map(str,macd_new[i])) +"\n")
    fw.close()