"""
Date    : 15/4/17
Author  : baylor
"""
import math
from base.mapreduce import PyMapper, PyReducer
from common import collections
from common.io.file_io import MultiFileReader, FileReader

__author__ = 'baylor'


class IGPrepareMapper(PyMapper):

    def extract_features(self, line):
        arr = line.split('\t')
        return arr[0], arr[1:]

    def handle_map(self, key, value):
        cat, terms = self.extract_features(value)
        # => term, cat, count
        # => cat, count
        # => term, count
        # for term in terms:
        #     self.write('__term__'+term, '1')
        #     self.write('__termcat__'+term+'##'+cat, '1')

        self.write('__cat__'+cat, '1')
        self.write('__total__count__', '1')


class IGPrepareReducer(PyReducer):

    def handle_reduce(self, key, values):
        count = 0
        for v in values:
            count += int(v)

        self.write(key, count)


class IGEntropyMapper(PyMapper):

    def extract_features(self, line):
        arr = line.split('\t')
        return arr[0], arr[1:]

    def handle_map(self, key, value):
        cat, terms = self.extract_features(value)
        # => term, cat, count
        # => cat, count
        # => term, count
        terms = set(terms)
        for term in terms:
            self.write('__term__'+term, '1')
            self.write('__term__'+term, '__cat__'+cat+'__cat__1')


class IGPrepareCombiner(PyReducer):

    def handle_reduce(self, key, values):
        term_count = 0
        term_cat_dict = {}
        for v in values:
            if v.startswith('__cat__'):
                arr = v.split('__cat__')
                v = arr[2]
                cat = arr[1]
                collections.incre_dict(term_cat_dict, cat, int(v))
            else:
                term_count += int(v)

        self.write(key, term_count)

        for cat, count in term_cat_dict.items():
            self.write(key, '__cat__'+cat+'__cat__'+str(count))


class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IGEntropyReducer(PyReducer):

    def __init__(self, cat_info_path):
        PyReducer.__init__(self)
        self.init_cat_count(cat_info_path)

    __total_count = 0
    __cat_dict = {}
    __h_c_ = 0

    def init_cat_count(self, cat_info_path):
        self.__total_count = 0
        self.__cat_dict = {}

        reader = FileReader(cat_info_path)
        for line in reader:
            arr = line.split('\t')
            v = int(arr[1])
            farr = arr[0].split('__')
            if farr[1] == 'total':
                self.__total_count = v
            if farr[1] == 'cat':
                collections.incre_dict(self.__cat_dict, farr[2], v)
        reader.close()

        self.__total_count *= 1.0
        #  H(C)
        h_c_ = 0
        for cat, count in self.__cat_dict.items():
            p = count / self.__total_count
            h_c_ += p * math.log(p, 2)
        self.__h_c_ = h_c_ * -1

    def handle_reduce(self, term, values):
        term_count = 0
        term_cat_dict = {}
        for v in values:
            if v.startswith('__cat__'):
                arr = v.split('__cat__')
                v = arr[2]
                cat = arr[1]
                collections.incre_dict(term_cat_dict, cat, int(v))
            else:
                term_count += int(v)

        term_count *= 1.0
        # P(t)
        p_t_ = term_count / self.__total_count
        p__t_ = 1 - p_t_

        # H(C|t)
        h_ct_ = 0
        h_c_t_ = 0
        for cat, cat_count in self.__cat_dict.items():
            # P(c|t)
            term_cat_count = term_cat_dict.get(cat, 0)
            p_ct_ = term_cat_count / term_count
            if p_ct_ > 0:
                h_ct_ += p_ct_ * math.log(p_ct_, 2)

            # P(c|_t)
            term_cat_count = cat_count - term_cat_count
            p_c_t_ = term_cat_count / (self.__total_count - term_count)
            if p_c_t_ > 0:
                try:
                    h_c_t_ += p_c_t_ * math.log(p_c_t_, 2)
                except Exception, e:
                    raise MyError('whats wrong with,'+term+', '+cat+',   '+str(term_count)+' , '+str(term_cat_count)+' , '+str(cat_count))

        # H(C|t)
        h_ct_ = (p_t_ * h_ct_ + p__t_ * h_c_t_) * -1
        # ig of t
        ig = self.__h_c_ - h_ct_

        self.write(term, str(ig))


# class IGMapper(PyMapper):
#
#     def handle_map(self, key, value):
#         arr = key.split('__')
#         cat, terms = self.extract_features(value)
#         # => term, cat, count
#         # => cat, count
#         # => term, count
#         for term in terms:
#             self.write('__term__'+term, '1')
#             self.write('__termcat__'+term+'##'+cat, '1')
#
#         self.write('__cat__'+cat, '1')
#         self.write('__total__count__', '1')
#
#
# class IGReducer(PyReducer):
#
#     def handle_reduce(self, key, values):
#         count = 0
#         for v in values:
#             count += int(v)
#
#         self.write(key, count)


class InfoGain(object):
    def __init__(self, input_path):
        self.__cat_dict = {}
        self.__term_dict = {}
        self.__term_cat_dict = {}
        self.__total_count = 0

        self.__term_ig = {}

        self.__load(input_path)

    def __load(self, input_path):
        reader = MultiFileReader(input_path)
        for line in reader:
            arr = line.split('\t')
            term = arr[0]
            ig = float(arr[1])
            self.__term_ig[term] = ig
        reader.close()

    def calc_entropy(self):
        pass

    def get_ig(self, term):
        pass

    def get_ig_list(self):
        return sorted(self.__term_ig.items(), key=lambda x: x[1])