# -*- coding: UTF-8 -*-
import re

pos=0
def test():
    a='_Callback({a:2})'
    p1='_Callback\((.+)\)'
    c=re.compile(p1)
    b=re.search(c,a)
    print b.group(1)
    #print b.group(1)

if __name__ == '__main__':
    test()