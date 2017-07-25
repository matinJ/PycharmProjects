#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import operator

if __name__ == '__main__':
    cluster_file = open(sys.argv[1])
    buy_file = open(sys.argv[2])
    labels = {}
    recommendations = {}
    buys = {}
    stocks = {}
    stock_names = {}
    for line in buy_file:
        row = line.split('\t')
        client_id = row[0]
        stock_code = row[1]
        if not stock_names.has_key(stock_code):
            stock_names[stock_code] = row[3].strip()
        if not buys.has_key(client_id):
            buys[client_id] = set()
        buys[client_id].add(stock_code)
        if not stocks.has_key(stock_code):
            stocks[stock_code] = 1
        else:
            stocks[stock_code] += 1
    sorted_stocks = sorted(stocks.items(), key=operator.itemgetter(1), reverse=True)
    common_stock_code = sorted_stocks[0][0]
    for line in cluster_file:
        row = line.strip().split('\t')
        client_id = row[0]
        label = row[1]
        if not recommendations.has_key(label):
            recommendations[label] = {}
            labels[label] = []
        labels[label].append(client_id)
        if buys.has_key(client_id):
            for stock_code in buys[client_id]:
                if not recommendations[label].has_key(stock_code):
                    recommendations[label][stock_code] = 1
                else:
                    recommendations[label][stock_code] += 1
    #calc recommendations
    rf = open("recommendations.r", "w")
    for label in recommendations.keys():
        tmp = recommendations[label]
        stmp = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)
        print "Label: %s"%label
        print stmp
        if len(stmp) > 0:
            for client_id in labels[label]:
                flag = True
                if buys.has_key(client_id):
                    for v in stmp:
                        if not v[0] in buys[client_id]:
                            rf.write(client_id + "\t" + v[0] + "\t" + stock_names[v[0]] +"\n")
                            flag = False
                            break
                    if flag == True:
                        for v in sorted_stocks:
                            if not v[0] in buus[client_id]:
                                rf.write(client_id + "\t" + v[0] + "\t" + stock_names[v[0]] + "\n")
                                break
                else:
                    rf.write(client_id + "\t" + stmp[0][0] + "\t" + stock_names[stmp[0][0]] +"\n")
        else:
            rf.write(client_id + "\t" + stock_code + "\n")
            #rf.write(label + "\t" + stock_code + "\n")
    rf.close()