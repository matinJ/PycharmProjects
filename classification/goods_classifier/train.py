# -*- coding: utf-8 -*-
"""
Date    : 15/4/13
Author  : baylor
"""
import sys
import os

prj_path = os.path.split(os.path.realpath(__file__))[0]+'/../../'
sys.path.append(prj_path)

from classification.goods_classifier.mi import StatisticsTask
from rule_classifier import RuleBaseClassifier
from common.base import StringBuilder
from common.base.strings import Strings
from common.collections import Seq
from features import GoodsFeatureParser
from common.io import FileReader, FileWriter


__author__ = 'baylor'


def wrap_doc(fields, values):
    return Seq(fields).zip(values).filter(lambda x: x[0] is not None and len(x[0]) > 0).value_to_dict()


def test():
    l = 'a,b,c,d,e,f'.split(',')

    seq = Seq(l)
    print seq.zip([1, 2, 3, 4, 5, 6])\
        .map(lambda x: (x[1], x[0]))\
        .filter(lambda x: x[0] > 3)\
        .value_to_dict()

    values = l
    fields = ['1', '2', '3', '', None, '6']
    f = ['1', '2', '3', '4', '5', '6']
    obj = wrap_doc(fields, values)
    seq = Seq(obj)
    print seq.filter(lambda x: x[0] in f).sort(key=lambda x:x[0]).value()

    print Seq(f).map(lambda x: ((x in obj) and (x, obj[x])) or (x, '')).value()

    items = Seq(fields).map(lambda x: ((x in obj) and (x, Strings.parse(obj[x].replace('\n', '  ')))) or (x, ''))\
        .map(lambda x: x[1])

    print items.value()

    print Seq(f).value_to_string()


def train():
    # 1. feature extract
    feature_extract()
    # 2.train model
    train_model()
    # 3.evaluation
    evaluation()


def train_model():
    i = '/home/hdp-dianshang/jinxueyu/goods-classification/train.set'
    o = i + '.smi'
    task = StatisticsTask(i, o, 'label')
    task.run()


def evaluation():
    pass


def select_training_data_set():
    pass


def feature_extract():
    rule = RuleBaseClassifier(prj_path+'../data/rules/')
    feature_parser = GoodsFeatureParser()

    writer = FileWriter('/home/hdp-dianshang/jinxueyu/goods-classification/train.set')
    writer.write('#fields\tid\tfeatures\tlabel')
    reader = FileReader('/home/hdp-dianshang/jinxueyu/goods-classification/goods-snapshot')

    fields = ['id', 'name', 'url', 'cid', 'price', 'isbn', 'pv']
    sep = '\t'

    count = 0
    for line in reader:
        count += 1
        if count % 10000 == 0:
            print '[feature_extract count]', count

        if line.startswith('#fields'):
            fields = line.split('\t')[1:]
            continue

        if line.startswith('#'):
            continue

        # wrap goods
        goods_doc = wrap_doc(fields, line.split(sep))

        feature_list = feature_parser.parse(goods_doc)
        goods_id = goods_doc['id']

        # write in file
        sb = StringBuilder()
        sb.append(goods_id).append('\t')

        for feature in feature_list:
            sb.append(feature[0]).append(',').append(feature[1]).append(',').append(feature[2]).append(';')

        label = rule.classify(goods_doc.get('url'), goods_doc.get('cid'), None)
        if label is None:
            continue

        sb.append('\t').append(label)

        writer.write(sb.to_string())

    reader.close()
    writer.close()


if __name__ == '__main__':
    if len(sys.argv[1]) <= 1:
        test()
        exit()

    func = sys.argv[1]
    if func == 'feature_extract':
        feature_extract()

    if func == 'train':
        train_model()
