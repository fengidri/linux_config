# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2016-07-18 02:17:17
#    email     :   fengidri@yeah.net
#    version   :   1.0.1


#encoding: utf8



import os
import sys
import argparse

class Git(object):
    def __init__(self):
        self.is_gitdir = False

        self.branch = ''
        self.branch_remote = None

        self.ahead = 0
        self.behind = 0
        self.clear = True

        self._gs()

    def _gs(self):
        cmd = "LANG=en_US git status --porcelain --branch 2>/dev/null"
        lines = os.popen(cmd).readlines()

        if not lines:
            return

        self.is_gitdir = True

        self.clear = len(lines) != 1

        info = lines[0].strip().split(' ', 2)

        br = info[1].split('...')
        self.branch = br[0]
        if len(br) == 2:
            self.branch_remote = br[1]

        if len(info) == 3:
            gs = info[2][1:-1].split()
            if gs[0] == 'behind':
                self.behind = int(gs[1])

            if gs[0] == 'ahead':
                self.ahead = int(gs[1])


def gs(args):

    remote = ' -'
    if git.branch_remote:
        remote = ' '
        if git.ahead:
            remote += '+%s' % git.ahead

        if git.behind:
            remote += '-%s' % git.behind

    clear = ''
    if not git.clear:
        clear = '|X'

    #print ' %s%s[0;31;46m%s%s ' % (branch, chr(27), remote, clean)
    print ' %s%s%s ' % (git.branch, remote, clear)

def gp(args):
    if git.branch_remote:
        cmd = 'git push'
    else:
        cmd = 'git push --set-upstream origin %s' % git.branch
    os.system(cmd)


import argparse

parser = argparse.ArgumentParser(description='git')
subparser = parser.add_subparsers()

arg = subparser.add_parser('gs', help= 'git info')
arg.set_defaults(func = gs)

arg = subparser.add_parser('gp', help= 'git push')
arg.set_defaults(func = gp)



git = Git()
if not git.is_gitdir:
    sys.exit(0)

args = parser.parse_args()
args.func(args)
