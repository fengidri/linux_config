# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-27 10:05:21
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import time
def git_status(length=20):
    branch='master'
    remote=''
    clean=''
    cmd = 'LANG=en_US git status --porcelain --branch 2>/dev/null'
    lines = os.popen(cmd).readlines()
    for line in lines:
        if not line.startswith('##'):
            continue
        t = line.split()
        branch = t[1].split('...')[0]
        if len(branch) > length:
            if branch.startswith('feature/'):
                branch = branch.split('/')[1]
            branch = branch[-1 * length:]

        if len(t) == 4:
            s = t[2][1:]
            n = t[3][0:-1]
            remote = ' -%s'
            if s == 'ahead':
                remote = ' +%s'
            remote = remote % n
        break
    if len(lines) != 1:
        clean = '|X'
    l = len(branch) + len(remote) + len(clean)
    return '%s%s[0;31;46m%s%s ' % (branch, chr(27), remote, clean), l

def path(length):
    p = os.getcwd()
    home = os.getenv("HOME")
    p = p.replace(home, '~')

    if len(p) > length:
        p = p[-1 * (length - 3)]
        p = '...%s' % p
    return p

def prompt():
    s = time.time()

    gitstatus, l =  git_status()

    print gitstatus
    print time.time() - s

if __name__ == "__main__":
    prompt()

