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
from common.json import ReadException

from base.mapreduce import PyMapper, PyReducer

parse_fields = ['timestamp']


class ParseMapper(PyMapper):
    def __init__(self, sys_in):
        PyMapper.__init__(self, sys_in, False)
        self.__fields = parse_fields

    def handle_map(self, key, value):

        try:
            # arr = value.split('PluginCallbackGoodsInfo:')

            # obj = json.loads(value[s:e], 'utf-8')
            # obj = json.read(arr[1])

            arr = value.split('&')
            guid = None
            timestamp = None
            for v in arr:
                if v.find('guid') >= 0:
                    guid = v.split('=')[1]

                if v.find('timestamp') >= 0:
                    timestamp = v.split('=')[1]

            if guid is None or timestamp is None:
                return
            self.write(str(guid), str(timestamp))

        except ReadException, e:
            pass


class ParseReducer(PyReducer):

    def __init__(self, sys_in):
        PyReducer.__init__(self, sys_in)

    hour_time = 60*60*1000

    def handle_reduce(self, key, values):
        max_time = None
        min_time = None

        first_goods_time = None
        last_goods_time = None

        values = sorted(values)

        for value in values:
            try:
                v_time = long(value)
            except Exception, e:
                pass

            if last_goods_time is None:
                last_goods_time = v_time
                first_goods_time = v_time
                continue

            if v_time - last_goods_time > self.hour_time:
                self.write(key, str(last_goods_time - first_goods_time))

                first_goods_time = None
                last_goods_time = None

                continue

            last_goods_time = v_time

        if last_goods_time is not None and first_goods_time is not None:
            self.write(key, str(last_goods_time - first_goods_time))
        # else:
        #     self.write(key, str(0))


class StatMapper(PyMapper):
    def __init__(self, sys_in):
        PyMapper.__init__(self, sys_in, False)

    def handle_map(self, key, value):
        last_time = value.split('\t')[1]
        self.write('time', '1'+' '+last_time)


class StatReducer(PyReducer):

    def __init__(self, sys_in):
        PyReducer.__init__(self, sys_in)

    def handle_reduce(self, key, values):
        total_time = 0
        total_user = 0
        for value in values:
            arr = value.split(' ')
            total_time += long(arr[1])
            total_user += long(arr[0])

        self.write('time', str(total_user) + ' ' + str(total_time))


if __name__ == '__main__':
    task = sys.argv[1]
    if task == 'map':
        mapper = ParseMapper(sys.stdin)
        mapper.run()
    elif task == 'reduce':
        reducer = ParseReducer(sys.stdin)
        reducer.run()
    elif task == 'stat_map':
        mapper = StatMapper(sys.stdin)
        mapper.run()
    elif task == 'stat_reduce':
        reducer = StatReducer(sys.stdin)
        reducer.run()