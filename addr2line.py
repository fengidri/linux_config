#!/bin/python2.7
# -*- coding:utf-8 -*-


if __name__ == "__main__":
    pass

import sys
import os

if len(sys.argv) != 3:
    print "addr2line.py binary fun+offset"
    sys.exit()

addr = sys.argv[2]
binary = sys.argv[1]

fun, offset = addr.split('+')


cmd = 'nm %s' %  binary

lines = os.popen(cmd).readlines()
for line in lines:
    t = line.strip().split()
    fun_addr = t[0]
    f = t[-1]
    if f != fun:
        continue
    break

else:
    sys.exit()

addr = int(fun_addr, 16) + int(offset, 16)
cmd = 'addr2line -e %s 0x%x' % (binary, addr)
os.system(cmd)




