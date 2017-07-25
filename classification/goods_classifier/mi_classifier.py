# -*- coding: utf-8 -*-
"""
Date    : 15/4/13
Author  : baylor
"""

import sys
import os


prj_path = os.path.split(os.path.realpath(__file__))[0]+'/../../'
sys.path.append(prj_path)
import math
from common.base.strings import Strings
from common.io.file_io import MultiFileReader
from common.io import FileReader
from classification.goods_classifier.features import GoodsFeatureParser


def round_float(f):
    f = round(f, 4)
    str_f = str(f)
    return Strings.parse_float(str_f)


__author__ = 'baylor'


class MInfoLoader(object):

    def __init__(self, input_path):
        self.__feature_count_dict = {}
        self.__label_count_dict = {}
        self.__label_feature_count_dict = {}
        # ??????????? why this name ?
        self.__label_total_count = 0

        self.__load(input_path)

        self.__label_feature_weight = self.__compute_label_feature_weight()

        self.__feature_weight = self.__compute_feature_weight()
        self.__feature_label_list = self.__compute_feature_labels_dict()

        del self.__feature_count_dict, self.__label_count_dict, self.__label_feature_count_dict

    def __load(self, input_path):
        reader = MultiFileReader(input_path)

        for line in reader:
            if line.find('__total_count__') == 0:
                key, value = line.split('_count__', 1)
                self.__label_total_count = float(value)
                continue

            key, line = line.split('_', 1)
            if key == 'lf':
                label_feature, count = line.split('\t', 1)
                label, feature = label_feature.split('_', 1)
                if label not in self.__label_feature_count_dict:
                    self.__label_feature_count_dict[label] = {}
                self.__label_feature_count_dict[label][feature] = int(count)
                continue

            label, count = line.split('\t', 2)
            count = int(count)
            if key == 'l':
                self.__label_count_dict[label] = count

            if key == 'f':
                self.__feature_count_dict[label] = count

        reader.close()

    def __compute_label_feature_weight(self):
        f_count = 0
        label_feature_weight = {}

        for label, label_feature_count_dict in self.__label_feature_count_dict.items():
            label_count = self.__label_count_dict[label]
            # # recompute label_feature_count_dict
            for feature, label_feature_count in label_feature_count_dict.items():
                feature_count = self.__feature_count_dict[feature]
                # p_weight = total_count * (l_f_c) / (l_w * f_w)
                # label_feature_count[feature] = math.log(p_weight)
                p_weight = self.__label_total_count * label_feature_count / (label_count * feature_count)
                del label_feature_count_dict[feature]
                try:
                    label_feature_count_dict[feature] = round_float(math.log(p_weight))
                except Exception, e:
                    print p_weight, self.__label_total_count, label_feature_count, (label_count, feature_count)
                    raise e
            # finish 1 label
            label_feature_weight[label] = label_feature_count_dict

            f_count += len(label_feature_count_dict)
            del label, label_feature_count_dict

        print 'feature_count', f_count
        return label_feature_weight

    def __compute_feature_weight(self):
        feature_weight = {}
        max_weight = None
        for feature, count in self.__feature_count_dict.items():
            feature_weight[feature] = math.log(count / self.__label_total_count)
            if max_weight is None or max_weight > feature_weight[feature]:
                max_weight = feature_weight[feature]
        # ## normalize to max_weight
        for feature, weight in feature_weight.items():
            del feature_weight[feature]
            feature_weight[feature] = round_float(weight / max_weight * - 1)
        return feature_weight

    # # compute an inverted index from feature-->labels, to improve the efficiency of classify
    # # it's used to candidate a possible label to compute when classify
    def __compute_feature_labels_dict(self):
        feature_label_list_dict = {}
        for label, feature_weight_dict in self.__label_feature_weight.items():
            for feature in feature_weight_dict.keys():
                if feature not in feature_label_list_dict:
                    feature_label_list_dict[feature] = []

                if feature_weight_dict[feature] < 0:
                    continue

                feature_label_list_dict[feature].append(label)

        return feature_label_list_dict

    def get_smi_result(self):
        return self.__label_feature_weight, self.__feature_weight, self.__feature_label_list

    def print_smi_result(self):
        print '__label_feature_weight:\n'
        for label, feature_weight_dict in self.__label_feature_weight.items():
            for feature, weight in feature_weight_dict.items():
                print str(label) + '\t' + feature + '\t' + str(weight)
            print '\n'

        print '\n__feature_weight:\n'
        for feature, weight in self.__feature_weight.items():
            print feature + '\t' + str(weight)

        print '\n__feature_label_list:\n'
        for feature, label_list in self.__feature_label_list.items():
            ss = feature + '\t'
            for label in label_list:
                ss += str(label) + ','
            print ss

