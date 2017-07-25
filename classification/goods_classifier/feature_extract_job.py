# -*- coding: utf-8 -*-
"""
Date    : 15/4/10
Author  : baylor
"""


__author__ = 'baylor'

import sys
import os
prj_path = os.path.split(os.path.realpath(__file__))[0]+'/../../'
sys.path.append(prj_path)

from common.collections import Seq

from features import GoodsFeatureParser
from rule_classifier import RuleBaseClassifier
from common.base import StringBuilder

from base.mapreduce import PyMapper, PyReducer


def wrap_doc(fields, values):
    return Seq(fields).zip(values).filter(lambda x: x[1] is not None and len(x[1]) > 0).value_to_dict()


class ParseMapper(PyMapper):
    def __init__(self, sys_in):
        PyMapper.__init__(self, sys_in, False)
        self.__fields = ['id', 'name', 'url', 'cid', 'price', 'isbn', 'pv']
        self.__rule = RuleBaseClassifier()
        self.__feature_parser = GoodsFeatureParser()

    def handle_map(self, key, value):
        try:
            sep = '\t'

            # wrap goods
            goods_doc = wrap_doc(self.__fields, value.split(sep))

            feature_list = self.__feature_parser.parse(goods_doc)
            goods_id = goods_doc['id']

            # write in file
            sb = StringBuilder()

            i = 0
            for feature in feature_list:
                if i > 0:
                    sb.append(';')
                sb.append(feature[0]).append(',').append(feature[1]).append(',').append(feature[2])
                i += 1

            label = self.__rule.classify(goods_doc.get('url'), goods_doc.get('cid'), None)
            if label is None:
                return

            sb.append('\t').append(label)

            self.write(str(goods_id), sb.to_string())
        except Exception, e:
            raise e

if __name__ == '__main__':

    task = sys.argv[1]
    if task == 'map':
        mapper = ParseMapper(sys.stdin)
        mapper.run()