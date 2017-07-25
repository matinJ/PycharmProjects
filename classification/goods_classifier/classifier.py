# -*- coding: utf-8 -*-
import sys
import gc
import os

from classification.goods_classifier.features import GoodsFeatureParser
from classification.goods_classifier.mi_classifier import MIClassifier
from classification.goods_classifier.rule_classifier import RuleBaseClassifier


class CompositiveClassifier(object):
    """
    This class is just the encapsulation of MIClassifier and RuleBaseClassifier. providing 3 classifier:
    B2c Classifier and Taobao Classifier & rule base classifier
    """

    def __init__(self, file_path):

        print 'b2c_smi_file'
        self.__b2c_classifier = MIClassifier(file_path)
        print 'b2c_smi_file over '
        print 'taobao_smi_file '
        self.__taobao_classifier = self.__b2c_classifier
        print 'taobao_smi_file over '
        self.__rule_base_classifier = RuleBaseClassifier()
        self.__feature_parser = GoodsFeatureParser()

        gc.collect()

    def classify_by_feature_doc(self, feature_doc, is_b2c):
        if is_b2c:
            return self.__b2c_classifier.classify_by_feature_doc(feature_doc)
        # if isbn return
        return self.__taobao_classifier.classify_by_feature_doc(feature_doc)

    def classify(self, url, tag, title, tb_cid=None, price=None, isbn=None):
        label = None
        labels = self.__rule_base_classifier.classify(url, tb_cid=tb_cid, tag=tag)
        if label is None:
            pass
        elif len(label) == 1:
            label = labels[0]
            return label

        goods_doc = {'name': title, 'url': url, 'cid': tb_cid, 'price': price, 'isbn': isbn}

        feature_doc = self.__feature_parser.parse(goods_doc)
        if feature_doc is None:
            return None

        if url.find('.taobao.com') > 0 or url.find('.tmall.com') > 0:
            label = self.classify_by_feature_doc(feature_doc, False)
        else:
            label = self.classify_by_feature_doc(feature_doc, True)

        return label


if __name__ == '__main__':

    print 'gc:', gc.get_threshold()
    classifier = CompositiveClassifier()

    print 'please input:'
    while True:
        line = sys.stdin.readline()
        print line

        if line == 'exit':
            break

        arr = line.split(' ')

        # url = arr[0]
        # tag = arr[1]
        # title = arr[2]

        # print classifier.classify(url, tag, title)