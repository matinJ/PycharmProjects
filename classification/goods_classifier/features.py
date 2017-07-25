# -*- coding: utf-8 -*-
"""
Date    : 15/4/13
Author  : baylor
"""
from classification.goods_classifier import util
from common.base.strings import Strings
try:
    from segment import TcAnalyzer
except:
    pass

__author__ = 'baylor'


class FeatureParser(object):
    def __init__(self):
        pass

    def feature_extract(self):
        pass

    def feature_select(self):
        pass

    def feature_transform(self):
        pass


class GoodsFeatureParser(FeatureParser):
    def __init__(self):
        self.gender_male = '男'
        self.gender_female = '女'
        self.gender_child = '童'
        self.seg = TcAnalyzer()

    def parse(self, goods_doc):
        title = goods_doc.get('name')
        url = goods_doc.get('url')
        price = goods_doc.get('price')
        cid = goods_doc.get('cid')
        isbn = goods_doc.get('isbn')

        feature_list = self.feature_extract(title, url, price, cid, isbn)
        feature_list = self.feature_transform(feature_list)
        feature_list = self.feature_select(feature_list)

        return feature_list

    def feature_extract(self, title, url, price, cid, isbn):
        feature_list = []

        if title is not None:
            title = title.decode('utf8', 'ignore').encode('gbk', 'ignore')
            word_tag_list = self.seg.get_word_tag(title)
            for w in word_tag_list:
                # word
                if len(w[0].rstrip()) <= 0 or w[1] == 'w':
                    continue

                k = w[0].decode('gbk', 'ignore').encode('utf8', 'ignore')
                feature_list.append((k, w[1]))

        if not Strings.is_empty(url):
            # domain
            domain = util.get_domain_f_url(url)
            if not Strings.is_empty(domain):
                feature_list.append((domain, 'o_domain'))
        if not Strings.is_empty(price):
            feature_list.append((price, 'o_price'))
        if not Strings.is_empty(cid):
            feature_list.append((cid, 'o_cid'))
        if not Strings.is_empty(isbn):
            feature_list.append((isbn, 'o_isbn'))

        return feature_list

    def feature_transform(self, feature_list):
        """
        归一化
        """
        tf_feature_list = []
        gender = None
        for w in feature_list:
            # f
            if w[1].startswith('o_'):
                f = w[1].split('_')[-1]
            else:
                f = 'seg_' + w[1]

            # f-->wordlist
            word = w[0]
            # if f not in feat_doc:
            #     feat_doc[f] = []
            # if word not in feat_doc[f]:
            #     feat_doc[f].append(word)
            tf_feature_list.append((f, word, 1))

            # if add gender
            if gender is None:
                gender = self.check_gender(word)
                if gender is not None:
                    # feat_doc['gender'] = [gender]
                    tf_feature_list.append(('gender', word, 1))

        return tf_feature_list

    def feature_select(self, feature_list):

        select_feature_list = []
        for feature in feature_list:
            if feature[0].startswith('seg_'):
                if len(feature[0]) <= 1:
                    continue

            select_feature_list.append((feature[0], feature[1], feature[2]))
        return select_feature_list

    def check_gender(self, word):
        if word.find(self.gender_male) >= 0:
            return self.gender_male
        elif word.find(self.gender_female) >= 0:
            return self.gender_female
        if word.find(self.gender_child) >= 0:
            return self.gender_child
        return None