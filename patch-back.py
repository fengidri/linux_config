# -*- coding:utf-8 -*-


import os
import sys


class g:
    index = 1
    ext_info = None
    patchdir = '__patch__'

def mkpatch(gh):

    print('')
    print(">>> make patch for hash: %s" % gh)
    print('')

    cmd = 'git checkout %s' % gh
    os.system(cmd)

    cmd = "git format-patch -1 --start-number %d -o %s" % (g.index, g.patchdir)
    g.index += 1

    patch = os.popen(cmd).read().strip()

    l_hash = os.popen('git rev-parse HEAD').read().strip()

    lines = open(patch).readlines()

    for i, line in enumerate(lines):
        if line.strip() != '':
            continue

        ins = []
        if g.ext_info:
            ins.append("%s\n" % g.ext_info)
            ins.append("\n")
        ins.append('commit %s upstream.\n' % l_hash)
        ins.append('\n')

        while ins:
            l = ins.pop()
            lines.insert(i + 1, l)

        break

    open(patch, 'w').write(''.join(lines))

def run(githash):
    cmd = 'rm -rf %s' % g.patchdir
    os.system(cmd)

    start_hash = os.popen('git rev-parse HEAD').read().strip()
    for gh in githash:
        mkpatch(gh)

    print('')
    print('>>> [go back to start hash]')
    print('')
    os.system("git checkout %s" % start_hash)

def main():
    githash = []

    while len(sys.argv) >= 2:
        a = sys.argv.pop(1)

        if a == '-e':
            g.ext_info = sys.argv.pop(1)
            continue

        githash.append(a)

    if not githash:
        print "make patch for backport."
        print "patch-back [-e ext info] <githash> [<githash> <githash> ...]"

main()