# class MILoader(object):
#     def __init__(self, fc_file_path, lc_file_path, smi_file_path):
#         self.__feature_count_dict = self.__load_word_count(fc_file_path)
#         self.__label_count_dict = self.__load_word_count(lc_file_path)
#
#         self.__label_total_count = int(self.__label_count_dict['__total_count__']) * 1.0
#
#         self.__label_feature_weight = self.__compute_label_feature_weight(smi_file_path)
#
#         self.__feature_weight = self.__compute_feature_weight()
#         self.__feature_label_list = self.__compute_feature_labels_dict()
#
#         del self.__feature_count_dict, self.__label_count_dict
#
#     def get_int(self, s):
#         return Strings.parse_int(s)
#
#     def parse_label_and_feature_count_dict(self, smi_string):
#         items = smi_string.split('\t')
#         if len(items) != 2:
#             return None
#         label = items[0]
#         feature_count_string = items[1]
#         feature_count_items = feature_count_string.split(';')
#         feature_count_dict = {}
#         for feature_count_item in feature_count_items:
#             feature_count = feature_count_item.split(':')
#             if len(feature_count) != 2:
#                 continue
#             feature = feature_count[0]
#             count = feature_count[1]
#
#             feature = Strings.parse(feature)
#             feature_count_dict[feature] = Strings.parse_int(count)
#
#             del feature_count
#
#         del items
#         label = Strings.parse(label)
#         return label, feature_count_dict
#
#     def load_lf_count(self):
#         pass
#
#     def __compute_label_feature_weight(self, smi_file_path):
#         f_count = 0
#         label_feature_weight = {}
#         smi_reader = open(smi_file_path, 'r')
#         while True:
#             line = smi_reader.readline()
#             if not line:
#                 break
#             label, label_feature_count_dict = self.parse_label_and_feature_count_dict(line)
#             label_count = self.__label_count_dict[label]
#             # # recompute label_feature_count_dict
#             for feature, label_feature_count in label_feature_count_dict.items():
#                 feature_count = self.__feature_count_dict[feature]
#                 # p_weight = total_count * (l_f_c) / (l_w * f_w)
#                 # label_feature_count[feature] = math.log(p_weight)
#                 p_weight = self.__label_total_count * label_feature_count / (label_count * feature_count)
#                 del label_feature_count_dict[feature]
#                 label_feature_count_dict[feature] = round_float(math.log(p_weight))
#             # finish 1 label
#             label_feature_weight[label] = label_feature_count_dict
#
#             f_count += len(label_feature_count_dict)
#             del line, label, label_feature_count_dict
#
#         smi_reader.close()
#
#         print 'feature_count', f_count
#         return label_feature_weight
#
#     def get_smi_result(self):
#         return self.__label_feature_weight, self.__feature_weight, self.__feature_label_list
#
#     def print_smi_result(self):
#         print '__label_feature_weight:\n'
#         for label, feature_weight_dict in self.__label_feature_weight.items():
#             for feature, weight in feature_weight_dict.items():
#                 print str(label) + '\t' + feature + '\t' + str(weight)
#             print '\n'
#
#         print '\n__feature_weight:\n'
#         for feature, weight in self.__feature_weight.items():
#             print feature + '\t' + str(weight)
#
#         print '\n__feature_label_list:\n'
#         for feature, label_list in self.__feature_label_list.items():
#             ss = feature + '\t'
#             for label in label_list:
#                 ss += str(label) + ','
#             print ss
#
#     def __load_word_count(self, file_path):
#         word_count_dict = {}
#         reader = open(file_path, 'r')
#         while True:
#             line = reader.readline()
#             if not line:
#                 break
#             word_count = line.rstrip().split(',')
#             if len(word_count) != 2:
#                 continue
#             word = word_count[0]
#             count = word_count[1]
#
#             k_word = Strings.parse(word)
#             word_count_dict[k_word] = self.get_int(count)
#
#             del count
#             del word
#             del word_count
#             del line
#         reader.close()
#         return word_count_dict
#
#     def __compute_feature_weight(self):
#         feature_weight = {}
#         max_weight = None
#         for feature, count in self.__feature_count_dict.items():
#             feature_weight[feature] = math.log(count / self.__label_total_count)
#             if max_weight is None or max_weight > feature_weight[feature]:
#                 max_weight = feature_weight[feature]
#         # ## normalize to max_weight
#         for feature, weight in feature_weight.items():
#             del feature_weight[feature]
#             feature_weight[feature] = round_float(weight / max_weight * - 1)
#         return feature_weight
#
#     # # compute an inverted index from feature-->labels, to improve the efficiency of classify
#     # # it's used to candidate a possible label to compute when classify
#     def __compute_feature_labels_dict(self):
#         feature_label_list_dict = {}
#         for label, feature_weight_dict in self.__label_feature_weight.items():
#             for feature in feature_weight_dict.keys():
#                 if feature not in feature_label_list_dict:
#                     feature_label_list_dict[feature] = []
#
#                 if feature_weight_dict[feature] < 0:
#                     continue
#
#                 feature_label_list_dict[feature].append(label)
#
#         return feature_label_list_dict


