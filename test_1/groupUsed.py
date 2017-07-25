#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
【教程】详解Python正则表达式之： (...) group 分组 
"""

import re;

#提示：
#此处所演示的是没有命名的组，unnamed group，关于named group，可以参考：
#【教程】详解Python正则表达式之： (?P<name>…) named group 带命名的组
#http://www.crifan.com/detailed_explanation_about_python_regular_express_named_group/

# 下列举例所用的字符串 http://www.songtaste.com/user/351979/ 中的部分html代码
reGroupTestStr = '<h1 class="h1user">crifan</h1>';
foundH1user = re.search('<h1 class="h1user">(.+?)</h1>', reGroupTestStr);

# 1. Match Objects
# 如果查找到了，则对应返回的值是一个 match对象，打印出来都是 _sre.SRE_Match object之类的
# 其中，Match Objects的详细说明，可参考官网的手册：
#http://docs.python.org/2/library/re.html#match-objects
print "foundH1user=",foundH1user; #foundH1user= <_sre.SRE_Match object at 0x023A7D60>

if(foundH1user):# 2. matched.group(0)
    #  如果有匹配的字符串，则之前通过括号所括起来的group，其中的group(0)，都表示整个所匹配的字符串的值
    wholeMatchString = foundH1user.group(0);
    print "wholeMatchString=",wholeMatchString; #wholeMatchString= <h1 class="h1user">crifan</h1>
    # 3. matched.group(N)
    # 余下的，如果之前有多个括号，即多个group，那么分别对应着group(1),group(2),group(3),...
    # 此处，就一个group，所以对应的group(1)就是我们所要提取出来的值
    h1User = foundH1user.group(1);
    print "Group(1): h1User=",h1User; #Group(1): h1User= crifan
    # 4. matched.groups()
    #Match对象的groups，表示从group(1)开始往后的所有的值，组合成一个Tuple类型的值
    allMatchedGroups = foundH1user.groups();
    print "allMatchedGroups=",allMatchedGroups; #allMatchedGroups= ('crifan',)

    #  5. matched.strat(N) and matched.end(N)
    #也可以获得所匹配的group的起始位置和结束位置
    start1 = foundH1user.start(1);
    end1 = foundH1user.end(1);
    print "Group(1): start position=%d, end postion=%d"%(start1,end1); #Group(1): start position=19, end postion=25

    # 6 matched.string
    #通过MatchObject.sring的方式，获得的值，和之前MatchObject.group(0)，是一样的
    foundString = foundH1user.string;
    print "foundString=",foundString; #foundString= <h1 class="h1user">crifan</h1>    

    #  7. get string by [startN:endN]
    # #对应的，还可以通过 start和end之间，获得所匹配的字符串
    # #和之前通过MatchObject.group(1)获得的值，也是一样的
    strByStartAndEnd = foundString[start1:end1];
    print "Group(1): strByStartAndEnd=",strByStartAndEnd; #Group(1): strByStartAndEnd= crifan

    #  8. 演示如何 前向引用，即匹配前面已经出现的某个group的值
#！！！注意：下面这个写法，是无法工作的，因为\1只是代表了特殊的单个字符'\1'而不是去匹配编号为1的group
#foundPrevMatch = re.search('<(\S+) class="h1user">.+?</\1>', reGroupTestStr);
#下面两种写法才是正确的：
#foundPrevMatch = re.search('<(\S+) class="h1user">.+?</\\1>', reGroupTestStr);
foundPrevMatch = re.search(r'<(\S+) class="h1user">(.+?)</\1>', reGroupTestStr);
print "foundPrevMatch=",foundPrevMatch; #foundPrevMatch= <_sre.SRE_Match object at 0x01F67BA8>
if(foundPrevMatch):
    # 9. 编号为1,2的group，分别就是上面的：
    #(\S+)和(.+?)，所以分别是标签h1和h1user的值
    # 10. 对应的\1就是匹配前面的，第一个group，即(\S+)
    h1 = foundPrevMatch.group(1);
    print "h1=",h1; #h1= h1
#  
    h1User = foundPrevMatch.group(2);
    print "h1User=",h1User; #h1User= crifan