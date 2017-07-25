#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import sys


def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)


def main(separator='\t'):
    current_client = None
    current_value = None
    client = None
    data = read_mapper_output(sys.stdin, separator=separator)
    for client, useValue in data:
        try:
            if current_client == client:
                current_value = current_value + ","+ useValue
            else:
                if current_client:
                    print "%s\t%s" % (current_client, current_value)
                current_value = useValue
                current_client = client
        except Exception, e:
            pass
    if client ==current_client:
        print "%s\t%s" % (current_client, current_value)

if __name__ == "__main__":
    main()
