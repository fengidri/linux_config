# -*- coding:utf-8 -*-
import os
import time

import subprocess

class LogItem(object):
    def __init__(self, lines):
        self.hash   = lines[0].split()[-1].strip()
        self.author = lines[1].split(' ', 1)[-1].strip()
        self.date   = lines[2].split(' ', 1)[-1].strip()
        self.title  = lines[4].strip()
        self.msg    = lines[5:]

def log(end = 'HEAD', num = 1, start = None, grep = None):

    if start:
        cmd = "git log %s..%s" % (start, end)
    else:
        cmd = "git log %s -%d" % (end, num)

    if grep:
        cmd = cmd + " --grep '%s'" % grep

    lines = os.popen(cmd).readlines()

    patchs = []
    patch = []

    for line in lines:
        if line.startswith('commit '):
            if patch:
                patchs.append(LogItem(patch))
            patch = []

        patch.append(line)

    if patch:
        patchs.append(LogItem(patch))

    patchs.reverse()

    return patchs

def get_hash(gh = 'HEAD'):
    return os.popen('git rev-parse %s' % gh).read().strip()

def commit_amend(msg, log='/dev/null'):
    if msg:
        f = '/tmp/tmp-kernel-patch-%s-%s'  % (time.time(), os.getpid())
        open(f, 'w').write(msg)

        cmd = 'git commit --amend -F %s >> %s'% (f, log)
        os.system(cmd)
    else:
        cmd='git commit --amend >>' + log
        os.system(cmd)

def get_commit_hash(num):
    cmd='git log --pretty=format:%H -' + str(num)
    lines = os.popen(cmd).readlines()
    o = []
    for line in lines:
        o.append(line.strip())
    return o

def hashs(num):
    cmd='git log --pretty=format:%H -' + str(num)
    lines = os.popen(cmd).readlines()
    o = []
    for line in lines:
        o.append(line.strip())
    return o

def get_commit_body(chash):
    return os.popen('git log --pretty=format:%B -1 ' + chash).read()
