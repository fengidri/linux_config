#!/bin/env python2
# -*- coding:utf-8 -*-


import os
import sys
import argparse
import email
import termcolor

class g:
    patchdir = "./__patch__/"
    cmdpath  = '__patch__/cmd.sh'
    addrpath = '~/.address_list'
    mailpath = '/tmp/mail.link'
    patch    = '__patch__/*.patch'
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
    cmd = './scripts/get_maintainer.pl %s' % g.patch

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

    cmd ='git send-email --quiet '

    fd = open(g.cmdpath, 'w')

    fd.write(cmd)

    fd.write(g.newline)
    fd.write(' %s' % g.patch)

    if args.dry:
        fd.write(g.newline)
        fd.write(' --dry-run')

    if not args.maintainer:
        fd.write(g.newline)
        fd.write(' --suppress-cc=all')

    if g.mail:
        if args.R:
            os.remove(g.mailpath)
        else:
            msgid = header_parse_msgid(g.mail.get("Message-id"))
            print ""
            print termcolor.colored("====== mail(%s) =======" % g.mailpath, 'green')
            if not args.reply:
                print termcolor.colored("  Use as reply by -r/--reply. Delete by -R", 'blue')
                print ''

            key = 'Date'
            print "    %s: %s" % (termcolor.colored(key, 'yellow'), g.mail.get(key))
            key = 'From'
            print "    %s: %s" % (termcolor.colored(key, 'yellow'), g.mail.get(key))
            key = 'Subject'
            print '    %s: %s' % (termcolor.colored(key, 'yellow'), g.mail.get("Subject").replace('\r', '').replace('\n', ''))
            key = 'Message-Id'
            print "    %s: %s" % (termcolor.colored(key, 'yellow'), msgid)

            if args.reply:
                fd.write(g.newline)
                fd.write(" --in-reply-to='%s'" % msgid)

                if not args.no_reply_addr:
                    for e in g.mail.get('Cc').split(','):
                        fd.write(g.newline)
                        fd.write(" --cc='%s'" % e.strip())

                    fd.write(g.newline)
                    fd.write(" --to='%s'" % g.mail.get('From'))

    fd.write(mo)
    fd.write('\n')

def dump():
    print ''
    print termcolor.colored('====== dump cmd.sh =========', 'green')
    print open(g.cmdpath).read()

def check():
    path = '~/.git-mail-check'
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        return
    m = open(path).read().strip()
    if open(g.cmdpath).read().find(m) > -1:
        print termcolor.colored(' Do not forget the checklist!!!', 'red')

def main():
    init()

    if args.patch:
        g.patch = args.patch

    if args.addr_list:
        addrlist()
        return

    if args.run:
        dump()
        os.system('sh %s' % g.cmdpath)
        return

    print termcolor.colored('====== list %s =============' % g.patchdir, 'green')
    for i in os.listdir(g.patchdir):
        print i

    build_cmd()
    dump()
    check()

parser = argparse.ArgumentParser(description="""
    wrap for git send-email.

    Example:
        git-email -m -t <to@email>
        git-email -t 0 -c 1 -c 2
        git-email --run

        # reply. link mail to /tmp/mail.link firstly.
        git-email -m -t <to@email> -r
        git-email -t 0 -c 1 -c 2   -r

"""
, formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument('-l', '--addr-list', help="list addr address list. %s" % g.addrpath, action='store_true')
parser.add_argument('-t', '--to', help="add to email. int value for addrlist index.", action='append', default = [])
parser.add_argument('-c', '--cc', help="add cc email. int value for addrlist index.", action='append', default = [])
parser.add_argument('-m', '--maintainer',  help="add maintainer", action='store_true')
parser.add_argument('-r', '--reply',  help="add in-reply-to by %s" % g.mailpath, action='store_true')
parser.add_argument('--no-reply-addr',  help="not use the addr from reply", action='store_true')
parser.add_argument('-R', help="remove %s" % g.mailpath, action='store_true')
parser.add_argument('--dry', help="try. no send", action='store_true')
parser.add_argument('--run', help="run cmd.sh", action='store_true')
parser.add_argument('-p', '--patch', help="special patch")

args = parser.parse_args()


main()


