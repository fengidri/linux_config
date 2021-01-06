#!/bin/env python2
# -*- coding:utf-8 -*-


if __name__ == "__main__":
    pass


import os
import sys
cmd = './scripts/get_maintainer.pl '

if len(sys.argv) > 1:
    cmd += ' '.join(sys.argv[1:])
else:
    cmd += "./__patch__/*"

o = []

cmd += ' 2>/dev/null'

for line in os.popen(cmd).readlines():
    line = line.split('(')[0]
    line = line.strip()
    o.append(line)

es = []
for e in o:
    if e == 'linux-kernel@vger.kernel.org':
        continue
    c = "--cc='%s'" % e
    es.append(c)

print(' '.join(es))

