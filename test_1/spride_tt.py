# -*- coding:utf-8 -*-
__author__ = 'Jian'
import urllib2
import urllib
import re

request = urllib2.urlopen("http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=2&fmq=1470223098862_R_D&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=唯美摄影")
html = request.read()
# print html

def getimg(html):
    reg = r'http://.+?\.jpg'
    imgre = re.compile(reg);
    imglist = re.findall(imgre,html)
    x = 0
    for ii in imglist:
        urllib.urlretrieve(ii ,'%s.jpg'%x )
        x+=1

print getimg(html)