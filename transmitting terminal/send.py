#!/usr/bin/python3
# _*_ coding=utf-8 _*_

from mLib.Huffman import encodefile
from mLib.midst import read2bits
from mLib.bch import init, enbch
from mLib.icmp import send_msg

import random
import time

def file_send(infile, host, err_rate):
    print('丢包率', err_rate)

    stamp = '-'.join([str(i) for i in time.gmtime(time.time())[:6]])
    sinfile = stamp + '_*C4CHE*_' + infile
    
    encodefile(sinfile) #压缩编码
    read2bits(stamp + infile.replace(infile[infile.index('.'):],'.hfm'))#中间过渡
    
    #以下，进行纠错编码，同时发送数据
    print("传输开始...")
    
    n = 15
    t = 3

    mInit = init(n, t, True)
    n, k, t = mInit[0]
    
    buf = ''
    with open(stamp + infile.replace(infile[infile.index('.'):],'.mid'), 'r') \
         as f:
       buf = f.read()

    redun = 0
    length = int(len(buf)/k)*n
    if len(buf) % k != 0:
        length += n
        redun += k - len(buf)%k
    seq = 0
    print('>>报文总数', length)
      
    last = 0
    for i in range(int(len(buf)/k)):
        msg = buf[i*k : (i+1)*k]
        value = enbch(msg, mInit)
        for j in value:
            seq += 1
            if random.random() >= err_rate:
                send_msg(host, j, seq, length, redun)

        tmp = int(i * k / len(buf) * 100)
        if tmp > last:
            print("已传输:", tmp, '%') #输出压缩进度
            last = tmp

    if len(buf) % k != 0:
        msg = buf[(i+1)*k : ]
        msg += '0'*(k - len(buf)%k)
        value = enbch(msg, mInit)
        for j in value:
            seq += 1
            if random.random() >= err_rate:
                send_msg(host, j, seq, length, redun)
                
    for i in range(3): #冗余
        seq = length + 1
        if random.random() >= err_rate:
            send_msg(host, j, seq, length, redun)

    print("传输成功.")

if __name__ == '__main__':
    START = time.perf_counter()

    while True:
        file_send(input('待传输的文件名：'), \
                  input('传输对象的ip：'), \
                  eval(input('丢包率(0~1)：')))
        
        END = time.perf_counter()
        print('总用时 %d 秒.\n' % int(END - START))