class MIClassifier(object):
    def __init__(self, file_path):
        self.__stop_words = ['淘宝', '代购', '现货', '促销', '特价', '清仓']
        self.__gender_words = ['男', '女', '童']
        self.__only_words = ['幼儿', '儿童', '男士', '女式', '男', '女']

        self.__loader = MInfoLoader(file_path)
        self.__label_feature_weight, self.__feature_weight, self.__feature_label_list = self.__loader.get_smi_result()
        # self.__loader.print_smi_result()

    # ## compute score between feature_doc and label
    def compute_score_between(self, feature_doc, label):
        # ## product_weight
        total_words = 0
        total_words += len(feature_doc)
        if total_words <= 4:
            product_weight = 2
        else:
            product_weight = math.log(total_words, 2)
        # compute score
        score = 0
        feature_weight = self.__label_feature_weight[label]
        for pf in feature_doc:
            property_field = pf[0]
            feature = pf[1]
            feature_score = 0
            if feature_weight.has_key(feature):
                if feature in self.__stop_words:
                    continue
                feature_score = feature_weight[feature]
            else:
                if self.__feature_weight.has_key(feature):
                    feature_score = self.__feature_weight[feature]
            if feature.find('孕妇') >= 0 or feature.find('婴幼儿') >= 0 or feature.find('宝贝') >= 0:
                feature_score *= 4.8
            if property_field == 'product':
                feature_score *= product_weight
            elif property_field == 'brand':
                feature_score *= product_weight
            elif property_field == 'gender' and (feature in self.__gender_words):
                feature_score *= product_weight
            elif property_field == 'only':
                feature_score *= product_weight
                if feature in self.__only_words:
                    feature_score *= 2
            elif property_field == 'seg_nr':
                feature_score = feature_score * product_weight / 2

            score += feature_score
        # # return score
        return score

    def select_labels(self, feature_doc):
        selected_labels = []

        select_feature = filter(lambda x: x[1] == 'product' or x[1] == 'brand', feature_doc)
        if len(select_feature) == 0:
            select_feature = feature_doc

        for feature_list in select_feature:
            # if feature_list[0] != 'product':
            #     continue
            feature = feature_list[1]
            if feature in self.__feature_label_list:
                label_list = self.__feature_label_list[feature]
                selected_labels += label_list
        return set(selected_labels)  # ## remove duplicate

    # # feature_doc:{property: [feature1, feature2,,,]}
    # ##
    def classify_by_feature_doc(self, feature_doc):
        # ## classfiy by score
        result_label = None
        result_score = None
        selected_labels = self.select_labels(feature_doc)

        for label in selected_labels:
            # for label in self.__label_feature_weight.keys():
            score = self.compute_score_between(feature_doc, label)
            if result_score is None or score > result_score:
                result_label = label
                result_score = score
        if not result_score > 0.0 or result_label is None:
            result_label = '-1'
        return result_label


if __name__ == '__main__':
    file_path = '/home/hdp-dianshang/jinxueyu/goods-classification/model.dat'
    file_path = '/data/recommend/goods-classification/model.dat'

    line = '-1000888176652623960\tbrand,kidstar,1;tags,儿童,1;gender,儿童,1;product,汽车安全座椅,1;seg_n,靠背,1;tags,可调,1;' \
           'seg_e,可,1;seg_v,躺,1;seg_d,双向,1;seg_v,安装,1;seg_nx,/0-4,1;seg_q,岁,1;seg_nx,ece,1;seg_vn,认证,1;\t1367'
    l = map(lambda x: x.split(','), line.split('\t')[1].split(';')[0:-1])
    print l

    c = MIClassifier(file_path)
    parser = GoodsFeatureParser()
    # goods_doc = {'name': title, 'url': url, 'cid': tb_cid}
    doc = parser.parse()

    print c.classify_by_feature_doc(l)