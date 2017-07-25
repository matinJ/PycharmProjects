"""
Date    : 15/4/20
Author  : baylor
"""
import os
import sys
prj_path = os.path.split(os.path.realpath(__file__))[0]+'/../../'
sys.path.append(prj_path)
from learning.information_gain import InfoGain, IGPrepareMapper, IGPrepareReducer, IGEntropyMapper, IGEntropyReducer, \
    IGPrepareCombiner

__author__ = 'baylor'


class FeatureMapper(IGPrepareMapper):
    __field_list = set(['url', 'cid', 'price', 'isbn', 'pv', 'domain'])

    def extract_features(self, line):
        arr = line.split('\t')
        label = arr[1]

        features = map(lambda x: x.split(','), arr[0].split(';'))
        features = filter(lambda x: x[0] not in self.__field_list, features)
        features = map(lambda x: x[1], features)
        return label, features


class FeatureReducer(IGPrepareReducer):
    pass


class FeatureEntropyMapper(IGEntropyMapper):
    __field_list = set(['url', 'cid', 'price', 'isbn', 'pv', 'domain'])

    def extract_features(self, line):
        arr = line.split('\t')
        label = arr[1]

        features = map(lambda x: x.split(','), arr[0].split(';'))
        features = filter(lambda x: x[0] not in self.__field_list, features)
        features = map(lambda x: x[1], features)
        return label, features


class FeatureEntropyReducer(IGEntropyReducer):
    pass


if __name__ == '__main__':
    task = sys.argv[1]

    if task == 'ppmap':
        task = FeatureMapper()
        task.run()
    elif task == 'ppreduce':
        task = FeatureReducer()
        task.run()
    elif task == 'igmap':
        task = FeatureEntropyMapper()
        task.run()
    elif task == 'igcombiner':
        task = IGPrepareCombiner()
        task.run()
    elif task == 'igreduce':
        task = FeatureEntropyReducer(os.path.split(os.path.realpath(__file__))[0]+'/cat_info')
        task.run()
    else:
        ig = InfoGain('/home/hdp-dianshang/jinxueyu/goods-classification/goods_feature_selection/20150410/')
        term_list = ig.get_ig_list()
        for term in term_list:
            print term[0], term[1]