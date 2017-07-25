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
from common import json

from base.mapreduce import PyMapper, PyReducer


class ParseMapper(PyMapper):
    def __init__(self, sys_in):
        PyMapper.__init__(self, sys_in, False)
        self.__field_list = set(['seg_nx', 'url', 'cid', 'price', 'isbn', 'pv', 'domain'])

    def parse_feat(self, line):
        s = {}
        arr = line.rstrip().split('\t')
        s['label'] = arr[2]
        features = arr[1].split(';')

        s['features'] = set()

        for v in features:
            if len(v) == 0:
                continue

            v = v.split(',')
            field = v[0]

            if field in self.__field_list:
                continue

            if field.startswith('seg_') and len(v[1]) < 2:
                continue

            s['features'].add(v[1])

            if field == 'product':
                s['product'] = v[1]
        return s

    def handle_map(self, key, value):
        try:

            feat = self.parse_feat(value)

            features = feat['features']
            if 'label' in feat:
                labels = feat['label']
            else:
                return

            if isinstance(labels, str):
                label = labels
                labels = [label]

            for label in labels:
                if label == '-1' or label == 'NA':
                    return

                self.write('l_'+label, '1')

                for f in features:
                    self.write('lf_'+label+'_'+f, 1)

            for f in features:
                self.write('f_'+f, '1')

            self.write('__total_count__', '1')

        except Exception, e:
            print value
            raise e


class ParseReducer(PyReducer):

    def __init__(self, sys_in):
        PyReducer.__init__(self, sys_in)

    def handle_reduce(self, key, values):
        # line = ','.join(values)
        pv = len(values)

        self.write(key, str(pv))

if __name__ == '__main__':
    task = sys.argv[1]
    if task == 'map':
        mapper = ParseMapper(sys.stdin)
        mapper.run()
    elif task == 'reduce':
        reducer = ParseReducer(sys.stdin)
        reducer.run()