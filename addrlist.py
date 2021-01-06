#!/bin/env python2
# -*- coding:utf-8 -*-

import sys
import os
import argparse

path ='~/.address_list'

path = os.path.expanduser(path)

addrs = []

for line in open(path).readlines():
    line = line.strip()
    addrs.append(line)

parser = argparse.ArgumentParser(description="email address list")
parser.add_argument('-t', '--to', help="as to addr. default cc", action='append')
parser.add_argument('input', nargs='*')


args = parser.parse_args()


if not args.input and not args.to:
    for i, a in enumerate(addrs):
        print "%d: %s" % (i, a)
else:
    for i, a in enumerate(addrs):
        if args.to:
            for ii in args.to:
                if i == int(ii):
                    print "--to='%s'" % (a,)

        for ii in args.input:
            if i == int(ii):
                print "--cc='%s'" % (a,)


