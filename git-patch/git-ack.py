#!/bin/env python2
# -*- coding:utf-8 -*-

import os
import git

class g:
    path = "/tmp/git-ack-tmp"
    log = "/tmp/git-ack-log"

def change_msg(path):
    acks = open(g.path).readlines()
    lines = open(path).readlines()

    o = []

    for line in lines:
        if not line:
            continue

        if line[0] == '#':
            continue

        o.append(line)

    while True:
        if o[-1].strip() == '':
            del o[-1]

        break

    for a in acks:
        o.append(a)

    open(path, 'w').write(''.join(o))

def diff(org_hash, num):
    ghash = git.get_hash()

    print("")
    print("diff: ")

    cmd1 = "git log %s -%d > /tmp/git-ack.diff1" % (org_hash, num)
    cmd2 = "git log %s -%d > /tmp/git-ack.diff2" % (ghash, num)

    os.system(cmd1)
    os.system(cmd2)
    os.system("diff /tmp/git-ack.diff1 /tmp/git-ack.diff2 -U 1| grep 'commit ' -v ")

def main(num, lines):
    ghash = git.get_hash()

    f = open(g.path, 'w')
    f.write('\n'.join(lines) + '\n')
    f.close()

    os.environ["GIT_SEQUENCE_EDITOR"] = "sed -e 's/^pick /reword /' -i"
    os.environ["GIT_EDITOR"] = "git-ack -e "
    cmd = "git rebase -i HEAD~%d > %s 2>&1" % (num, g.log)
    print("git rebase")
    os.system(cmd)

    diff(ghash, num)

    print("")
    print("Try this to recover: git reset %s" % ghash)
    print("more info: %s" % g.log)


import argparse
parser = argparse.ArgumentParser(description="git append ack to commit message")

mk = parser
mk.add_argument('-n', help="commit num. default 1", default = 1, type=int)
mk.add_argument('-e', help="git edit message mode")
mk.add_argument('ack', help="ack", nargs='*')

args = parser.parse_args()


if args.e:
    change_msg(args.e)

else:
    if args.ack:
        main(args.n, args.ack)
