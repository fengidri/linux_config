# -*- coding:utf-8 -*-


import os
import sys
import random
import subprocess
import email
import time

class TransferMail(object):
    def __init__(self, path, sent = None):
        self.queue_path = path
        self.sent_path = sent

    def append(self, mail):
        filename = os.path.join(self.queue_path, '%s-%s.mail' % (time.time(), random.random()))
        open(filename, 'w').write(mail)
        print("  transfer: save mail to sendq: %s" % email.message_from_string(mail).get('Subject'))

    def hanlder(self):
        for n in os.listdir(self.queue_path):
            f = os.path.join(self.queue_path, n)

            m = open(f).read()

            mail = email.message_from_string(m)

            p = subprocess.Popen(['msmtp', '-t'], stdin = subprocess.PIPE)

            p.communicate()
            if 0 == p.returncode:
                print("sent success. subject: %s" % mail.get('Subject'))
                if self.sent_path:
                    ff = os.path.join(self.sent_path, n)
                    open(ff, 'w').write(m)

                os.remove(f)

            else:
                print("sent fail. subject: %s" % mail.get('Subject'))

