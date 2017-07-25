# -*- coding: utf-8 -*-
"""
Created on 2013-7-23

@author: jinxueyu
"""

from miaomiao.core.rank import Ranker
from miaomiao.core.commons import BinHeap

'''
P(C|D) = P(D|C)*P(C) / P(D) = P(w1|C)*P(w2|C)*...*P(wn|C) * P(C) / P(D)

1.multinomial
P(C) = (the total count of words in class C) / ( the count of words in all the docs)
P(w|C) = (the count of words 'w' which in the docs of class C + 1 ) /
         (the total count of all the words in all the docs Of class C + |V|)

2.bernoulli
P(C) = (the total count of docs in class C) / (the count of all the docs)
P(w|C) = (the count of docs which contains the 'w' + 1 ) / (the total count of docs in class C + 2)


output file format

0:model name
1:|V|
2:total count for Class
3:count of words for Class

'''


class Bayesian(object):

    def extract_feature(self, goods, fields_list=None):
        values = []

        if fields_list is None:
            for k, v in goods.items():
                arr1 = v.split(',')
                values.extend(arr1)
        else:
            for field in fields_list:
                if goods.has_key(field):
                    v = goods[field]
                    arr1 = v.split(',')
                    values.extend(arr1)

        comb_features = []
        i = 0
        l = len(values)
        while i < l:
            v0 = values[i]
            i += 1
            j = i
            while j < l:
                v1 = values[j]
                j += 1
                if v1 == v0:
                    continue

                if v0 > v1:
                    feature = v0 + '_' + v1
                else:
                    feature = v1 + '_' + v0
                comb_features.append(feature)

        return comb_features


class BayesRanker(Ranker, Bayesian):
    def __init__(self, model_path, fields_list=None):
        self.__prob = {}
        self.__load(model_path)
        self.__fields_list = fields_list

    def __load(self, input_path):
        reader = open(input_path, 'r')
        i = -1
        pos_count = 0
        neg_count = 0
        total_words_count = 0
        while True:
            line = reader.readline()
            if not line:
                break
            i += 1

            if i == 0:
                self.__model_name = line
                continue
            if i == 1:
                total_words_count = int(line)
                continue

            arr = line.split('\t')
            if i == 2:
                pos_count = float(arr[0])
                neg_count = float(arr[1])

                self.__prob['class'] = [pos_count / (pos_count + neg_count), neg_count / (pos_count + neg_count)]

                # multinomial
                pos_count += total_words_count
                neg_count += total_words_count
                continue

            self.__prob[arr[0]] = [(float(arr[1]) + 1) / pos_count, (float(arr[2]) + 1) / neg_count]

        reader.close()

    def rank(self, goods):

        comb_features = self.extract_feature(goods, self.__fields_list)

        score0 = 1
        score1 = 1
        for feature in comb_features:
            if not self.__prob.has_key(feature):
                continue
            score0 *= self.__prob[feature][0]
            score1 *= self.__prob[feature][1]

        score0 *= self.__prob['class'][0]
        score1 *= self.__prob['class'][1]

        return score0, score1

    def score(self, goods):
        score0, score1 = self.rank(goods)
        return score0 / score1


class BayesianTrainer(Bayesian):
    '''
    class docs
    '''

    def __init__(self, model_name, input_path, output_path):
        '''
        Constructor
        '''
        # multinomial
        #         bernoulli

        self.__model_name = model_name
        self.__reader = open(input_path, 'r')
        self.__writer = open(output_path, 'w')

        self.__feature_count_dict = {'total': [0, 0]}

    __feature_count_dict = None
    __doc_count_dict = {}

    def __wrap_doc(self, line):
        doc = {}
        arr = line.split('\t')

        i = 0
        l = len(arr)
        while i < l:
            key = arr[i]
            i += 1
            value = arr[i]
            i += 1

            if key not in ['product', 'brand', 'cat', 'shop', 'pv']:
                continue

            if key == 'pv':
                key = 'label'
                value = int(value)

                if value >= 1000:
                    value = 'pos'
                elif 400 < value < 500:
                    value = 'neg'
                else:
                    return None

            doc[key] = value

        return doc

    def __stat_feature(self, doc):

        label = doc.pop('label')

        features = self.extract_feature(doc)

        for feature in features:
            if not self.__feature_count_dict.has_key(feature):
                self.__feature_count_dict[feature] = [0, 0]

            k = None
            if label == 'pos':
                k = 0
            else:
                k = 1

            if 'multinomial' == self.__model_name:
                self.__feature_count_dict[feature][k] += 1
                self.__feature_count_dict['total'][k] += 1
            else:
                pass

    def __write(self):
        self.__writer.write(self.__model_name + '\n')
        self.__writer.write(str(len(self.__feature_count_dict) - 1) + '\n')
        self.__writer.write(
                str(self.__feature_count_dict['total'][0]) + '\t' + str(self.__feature_count_dict['total'][1]) + '\n')

        for k, v in self.__feature_count_dict.items():
            self.__writer.write(k + '\t' + str(v[0]) + '\t' + str(v[1]) + '\n')

    def train(self):
        count = 0
        while True:
            count += 1
            if count % 10000 == 0:
                print count

            line = self.__reader.readline()
            if not line:
                break
            doc = self.__wrap_doc(line)
            if doc is None:
                continue

            self.__stat_feature(doc)

        self.__write()
        self.close()

    def close(self):
        self.__reader.close()
        self.__writer.close()


def train():

    model_path = '/data/recommend/goods-rank/data/model.dat'

    trainer = BayesianTrainer('multinomial', '/data/recommend/goods-rank/data/training_set', model_path)
    trainer.train()

    ranker = BayesRanker(model_path)
    goods = {'product': '短裙,中裙,a字裙,半裙,裙子', 'cat': '207', 'shop': '淘宝'}

    reader = open('/data/recommend/goods-rank/data/training_set', 'r')
    count = -1
    pos_count = 0
    neg_count = 0
    total_words_count = 0
    l = lambda x, y: x['score'] > y['score']
    h = BinHeap(100, l)
    while True:
        count += 1
        line = reader.readline()
        if not line:
            break
        doc = {}
        arr = line.split('\t')

        i = 0
        l = len(arr)
        while i < l:
            key = arr[i]
            i += 1
            value = arr[i]
            i += 1

            if key not in ['product', 'brand', 'cat', 'shop']:
                continue

            doc[key] = value

        s0, s1 = ranker.rank(doc)

        doc['score'] = s0 / s1
        doc['line'] = line
        h.insert(doc)

        if count > 100000:
            break

    print count
    reader.close()

    result_list = h.get_data()

    for s in result_list:
        if s is None:
            continue
        print s['score'], s['line'],

if __name__ == '__main__':
    train()