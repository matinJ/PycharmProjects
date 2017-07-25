__author__ = 'Jian'
# -*- coding:utf-8 -*-

import os
import sys
import string

ss = "rzrqlistview"
info = "/Users/Jian/" + ss

listfile =  os.listdir(info)
filename = open(info+'1.txt','a+')
for line in listfile:
    print line
    out = open(info+'/'+line,'r')
    for com in out:
        pos1=com.find('listView id=')
        yh = '"'
        if pos1 != -1:
            pos2=com[pos1+13:].find(yh)
            str1 = com[pos1+13:pos1+13+pos2]
            filename.write(str1)
            pos3 = com.find('name=')
            pos4 =com[pos3+6:].find('"')
            filename.seek(0,0)
            filename.write('\t'+com[pos3+6:pos3+6+pos4])
            filename.write('\n')
        else:
            pos1 = com.find('columnView value=')
            if pos1 != -1:
                pos2=com[pos1+18:].find('"')
                filename.seek(0,0)
                filename.write(com[pos1+18:pos1+18+pos2])
                pos3 = com.find('caption=')
                pos4 =com[pos3+9:].find('"')
                filename.seek(0,0)
                filename.write('\t'+com[pos3+9:pos3+9+pos4])
                pos5 = com.find("description=")
                if pos5 != -1:
                    pos6 = com[pos5+13:].find('"')
                    filename.seek(0,0)
                    filename.write('\t'+com[pos5+13:pos5+13+pos6])
                filename.write('\n')
    filename.seek(0,0)
    filename.write('\n')
filename.close()
