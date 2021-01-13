#!/bin/env python2
# -*- coding:utf-8 -*-


import os
import sys
import argparse
import email

class g:
    patchdir = "./__patch__/"
    cmdpath  = '__patch__/cmd.sh'
    addrpath = '~/.address_list'
    mailpath = '/tmp/mail.link'
    mail = None
    addrlist = []
    newline = ' \\\n    '

def init():
    path = os.path.expanduser(g.addrpath)

    for line in open(path).readlines():
        line = line.strip()
        g.addrlist.append(line)

    if os.path.islink(g.mailpath):
        m = open(g.mailpath).read()
        m = email.message_from_string(m)
        g.mail = m


def header_parse_msgid(h):
    if not h:
        return ''

    h = h.replace('\n', ' ')
    h = h.strip()

    if h[0] == '<':
        p = h.find('>')
        if p == -1:
            return ''

        return h[0:p + 1]


def addrlist():
    for i, a in enumerate(g.addrlist):
        print "%d: %s" % (i, a)

def get_addr(a):
    if a.isdigit():
        return g.addrlist[int(a)]
    return a


def append(es, tp, e):
    e = get_addr(e)

    es.append(g.newline)

    c = "--%s='%s'" % (tp, e)
    es.append(c)

def get_maintainer():
    cmd = './scripts/get_maintainer.pl ./__patch__/*.patch'

    o = []

    cmd += ' 2>/dev/null'

    for line in os.popen(cmd).readlines():
        line = line.split('(')[0]
        line = line.strip()
        o.append(line)

    return o

def mail_option(ms):
    es = []
    for e in ms:
        if e == 'linux-kernel@vger.kernel.org':
            continue

        if e in args.to or e in args.cc:
            continue

        append(es, 'cc', e)

    for t in args.cc:
        append(es, 'cc', t)

    for t in args.to:
        append(es, 'to', t)

    return es

def build_cmd():
    if args.maintainer:
        maintainer = get_maintainer()
    else:
        maintainer = []

    mo = mail_option(maintainer)
    mo = ' '.join(mo)

    cmd ='git send-email __patch__/*.patch --quiet '

    fd = open(g.cmdpath, 'w')

    fd.write(cmd)

    if args.dry:
        fd.write(' --dry-run')

    if not args.maintainer:
        fd.write(' --suppress-cc=all')

    if g.mail:
        if args.R:
            os.remove(g.mailpath)
        else:
            msgid = header_parse_msgid(g.mail.get("Message-id"))
            print ""
            print "====== mail(%s) =======" % g.mailpath
            if not args.reply:
                print "Use as reply by -r/--reply. Delete by -R"
                print ''

            print "    From: %s" % g.mail.get("From")
            print '    Subject: %s' % g.mail.get("Subject").replace('\r', '').replace('\n', '')
            print "    Message-Id: %s" % msgid
            if args.reply:
                fd.write(g.newline)
                fd.write(" --in-reply-to='%s'" % msgid)

    fd.write(mo)
    fd.write('\n')

def dump():
    print ''
    print '====== dump cmd.sh ========='
    print open(g.cmdpath).read()

def main():
    init()
    if args.addr_list:
        addrlist()
        return

    if args.run:
        dump()
        os.system('sh %s' % g.cmdpath)
        return

    print '====== list %s =============' % g.patchdir
    for i in os.listdir(g.patchdir):
        print i

    build_cmd()
    dump()

parser = argparse.ArgumentParser(description="wrap for git send-email")
parser.add_argument('-l', '--addr-list', help="list addr address list. %s" % g.addrpath, action='store_true')
parser.add_argument('-t', '--to', help="add to email. int value for addrlist index.", action='append', default = [])
parser.add_argument('-c', '--cc', help="add cc email. int value for addrlist index.", action='append', default = [])
parser.add_argument('-m', '--maintainer',  help="add maintainer", action='store_true')
parser.add_argument('-r', '--reply',  help="add in-reply-to by %s" % g.mailpath, action='store_true')
parser.add_argument('-R', help="remove %s" % g.mailpath, action='store_true')
parser.add_argument('--dry', help="try. no send", action='store_true')
parser.add_argument('--run', help="run cmd.sh", action='store_true')

args = parser.parse_args()


main()


