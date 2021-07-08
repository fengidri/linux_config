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

    patch_info = []

def stdout_write(msg, color = None):
    if color:
        msg = termcolor.colored(msg, color)
    sys.stdout.write(msg)
    sys.stdout.flush()


def found_fix():
    l_hash = os.popen('git rev-parse HEAD').read().strip()
    title = os.popen('git log -1 --oneline').read().strip()

    hsh = l_hash[0:12]

    cmd = 'git log HEAD..%s --grep %s' % (g.head, hsh)
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

        print("")
        msg = "This may be the fix for '%s'.\nUse this? (y/n): " % termcolor.colored(title, "yellow")
        stdout_write(msg)
        c = raw_input().lower()

        print("")

        if c == 'y':
            mkpatch(l_hash)

def __mk_patch():
    info = os.popen('git log -1 --oneline').read()
    l_hash = os.popen('git rev-parse HEAD').read().strip()

    stdout_write("   mkpatch: %s\n" % info, color = "green")

    cmd = "git format-patch -1 --start-number %d -o %s" % (g.index, g.patchdir)
    g.index += 1

    patch = os.popen(cmd).read().strip()

    g.patch_hash.append(l_hash)

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

    g.patch_info.append(info)


def mkpatch(gh):
    info = os.popen('git log %s -1 --oneline' % gh).read().strip()
    print(">> goto %s" % info)

    cmd = 'git checkout %s 2>/dev/null' % gh
    os.system(cmd)

    l_hash = os.popen('git rev-parse HEAD').read().strip()
    if l_hash in g.patch_hash:
        print("This patch is done.")
        found_fix()
        return

    __mk_patch()

    found_fix()

def go_back():
    br = g.br

    print('')
    print('>>> [go back to origin branch %s]' % br)
    print('')
    os.system("git checkout %s 2>/dev/null" % br)

def sig_handle(si, s):
    go_back()
    sys.exit(-1)

def run(githash):
    cmd = 'rm -rf %s' % g.patchdir
    os.system(cmd)

    start_hash = os.popen('git rev-parse HEAD').read().strip()
    br = os.popen('git branch --show-current').read().strip()
    g.head = start_hash
    g.br = br

    signal.signal(signal.SIGINT, sig_handle)

    for gh in githash:
        mkpatch(gh)

    go_back()

    print('')

    for i, info in enumerate(g.patch_info):
        msg = "%d. %s" %(i + 1, info[0:-1])
        print(msg)

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



    run(githash)

main()



