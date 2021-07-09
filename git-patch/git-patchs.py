#!/bin/env python2
# -*- coding:utf-8 -*-


import argparse
import os
import termcolor

class g:
    patchdir = "__patch__/"
    cover_name = '0000-cover-letter.patch'

    cover_path = os.path.join(patchdir, cover_name)

def check():
    path = '~/.git-mail-check'
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        return

    lines = open(path).readlines()
    e = lines[0].strip()

    remote = 'git remote -v'
    o = os.popen(remote).read()
    if o.find(e) == -1:
        return

    print ''

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        print termcolor.colored(line, 'red')


def main(args):
    cmd = 'rm -rf %s' % g.patchdir
    os.system(cmd)

    if args.num == 1:
        cmd = 'git format-patch --subject-prefix="%s" -1 -o %s' % (args.prefix, g.patchdir)
    else:
        cmd = 'git format-patch --cover-letter --subject-prefix="%s" -%d -o %s' % (args.prefix, args.num, g.patchdir)

    print "## make  patch"
    os.system(cmd)

    print ''
    print "## checkpatch.pl"

    ps = os.listdir(g.patchdir)
    ps.sort()

    for p in ps:
        if p == g.cover_name:
            continue

        p = os.path.join(g.patchdir, p)
        print termcolor.colored(p, 'green')
        cmd = './scripts/checkpatch.pl --color=always %s' % p
        lines = os.popen(cmd).readlines()
        for l in lines:
            if l.startswith(p):
                continue

            if l.startswith('total: '):
                break

            print '   ', l,
    print ''


parser = argparse.ArgumentParser(description="""
    wrap for git format-patch.


"""
, formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument('-p', '--prefix', help="patch title prefix")
parser.add_argument('-n', '--num', help="patch num", type=int, default = 1)
args = parser.parse_args()

main(args)

print termcolor.colored("Add change log inside patch or cover letter", 'blue')

check()
