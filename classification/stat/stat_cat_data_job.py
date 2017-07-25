"""
Date    : 15/4/10
Author  : baylor
"""

__author__ = 'baylor'

import sys
import os
prj_path = os.path.split(os.path.realpath(__file__))[0]+'/../../'
sys.path.append(prj_path)

from common.collections import Seq, util
from common import json
from common.io.file_io import MultiFileReader, FileWriter
from classification.goods_classifier.category import Category

from base.mapreduce import PyMapper, PyReducer

from classification.goods_classifier.rule_classifier import RuleBaseClassifier
from protocol.classifier.client import ClassifierClient

parse_fields = ['name', 'ourl', 'catid', 'price', 'isbn']


class StatMapper(PyMapper):
    def __init__(self, sys_in):
        PyMapper.__init__(self, sys_in, False)
        self.__fields = parse_fields
        self.__classifier = ClassifierClient('10.108.72.168', 9080)
        self.__rule = RuleBaseClassifier()

    def handle_map(self, key, value):
        try:
            items = value.split('\t')

            para = {}

            title = items[1]
            url = items[2]
            price = items[4]
            tb_cid = items[3]
            isbn = items[5]
            pv = items[6]

            para['title'] = title
            para['url'] = url
            para['price'] = price
            para['tb_cid'] = tb_cid
            para['isbn'] = isbn

            cat = self.__rule.classify(url, tb_cid, None)
            # if cat is None or len(cat) == 0:
            #     cat = self.__classifier.classifiy(para)

            if cat is None or len(cat) == 0:
                return

            self.write(cat, pv)

        except Exception, e:
            raise e


class StatReducer(PyReducer):

    def __init__(self, sys_in):
        PyReducer.__init__(self, sys_in)

    def handle_reduce(self, key, values):

        count = 0
        for v in values:
            count += int(v)

        self.write(key, count)


class StatPriceMapper(PyMapper):
    def __init__(self, sys_in):
        PyMapper.__init__(self, sys_in, False)
        self.__fields = parse_fields
        self.__classifier = ClassifierClient('10.108.72.168', 9080)
        self.__rule = RuleBaseClassifier()

    def handle_map(self, key, value):
        try:
            items = value.split('\t')

            para = {}

            title = items[1]
            url = items[2]
            price = items[4]
            tb_cid = items[3]
            isbn = items[5]
            pv = items[6]

            para['title'] = title
            para['url'] = url
            para['price'] = price
            para['tb_cid'] = tb_cid
            para['isbn'] = isbn

            cat = self.__rule.classify(url, tb_cid, None)
            # if cat is None or len(cat) == 0:
            #     cat = self.__classifier.classifiy(para)

            if cat is None or len(cat) == 0:
                return

            self.write(cat, price+'#'+pv)

        except Exception, e:
            raise e


class StatPriceReducer(PyReducer):

    def __init__(self, sys_in):
        PyReducer.__init__(self, sys_in)

    def handle_reduce(self, key, values):
        price_dict = {}

        for v in values:
            arr = v.split('#')
            price = float(arr[0])
            price = int(price - price % 10)
            count = int(arr[1])
            util.incre_dict(price_dict, price, count)

        items = sorted(price_dict.items(), key=lambda x: x[0])
        price_dict = {}
        l = len(items)

        t = l / 5 + 1
        i = 0
        while True:
            v_arr = items[i:i+t]
            if len(v_arr) <= 0:
                break
            price_dict[v_arr[0][0]] = reduce(lambda y, x: y+x[1], v_arr, 0)
            i += t

        for k, v in price_dict.items():
            self.write(key, str(k)+'#'+str(v))


def report():
    cat_dict = {}
    reader = MultiFileReader('/home/hdp-dianshang/jinxueyu/goods-classification/stat/cat/20150410/')
    for line in reader:
        arr = line.split('\t')
        if arr[0] not in cat_dict:
            cat_dict[arr[0]] = [arr[1], []]
    reader.close()

    reader = MultiFileReader('/home/hdp-dianshang/jinxueyu/goods-classification/stat/price/20150410/')
    for line in reader:
        arr = line.split('\t')
        p_arr = arr[1].split('#')
        cat_dict[arr[0]][1].append((p_arr[0], p_arr[1]))
    reader.close()

    category = Category()
    writer = FileWriter('/home/hdp-dianshang/jinxueyu/goods-classification/stat/report')
    for k, v in cat_dict.items():
        s = ''
        l = sorted(v[1], key=lambda x: int(x[0]))
        for item in l:
            s += str(item[0])+','+item[1]+'\t'

        k = category.get_cat_name(k)+'('+k+')'
        writer.write(k+'\t'+v[0]+'\t'+s)

    writer.close()

if __name__ == '__main__':
    task = sys.argv[2]
    service = sys.argv[1]
    if service == 'cat':
        if task == 'map':
            mapper = StatMapper(sys.stdin)
            mapper.run()
        elif task == 'reduce':
            reducer = StatReducer(sys.stdin)
            reducer.run()
    elif service == 'price':
        if task == 'map':
            mapper = StatPriceMapper(sys.stdin)
            mapper.run()
        elif task == 'reduce':
            reducer = StatPriceReducer(sys.stdin)
            reducer.run()
    elif service == 'report':
        report()