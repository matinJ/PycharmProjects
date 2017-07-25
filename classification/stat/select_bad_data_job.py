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

parse_fields = ['name', 'ourl', 'pic', 'timestamp']


class ParseMapper(PyMapper):
    def __init__(self, sys_in):
        PyMapper.__init__(self, sys_in, False)
        self.__fields = parse_fields

    def handle_map(self, key, value):
        if value.find('4235316927296408954') < 0:
            return

        try:
            arr = value.split('PluginCallbackGoodsInfo:')

            # obj = json.loads(value[s:e], 'utf-8')
            obj = json.read(arr[1])

            if 'id' not in obj:
                return

            items = Seq(self.__fields)\
                .map(lambda x: ((x in obj) and (x, str(obj[x]))) or (x, ''))\
                .map(lambda x: x[1].replace('\n', '  '))
            value = '\t'.join(items)

            self.write(str(obj['id']), str(value))

        except Exception, e:
            raise e


class ParseReducer(PyReducer):

    def __init__(self, sys_in):
        PyReducer.__init__(self, sys_in)

    def handle_reduce(self, key, values):

        for value in values:
            self.write(key, value)

if __name__ == '__main__':
    task = sys.argv[1]
    if task == 'map':
        mapper = ParseMapper(sys.stdin)
        mapper.run()
    elif task == 'reduce':
        reducer = ParseReducer(sys.stdin)
        reducer.run()