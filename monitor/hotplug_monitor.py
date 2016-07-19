#!/bin/env python2
# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-07-12 14:01:14
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import time
import re
import sys


class Monitor(object):
    STATUS_DISCON = 1
    STATUS_REMAIN = 4
    STATUS_PRIMARY = 2
    STATUS_CONNECT = 5
    STATUS_TOSHOW = 6

    def __init__(self, info):
        info = info.strip()

        self.name = info.split()[0]

        self.primary = False
        self.connect = False
        self.display = False

        if info.find('primary') > -1:
            self.primary = True
            self.connect = True
            self.display = True

        elif info.find(' connected ') > -1:
            self.connect = True

        if re.search(' \d+x\d+\+\d+\+\d+ ', info):
            self.display = True

    def output(self, primary):
        cmd = 'DISPLAY=:0 xrandr --output %s --auto --above %s' % (self.name, primary.name)
        print "connect to %s" % self.name
        print cmd
        os.system(cmd)

    def discon(self):
        cmd = 'DISPLAY=:0 xrandr --output %s --off' % (self.name, )
        print "discon to %s" % self.name
        print cmd
        os.system(cmd)

    def apply(self, primary):
        print self.name, self.connect, self.display
        if self.name.startswith('VIRTUAL'):
            return

        if self.connect and not self.display:
            self.output(primary)

        if not self.connect and self.display:
            self.discon()



def get_monitors():
    ms = []
    lines = os.popen('DISPLAY=:0 xrandr').readlines()
    for line in lines:
        if line.startswith('Screen'):
            continue

        if line[0] == ' ':
            continue

        m = Monitor(line)
        ms.append(m)

    return ms


def main():

    primary = None
    ms = get_monitors()
    for m  in ms:
        if m.primary:
            primary = m

    for m in ms:
        m.apply(primary)

sys.stderr = sys.stdout = open('/tmp/m.log', 'a')

print "start .."
main()
