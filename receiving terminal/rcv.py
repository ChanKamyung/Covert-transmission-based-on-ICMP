#!/usr/bin/python3
# _*_ coding=utf-8 _*_

from scapy.all import *
from mLib.icmp_recv import file_recv

def pack_callback(packet):
    global buf, cntr, last, rcv_seqs

    if packet['Raw'].load[8] % 3 == 0  and packet['Raw'].load[9] % 7 == 0 \
       and 0 <= packet['Raw'].load[10] < 16: #预先设计的报文特征

        seq = ((packet['IP'].id & 0x0f00) << 8) + packet['ICMP'].seq
        length = ((packet['IP'].id & 0x0f000) << 4) + packet['ICMP'].id

        if seq not in rcv_seqs:
            rcv_seqs.add(seq)
        
            if seq <= length:
                if len(buf) == 0 and cntr == 0:
                    print('Begin to receive msg! Length is', length)
                    buf = ['0'] * length

                cntr += 1
                
                #print(cntr, ':', seq, '-', length)

                tmp = int(cntr / length * 100)
                if tmp > last:
                    print("已接收：", tmp, '%') #输出接收进度
                    last = tmp
                
                buf[seq - 1] = str(eval(packet['IP'].src[-1]) % 2)

            if seq > length and len(buf) != 0 and cntr != 0:
                tmp = ''.join(buf)
                print('>>Get Message!', file_recv(tmp, packet['Raw'].load[10]))
                print('reveived', cntr, '-', length)
                print('Packet Loss Rate: %.2f%%' % ((1-cntr/length)*100))
                
                buf = []
                rcv_seqs = set()
                cntr = 0
                last = 0

filterstr="icmp" 

buf = [] #记录接收到的二进制数
rcv_seqs = set() #记录接收到的报文编号（防止接收重复报文）
                 #（若收发端都在同一个机子上，同一端口可能会监听到两个一样的报文）
cntr = 0 #记录接收到的报文数
last = 0 #用于接收进度的计算

show_interfaces()
iface_id = input('\n请输入你要监听的网卡对应的编号：')

print('\nI\'m ready..\n')

sniff(filter=filterstr,prn=pack_callback, \
      iface=IFACES.dev_from_index(iface_id), \
      count = 0)
