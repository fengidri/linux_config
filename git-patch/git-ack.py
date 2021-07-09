#!/bin/env python2
# -*- coding:utf-8 -*-

import os
import sys
import git
import difflib
import termcolor

class g:
    log = "/tmp/git-ack-log"

def change_msg(path):
    acks = os.environ.get("ACKS").split('\n')
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
        o.append(a + '\n')

    open(path, 'w').write(''.join(o))

def sequence_editor(path):
    print path
    h = os.environ.get('ACK-HASH')
    title = os.environ.get('ACK-TITLE')

    lines = open(path).readlines()

    o = []

    for line in lines:
        if not line:
            continue

        if line[0] == '#':
            continue

        if not line.strip():
            continue

        t = line.strip().split(' ', 2)
        print(t)

        if len(t) != 3:
            o.append(line)
            continue

        if not h and not title:
            t[0] = 'reword'
            line = ' '.join(t) + '\n'
            o.append(line)
            continue

        if t[2] == title or (h and h.startswith(t[1])):
            t[0] = 'reword'
            line = ' '.join(t) + '\n'
            o.append(line)
            continue

        o.append(line)

    open(path, 'w').write(''.join(o))

def diff(org_hash, num):
    log1 = git.log(end = org_hash, num = num)
    log2 = git.log(num = num)

    print("")

    for i in range(len(log1)):
        l1 = log1[i]
        l2 = log2[i]

        t1 = l1.title
        t2 = l2.title
        print(termcolor.colored("Title: " + t1, "yellow"))
        if t2 != t1:
            print("+ " + t2)

        sys.stdout.writelines(difflib.unified_diff(l1.msg, l2.msg))
        sys.stdout.flush()
        print('')


def main(args):
    num = args.n
    lines = args.ack
    ghash = git.get_hash()

    os.environ["GIT_SEQUENCE_EDITOR"] = "git-ack -s "
    os.environ["GIT_EDITOR"]          = "git-ack -e "
    os.environ['ACKS']                = '\n'.join(lines)

    if args.title:
        os.environ['ACK-TITLE'] = args.title

    if args.hash:
        os.environ['ACK-HASH'] = args.hash

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
mk.add_argument('-s', help="git edit sequence mode")
mk.add_argument('--hash', help="special git commit hash")
mk.add_argument('--title', help="special git commit title")
mk.add_argument('ack', help="ack", nargs='*')

args = parser.parse_args()

if args.e:
    change_msg(args.e)

elif args.s:
    sequence_editor(args.s)

else:
    if args.ack:
        main(args)

