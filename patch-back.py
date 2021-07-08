#!/bin/env python2
# -*- coding:utf-8 -*-


import os
import sys
import termcolor
import signal


class g:
    index = 1
    head = None
    ext_info = None
    patchdir = '__patch__'
    patch_hash = []

def stdout_write(msg, color = None):
    if color:
        msg = termcolor.colored(msg, color)
    sys.stdout.write(msg)
    sys.stdout.flush()


def find_fix(gh, prefix):
    l_hash = os.popen('git rev-parse %s' % gh).read().strip()
    title = os.popen('git log %s -1 --oneline' % l_hash).read().strip()

    print("%s. Find Fix For: %s" % (prefix, title))

    hsh = l_hash[0:12]

    cmd = 'git log %s..%s --grep %s' % (l_hash, g.head, hsh)
    lines = os.popen(cmd).readlines()

    patchs = []
    patch = []

    for line in lines:
        if line.startswith('commit '):
            if patch:
                patchs.append(patch)
            patch = []

        patch.append(line)

    if patch:
        patchs.append(patch)

    patchs.reverse()

    index = 1

    for patch in patchs:
        l_hash = patch[0].strip().split()[1]
        if l_hash in g.patch_hash:
            continue

        print("")
        print("=" * 80)

        h = True
        for l in patch:
            if h:
                h = False
                l = termcolor.colored(l, "yellow")
            else:
                l = l.replace(hsh, termcolor.colored(hsh, "yellow"))
            stdout_write(l)

        print("=" * 80)

        stdout_write("%s. %s\n" % (prefix, title), "yellow")
        stdout_write("\t%s.%s %s"% (prefix, index, patch[4]), "yellow")
        stdout_write('\nThis may be the fix. Use this? (y/n): ')
        c = raw_input().lower()

        print("")

        if c == 'y':
            g.patch_hash.append(l_hash)
            find_fix(l_hash, "%s.%d" %(prefix, index))
            index += 1

def find_fix_patch(githash):
    for gh in githash:
        l_hash = os.popen('git rev-parse %s' % gh).read().strip()
        g.patch_hash.append(l_hash)

    for i, gh in enumerate(githash):
        find_fix(gh, '%d' % (i + 1))

    print('')

def sort_patch():
    cmdfmt = 'git log --pretty=tformat:"%%H" %s~..%s'

    hs = []

    for gh in g.patch_hash:

        if gh in hs:
            continue

        cmd = cmdfmt % (gh, g.head)
        lines = os.popen(cmd).readlines()
        hs = [x.strip() for x in lines]

    o = []

    hs.reverse()

    for h in hs:
        if h in g.patch_hash:
            o.append(h)
            g.patch_hash.remove(h)

    if g.patch_hash:
        raise Exception("sort patch: left %s" % g.patch_hash)

    g.patch_hash = o


def __mk_patch():
    l_hash = os.popen('git rev-parse HEAD').read().strip()

    cmd = "git format-patch -1 --start-number %d -o %s" % (g.index, g.patchdir)
    g.index += 1

    patch = os.popen(cmd).read().strip()

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

def mkpatch(gh):
    info = os.popen('git log %s -1 --oneline' % gh).read().strip()
    stdout_write("mkpatch: %d. %s\n" % (g.index, info), color = "green")

    cmd = 'git checkout %s 2>/dev/null' % gh
    os.system(cmd)

    l_hash = os.popen('git rev-parse HEAD').read().strip()

    __mk_patch()

def go_back():
    br = g.br

    print('')
    print('>>> [go back to origin branch %s]' % br)
    print('')
    os.system("git checkout %s 2>/dev/null" % br)

def sig_handle(si, s):
    go_back()
    sys.exit(-1)

def run():
    cmd = 'rm -rf %s' % g.patchdir
    os.system(cmd)

    g.br = os.popen('git branch --show-current').read().strip()

    signal.signal(signal.SIGINT, sig_handle)

    for gh in g.patch_hash:
        mkpatch(gh)

    go_back()

    print('')

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
        return

    g.head = os.popen('git rev-parse HEAD').read().strip()

    find_fix_patch(githash)
    sort_patch()
    run()

main()



