#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from collections import Counter

try:
    num_words = int(sys.argv[1])
except:
    print "usage: most_common_words.py num_woeds"
    sys.exit(1)

counter = Counter(word.lower()
                  for line in sys.stdin
                  for word in line.strip().split() #空格划分
                  if word)  #跳过空的'words'
for word, count in counter.most_common(num_words):
    sys.stdout.write(str(count))
    sys.stdout.write("\t")
    sys.stdout.write(word)
    sys.stdout.write("\n")
