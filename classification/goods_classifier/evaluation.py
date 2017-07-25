# -*- coding: utf-8 -*-
"""
Created on 2014-12-8

@author: jinxueyu
"""

import sys
import os
prj_path = os.path.split(os.path.realpath(__file__))[0]+'/../../'
sys.path.append(prj_path)

from classification.goods_classifier.rule_classifier import RuleBaseClassifier
from classification.goods_classifier.category import Category
from common.io.file_io import MultiFileReader, FileWriter
from classification.goods_classifier.mi_classifier import MIClassifier
from common.io import FileReader
from classification.goods_classifier.features import GoodsFeatureParser
from common.collections import Seq


class Evaluator(object):
    def __init__(self):
        pass

    __total = 0
    __error_count = 0
    __error_list = []

    def evaluate(self, obj_id, obj, func, target):
        self.__total += 1
        result = func(obj)
        if result != target:
            self.__error_count += 1
            self.__error_list.append([obj_id, result, target])
        return result

    def get_accuracy(self):
        return 1.0 * (self.__total - self.__error_count) / self.__total

    def get_error_list(self):
        return self.__error_list


def wrap_doc(fields, values):
    return Seq(fields).zip(values).filter(lambda x: x[0] is not None and len(x[1]) > 0).value_to_dict()

if __name__ == '__main__':
    fields = ['id', 'name', 'url', 'cid', 'price', 'isbn', 'pv']
    filter_fields = set(['id', 'url', 'cid', 'price', 'isbn', 'pv', 'domain'])
    rule = RuleBaseClassifier()

    cat = Category()
    featureParser = GoodsFeatureParser()
    model_path = '/home/hdp-dianshang/jinxueyu/goods-classification/model/20150410'
    feature_path = '/home/hdp-dianshang/jinxueyu/goods-classification/evaluation/test_data'

    c = MIClassifier(model_path)

    evaluator = Evaluator()

    reader = FileReader(feature_path)

    doc_dict = {}

    error_count = [0, 0, 0]
    total_count = 0.0
    for line in reader:
        doc = wrap_doc(fields, line.split('\t'))
        if 'isbn' in doc and len(doc['isbn']) > 0:
            continue

        target = rule.classify(doc['url'], doc.get('cid'), None)
        if target is None:
            continue

        l = featureParser.parse(doc)
        l = filter(lambda x: x[0] not in filter_fields, l)
        result = evaluator.evaluate(doc['id'], l, c.classify_by_feature_doc, target)

        if target != result:
            doc_dict[doc['id']] = doc
            error_count[0] += 1

        result = cat.get_cat_parent(result)
        target = cat.get_cat_parent(target)
        if target != result:
            error_count[1] += 1

        result = cat.get_cat_parent(result)
        target = cat.get_cat_parent(target)
        if target != result:
            error_count[2] += 1

        total_count += 1

    reader.close()

    print 'accuracy:', (total_count - error_count[0])/total_count, (total_count - error_count[1])/total_count, \
        (total_count - error_count[2])/total_count

    # report format
    # goods_id, goods_url, goods_title, cat3, cat3, cat2, cat2, cat1, cat1

    error_list = evaluator.get_error_list()
    error_dict = {}
    for e_line in error_list:
        error_dict[e_line[0]] = e_line

    writer = FileWriter('/home/hdp-dianshang/jinxueyu/goods-classification/evaluation/evaluation_result')
    for k, v in error_dict.items():
        # obj_id, result, target, 'name', 'url'
        doc = doc_dict[k]
        line = k + '\t' + doc['url'] + '\t' + doc['name'] + '\t' + \
            str(cat.get_cat_name(v[1])) + '\t' + str(cat.get_cat_name(v[2])) + '\t' + \
            str(cat.get_cat_name(cat.get_cat_parent(v[1]))) + '\t' + \
            str(cat.get_cat_name(cat.get_cat_parent(v[2]))) + '\t' + \
            str(cat.get_cat_name(cat.get_cat_parent(cat.get_cat_parent(v[1])))) + '\t' + \
            str(cat.get_cat_name(cat.get_cat_parent(cat.get_cat_parent(v[2]))))
        writer.write(line)
    writer.close()