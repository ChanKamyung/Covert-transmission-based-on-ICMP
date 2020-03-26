#!/usr/bin/python3
# _*_ coding=utf-8 _*_

from scapy.all import *
from mLib.icmp_recv import file_recv

def pack_callback(packet):
    global buf, cntr

    if packet['Raw'].load[8] % 3 == 0  and packet['Raw'].load[9] % 7 == 0 \
       and 0 <= packet['Raw'].load[10] < 16: #预先设计的报文特征

        seq = ((packet['IP'].id & 0x0f00) << 8) + packet['ICMP'].seq
        length = ((packet['IP'].id & 0x0f000) << 4) + packet['ICMP'].id

        if seq <= length:
            if len(buf) == 0 and cntr == 0:
                print('Begin to receive msg! Length is', length)
                buf = ['0'] * length
            cntr += 1
            print(cntr, ':', seq, '-', length)
            buf[seq - 1] = str(eval(packet['IP'].src[-1]) % 2)

        if seq >= length and len(buf) != 0 and cntr != 0:
            tmp = ''.join(buf)
            print('>>Get Message!', file_recv(tmp, packet['Raw'].load[10]))
            print('reveived', cntr, '-', length)
            print('Packet Loss Rate: %.2f%%' % ((1-cntr/length)*100))
            buf = []
            cntr = 0

filterstr="icmp" 

buf = []
cntr = 0

show_interfaces()
iface_id = input('\n请输入你网卡对应的编号：')

print('\nI\'m ready..')

sniff(filter=filterstr,prn=pack_callback, \
      iface=IFACES.dev_from_index(iface_id), \
      count = 0)
