#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import numpy as np

def dealMultifile(dirname):
    dict={}
    for root,dir,files in os.walk(dirname):
        for file in files:
            if file[-4:]=='.crc':
                continue
            fd= open(dirname+'/'+ file)
            for line in fd:
                row = line.rstrip().split("\t")
                if row[0]=='\\N':
                    continue
                key = int(row[0])
                value=int(row[2])
                if int(row[0])<1000 or int(row[0])>2600 or int(row[0])==1060:
                    continue
                dict[key]=dict.get(key,0)+value
    return dict

def dealSinglefile(file):
    dict={}
    fd = open(file)
    for line in fd:
        row = line.rstrip().split("\t")
        if row[0]=='\\N':
            continue
        key = int(row[0])
        value = int(row[1])
        if key<1000 or key>2600 or key==1060 or key==2040:
            continue
        dict[key]=value
    return dict

def deal_xiaofangTimes(file):
    dict={}
    fd = open(file)
    for line in fd:
        row=line.rstrip().split("\t")
        if row[0]== '\\N':
            continue
        key = int(row[0])
        value = int(row[2])
        if key<1000 or key>2600 or key==1060 or key==2040:
            continue
        dict[key]=dict.get(key,0)+value
    return dict

def deal_age(file):
    dict={}
    fd = open(file)
    for line in fd:
        row=line.rstrip().split("\t")
        if row[0]== '\\N':
            continue
        key = int(row[0])
        value = int(row[2])
        if key<1000 or key>2600 or key==1060 or key==2040:
            continue
        if value<=0 or value>100:
            continue
        if not dict.has_key(key):
            dict[key]=[0,0,0,0,0,0,0,0,0]
        dict[key][0] += value
        if value/16==0:
            dict[key][1]+=value
        elif value/8 > 8:
            dict[key][8]+=value
        else:
            dict[key][value/8]+=value
    return dict

def deal_openDate(file):
    dict={}
    fd = open(file)
    for line in fd:
        row=line.rstrip().split("\t")
        if row[0]== '\\N':
            continue
        key = int(row[0])
        value = int(float(row[2]))
        if key<1000 or key>2600 or key==1060 or key==2040:
            continue
        if value<=0 or value>23:
            continue
        if not dict.has_key(key):
            dict[key]=[0,0,0,0,0,0,0,0]
        dict[key][0] += 1
        if value == 1:
            dict[key][1]+=1
        elif value ==2:
            dict[key][2]+=1
        elif value>=3 and value <6:
            dict[key][3]+=1
        elif value>=6 and value <10:
            dict[key][4] +=1
        elif value>=10 and value <15:
            dict[key][5]+=1
        elif value>=15 and value <18:
            dict[key][6]+=1
        else:
            dict[key][7]+=1
    return dict

def as_num(x):
    y='{:.2f}'.format(x) # 2f表示保留2位小数点的float型
    return(y)

def deal_asset(file):
    dict={}
    fd = open(file)
    for line in fd:
        row=line.rstrip().split("\t")
        if row[0]== '\\N':
            continue
        key = int(row[0])
        if key<1000 or key>2600 or key==1060 or key==2040:
            continue
        value=[]
        value.append(float(row[1]))
        value.append(float(row[2]))
        value.append(float(row[3]))
        dict[key]=value
    return dict

def deal_client(file):
    dict={}
    fd = open(file)
    for line in fd:
        row=line.rstrip().split("\t")
        if row[0]== '\\N':
            continue
        key = int(row[0])
        if key<1000 or key>2600 or key==1060 or key==2040:
            continue
        value=[]
        value.append(int(row[1]))
        value.append(float(row[2]))
        dict[key]=value
    return dict

def deal_singlefileFloat(file):
    dict={}
    fd = open(file)
    for line in fd:
        row = line.rstrip().split("\t")
        if row[0]=='\\N':
            continue
        key = int(row[0])
        if key<1000 or key>2600 or key==1060 or key==2040:
            continue
        value = float(row[1])
        dict[key]=value
    return dict

def tolist(dict, alist):
    arr=[]
    for i in alist:
        arr.append(dict[i])
    return arr

def tolist_more(dict,alist):
    arr=[]
    for i in alist:
        arr.append(dict[i])
    result=[]
    for i in arr:
        if isinstance(i,list):
            k = i[0]
            tmp=[]
            for j in i:
                j=float(j)/k
                tmp.append(j)
            result.append(tmp)
    return result

def makeMatrix():
    age = deal_age("/home/hadoop/jianhuoyong/branch_cluster/age/000000_0")
    asset_market = deal_asset("/home/hadoop/jianhuoyong/branch_cluster/asset_market/000000_0")
    fwcp = dealSinglefile("/home/hadoop/jianhuoyong/branch_cluster/fwcp/000000_0")
    hold_rate = deal_singlefileFloat("/home/hadoop/jianhuoyong/branch_cluster/hold_rate/000000_0")
    opendate = deal_openDate("/home/hadoop/jianhuoyong/branch_cluster/open_date/000000_0")
    profit_rate = deal_singlefileFloat("/home/hadoop/jianhuoyong/branch_cluster/profit_rate/000000_0")
    rzrq = deal_singlefileFloat("/home/hadoop/jianhuoyong/branch_cluster/rzrq/000000_0")
    trade_mount = deal_singlefileFloat("/home/hadoop/jianhuoyong/branch_cluster/trade_mount/000000_0")
    trade_times = deal_singlefileFloat("/home/hadoop/jianhuoyong/branch_cluster/trade_times/000000_0")
    valid_client = deal_client("/home/hadoop/jianhuoyong/branch_cluster/valid_client/000000_0")
    xianjingang = dealSinglefile("/home/hadoop/jianhuoyong/branch_cluster/xianjingang/000000_0")
    xiaofang_days = dealMultifile("/home/hadoop/jianhuoyong/branch_cluster/xiaofang_days")
    xiaofang_times = deal_xiaofangTimes("/home/hadoop/jianhuoyong/branch_cluster/xiaofang_times/000000_0")
    branch_no = sorted(age.keys())
    branch = np.array(branch_no).T
    branch = np.column_stack((branch,tolist_more(age,branch_no)))
    branch = np.column_stack((branch,tolist_more(opendate,branch_no)))
    branch = np.column_stack((branch,tolist(asset_market,branch_no)))
    branch = np.column_stack((branch,tolist(fwcp,branch_no)))
    branch = np.column_stack((branch,tolist(hold_rate,branch_no)))
    branch = np.column_stack((branch,tolist(profit_rate,branch_no)))
    branch = np.column_stack((branch,tolist(rzrq,branch_no)))
    branch = np.column_stack((branch,tolist(trade_mount,branch_no)))
    branch = np.column_stack((branch,tolist(trade_times,branch_no)))
    branch = np.column_stack((branch,tolist(valid_client,branch_no)))
    branch = np.column_stack((branch,tolist(xianjingang,branch_no)))
    branch = np.column_stack((branch,tolist(xiaofang_days,branch_no)))
    branch = np.column_stack((branch,tolist(xiaofang_times,branch_no)))
    # branch = np.delete(branch,[0,1,10],axis=1)
    return branch