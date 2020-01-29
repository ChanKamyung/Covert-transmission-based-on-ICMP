#!/usr/bin/python3
# _*_ coding=utf-8 _*_

#导入相应的包
from scapy.all import *
from random import randint, choice
import time

def get_data(redun):
    t = hex(int(time.time()))[2:]

    #时间戳
    data = ''
    for i in range(4, 0, -1):
        tmp = '0x' + t[(i - 1)*2:i*2]
        data += chr(eval(tmp))
    data += '\x00'*4

    #构造data
    data += chr(randint(0, 85) * 3)+chr(randint(0, 36) * 7) + chr(redun)
    for i in range(5):
        data += '\x00'
    for i in range(0x10, 0x38):
        data += chr(i)
    data = data.encode('raw_unicode_escape')

    return data


def send_msg(host, bit, seq, length, redun):
    ip = IP()
    ip.dst = host
    ip.src = randint(1448498774, 1701143909)*2 + eval(bit) #判断‘0’、‘1’
    ip.id = (((length & 0x0f0000) >> 4) \
             + ((seq & 0x0f0000) >> 8)) \
             + randint(0, 0xff)

    icmp = ICMP()
    icmp.id = length & 0x0ffff
    icmp.seq = seq & 0x0ffff
    icmp.type = 0

    data = get_data(redun)

    packet=ip/icmp/data

    send(packet, verbose=False)


if __name__ == '__main__':
    msg = '10101001'
    for i in range(len(msg)):
        send_msg('192.168.1.11', msg[i], i + 1, len(msg), 0)
