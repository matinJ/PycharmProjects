#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    stocks = dict()
    users = {}
    with open(filename) as f:
        count = 1
        for line in f:
            row = line.split('\t')
            client_id = row[0]
            stock_code = row[1]
            buy = float(row[2]) + float(row[3])
            if not stocks.has_key(stock_code):
                stocks[stock_code] = len(stocks)
            if not users.has_key(client_id):
                users[client_id] = {}
                users[client_id]["id"] = len(users)
            users[client_id][stock_code] = buy
            if count%1000 == 0:
                print count
            count += 1
    #post process
    rf = open("pre.r", "w")
    for client_id in users.keys():
        if len(users[client_id]) == 2:
            for stock_code in users[client_id]:
                if stock_code != "id":
                    rf.write(str(users[client_id]["id"]) + "\t" + str(stocks[stock_code]) + "\t5\n")
            continue
        upper = None
        lower = None
        stock_list = []
        for stock_code in users[client_id].keys():
            if stock_code == "id":
                continue
            stock_list.append(stock_code)
            if upper == None:
                upper = lower = users[client_id][stock_code]
            else:
                upper = max(upper, users[client_id][stock_code])
                lower = min(lower, users[client_id][stock_code])
        #normalize
        if lower == upper:
            b = 5
            a = 0
        else:
            a = 4./(upper-lower)
            b = 1
        for stock_code in stock_list:
            rf.write(str(users[client_id]["id"]) + "\t" + str(stocks[stock_code]) + "\t" + str(a*(users[client_id][stock_code]-lower) + b) + "\n")
    rf.close()
