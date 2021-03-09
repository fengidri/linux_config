#!/bin/env python2
# -*- coding:utf-8 -*-

import argparse
import os
import sys
import random

def handle_ssh():
    path = 'qemu-tap-0-mac.conf'
    mac = open(path).read().strip()

    arps = os.popen('arp -n').readlines()
    for line in arps:
        t = line.split()
        if t[2] == mac:
            ip = t[0]
            break

    cmd = 'ssh root@%s' % ip
    print cmd
    print "================"
    os.system(cmd)



class Tap(object):
    def __init__(self, taps):
        self.confs = []

        if len(taps) == 1 and taps[0].isdigit():
            n = int(taps[0])

            taps = self.get_free_tap()
            taps.sort(reverse=True)
            for i in range(n):
                if taps:
                    tap = taps.pop()
                else:
                    tap = self.create_tap()

                self.net_tap(i, tap)
        else:
            for i, t in enumerate(args.tap):
                self.net_tap(t)

    def get_free_tap(self):
        cmd = 'ip -details tuntap'
        lines = os.popen(cmd).readlines()

        o = []
        dev = None

        for line in lines:
            if line[0] != '\t':
                dev = line.split(':')[0]
            else:
                if line.split(':')[-1].strip() == '':
                    o.append(dev)
                    dev = None
        return o

    def get_all_tap(self):
        o = []
        cmd = 'ip tuntap'
        lines = os.popen(cmd).readlines()
        for line in lines:
            dev = line.split(':')[0]
            o.append(dev)

        return o

    def create_tap(self):
        taps = self.get_all_tap()
        index = len(taps)

        while True:
            tap = 'tap%d' % index
            if tap not in taps:
                break
            index += 1
        cmd = 'sudo ip tuntap add %s mode tap multi_queue' % tap
        os.system(cmd)
        cmd = 'sudo ip link set %s up' % tap
        os.system(cmd)
        cmd = 'sudo brctl addif virbr0 %s' % tap
        os.system(cmd)

        return tap


    def net_tap(self, index, tap):
        # static mac for static ip

        path = 'qemu-tap-%d-mac.conf' % index
        if os.path.exists(path):
            mac = open(path).read().strip()
        else:
            mac = '52:55:00:d1:%x:%x' % (random.randrange(0xff), random.randrange(0xff))
            open(path, 'w').write(mac)

        c = "-netdev tap,ifname=%s,id=%s,script=no,downscript=no,queues=4"
        self.confs.append(c % (tap, tap))

        c = "-device virtio-net-pci,netdev=%s,mac=%s,vectors=10,mq=on"
        self.confs.append(c % (tap, mac))

def net_vfio(vfname):
    dev,vf = vfname.split('.')
    path = '/sys/class/net/%s/device/virtfn%s' %(dev, vf)
    bus = os.path.basename(os.path.realpath(path))

    path_drv= path + '/driver'

    drv = os.path.basename(os.path.realpath(path_drv))
    if drv != 'vfio-pci':
        k = os.popen('lspci -ns %s' % bus).read().strip().split()[-1].split(':')

        print("dev %s need bind to vfio-pci" % vfname)
        print "    echo %s > %s/unbind" % (bus, path_drv)
        print "    echo %s %s > /sys/bus/pci/drivers/vfio-pci/new_id" % (k[0], k[1])

        sys.exit(-1)

    return "-device vfio-pci,host=%s" % bus[5:]

def hda_get(args):
    if args.hda:
        return args.hda

    hda = None

    fs = os.listdir('.')
    for f in fs:
        if f[0] == '.':
            continue

        if f.endswith('.qcow2'):
            if hda:
                print("multi qcow2 file")
                sys.exit()

            hda = f

    print("use %s as hda file." % hda)
    return hda



OPT_BASE    = '-nographic --no-reboot'
OPT_MACHINE = '-machine pc-i440fx-2.1,accel=kvm,usb=off'
OPT_CPUMEM  = '-cpu host -m 16384 -smp 8,sockets=1,cores=8,threads=1'
OPT_DISK    = "-drive file=%s,if=virtio"

#############################################################

def command(args):
    command = ['qemu-system-x86_64']
    command.append(OPT_BASE)
    command.append(OPT_MACHINE)
    command.append(OPT_CPUMEM)
    command.append(OPT_DISK % hda_get(args))

    ################  net  ######################################
    OPT_NET = []

    tap = Tap(args.tap)
    OPT_NET.extend(tap.confs)

    for v in args.vf:
        OPT_NET.append(net_vfio(v))

    command.extend(OPT_NET)

    #############################################################

    if args.kernel:
        command.append('-kernel %s/arch/x86_64/boot/bzImage' % args.kernel)

        ap =  "-append 'root=/dev/vda1 console=tty console=ttyS0 net.ifnames=0 biosdevname=0 nokaslr mitigations=on virtio_net.napi_tx=1'"

        command.append(ap)


    cmd = ' \\\n    '.join(command)
    print cmd
    return cmd


parser = argparse.ArgumentParser()
parser.add_argument("-k", '--kernel', help="kernel")
parser.add_argument('--stop', help="stop before run qemu. wait for recv", action='store_true')
parser.add_argument('--hda', help="kernel")
parser.add_argument('--tap', help="special tap name or tap num. auto create tap dev. default 1", action='append', default=['1'])
parser.add_argument('--vf', help="special vf. like --vf eth1.0", action='append', default=[])
parser.add_argument("-s", '--ssh', help="ssh to machine", action='store_true')

args = parser.parse_args()

if args.ssh:
    handle_ssh()
    sys.exit(0)

cmd = command(args)
print '================================='
if args.stop:
    raw_input('wait for input. \\n end:')

os.system(cmd)

