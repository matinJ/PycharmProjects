"""
Date    : 15/4/13
Author  : baylor
"""
import os
from classification.goods_classifier import util
from common.base.strings import Strings
from common.io import FileReader

__author__ = 'baylor'


class RuleBaseClassifier(object):
    __rules = {}
    __tb_cid_dict = {}
    __url_suf = set()

    def __init__(self, rule_path=os.path.split(os.path.realpath(__file__))[0]+'/../data/rules/'):
        self.__load_rules(rule_path+'/tag-corres')
        self.__load_tb_cid_map(rule_path+'/taobao_cat_map')

    def __get_domain(self, url):
        if Strings.is_empty(url):
            return None
        return util.get_domain_f_url(url)

    def __load_rules(self, file_path):
        reader = open(file_path, 'r')
        while True:
            line = reader.readline()
            if not line:
                break
            line = line.rstrip('\r\n')
            arr = line.split('\t')
            url = arr[0]
            tag = arr[1]

            label_arr = arr[3].split('|')
            label = set()
            for l in label_arr:
                l = Strings.parse(l)
                label.add(l)

            domain = self.__get_domain(url)
            if domain is None:
                continue

            rule = Strings.parse(domain + tag)
            if self.__rules.has_key(rule):
                self.__rules[rule].update(label)
            else:
                self.__rules[rule] = label
        reader.close()

    def __load_tb_cid_map(self, tb_cid_input):
        reader = FileReader(tb_cid_input)
        for line in reader:
            if line.startswith('#'):
                continue
            arr = line.split('\t')
            if len(arr) < 2:
                continue
            tb_cid = arr[0]
            cat3 = arr[1]

            if len(cat3) == 0:
                continue

            self.__tb_cid_dict[tb_cid] = cat3
        reader.close()

    def classify(self, url, tb_cid=None, tag=None):
        domain = self.__get_domain(url)
        if domain is None:
            return None

        if tb_cid is not None and domain == 'taobao':
            if tb_cid in self.__tb_cid_dict:
                return self.__tb_cid_dict[tb_cid]
            # print 'taobao\t' + tb_cid

        if tag is not None:
            rule = domain + tag
            if rule in self.__rules:
                return self.__rules[rule]

        return None