# -*- coding:utf-8 -*-

import json
import os
import sys

import imaplib
import email
import time
import subprocess


class config:
    confd = os.path.expanduser("~/.syncmail")
    server   = None
    port     = None
    user     = None
    password = None
    folders  = None
    deliver  = None
    procmail = os.path.join(config.confd, 'procmail.py')

def conf():
    path = os.path.expanduser("~/.syncmailrc")
    c = open(path).read()
    j = json.loads(c)

    config.server   = j['server']
    config.port     = j['port']
    config.user     = j['user']
    config.password = j['password']
    config.folders = j['folders']
    config.deliver = os.path.expanduser(j['deliver'])

def sync(conn, fold, last, callback):
    typ, [data] = conn.select('"%s"' % fold)
    if typ != 'OK':
        print("select to folder: %s. fail" % fold)
        sys.exit(-1)

    print("folder [%s]:\t %s %s" % (fold, data, typ))

    config.current_total = data

    typ, [data] = conn.uid('search', None, 'ALL')
    ids = data.split()

    for i in ids:
        i = int(i)

        if i <= last:
            continue

        resp, data = conn.uid('fetch', "%d" % i, '(RFC822)')
        callback(data)

def get_last_uid():
    fold = config.current_fold
    if not os.path.isdir(config.confd):
        return -1

    t = os.path.join(config.confd, config.user)
    if not os.path.isdir(t):
        return -1

    t = os.path.join(t, fold)
    if not os.path.isdir(t):
        return -1

    t = os.path.join(t, 'uid')
    if not os.path.isfile(t):
        return -1

    uid = open(t).read()
    return int(uid)


def save_uid(uid):
    fold = config.current_fold
    if not os.path.isdir(config.confd):
        os.mkdir(config.confd)

    t = os.path.join(config.confd, config.user)
    if not os.path.isdir(t):
        os.mkdir(t)

    t = os.path.join(t, fold)
    if not os.path.isdir(t):
        os.mkdir(t)

    t = os.path.join(t, 'uid')
    open(t, 'w').write(uid)


def save_mail(dirname, mail, uid):
    path = os.path.join(config.deliver, dirname)
    new = os.path.join(path, 'new')
    if not os.path.isdir(path):
        os.mkdir(path)
        t = os.path.join(path, 'tmp')
        os.mkdir(t)
        t = os.path.join(path, 'cur')
        os.mkdir(t)
        os.mkdir(new)

    filename = "%s-%s.eu6sqa" % (time.time(), uid)

    path = os.path.join(new, filename)

    open(path, 'w').write(mail)
    save_uid(uid)

    print("save email %s:%s/%s to %s" % (config.current_fold, uid,
        config.current_total, dirname))


def procmail(mail):
    cmd = ['python2', config.procmail]

    p = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate(mail)

    o = []
    for l in stdout.split('\n'):
        l = l.strip()
        if not l:
            continue

        o.append(l)

    return o


def procmails(maillist):
    for mail in maillist:
        if mail == ')':
            continue

        uid = mail[0].split()[2]
        mail = mail[1]

        ds = procmail(mail)
        for d in ds:
            save_mail(d, mail, uid)



def main():
    conf()

    conn = imaplib.IMAP4_SSL(host = config.server, port = config.port)

    typ, [data] = conn.login(config.user, config.password)
    if typ != 'OK':
        print("login fail" % fold)
        return

    for fold in config.folders:
        config.current_fold = fold

        last = get_last_uid()

        sync(conn, fold, last, procmails)


main()

