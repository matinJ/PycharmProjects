# -*- coding: utf-8 -*-
"""
Date    : 15/4/17
Author  : baylor
"""
import os
prj_path = os.path.split(os.path.realpath(__file__))[0]+'/../../'
from common.io import FileReader

__author__ = 'baylor'


class Category(object):
    def __init__(self):
        self.__load(prj_path+'/classification/data/cat_tag')

    def __load(self, path):

        reader = FileReader(path+'/tag_map')
        for line in reader:
            arr = line.split('\t')
            self.__cat_dict[arr[0]] = ['', 3, arr[1]]
            self.__cat_dict[arr[1]] = ['', 2, arr[2]]
            self.__cat_dict[arr[2]] = ['', 1, None]
        reader.close()

        self.__cat_dict['3841'] = ['', 3, None]

        reader = FileReader(path+'/tag_info')
        for line in reader:
            arr = line.split('\t')
            self.__cat_dict[arr[0]][0] = arr[1]

        reader.close()

    __cat_dict = {}

    def __get_cat_field(self, cat_id, index=None):
        if cat_id not in self.__cat_dict:
            return None
        if index is None:
            return self.__cat_dict[cat_id]

        return self.__cat_dict[cat_id][index]

    def get_cat(self, cat_id):
        return self.__get_cat_field(cat_id)

    def get_cat_name(self, cat_id):
        return self.__get_cat_field(cat_id, 0)

    def get_cat_level(self, cat_id):
        return self.__get_cat_field(cat_id, 1)

    def get_cat_parent(self, cat_id):
        return self.__get_cat_field(cat_id, 2)