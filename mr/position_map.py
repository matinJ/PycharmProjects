#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def read_input(file):
    for line in file:
        yield line.split("\t")


def main(type, separator='\t'):
    data = read_input(sys.stdin)
    for items in data:
        try:
            client_id = items[0]
            enddate = items[1]
            position = items[2]
            _position = enddate + ":"+position
            print '%s%s%s' % (client_id, separator, _position)
        except Exception, e:
            pass


if __name__ == "__main__":
    main(sys.argv[1])