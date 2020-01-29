#!/usr/bin/python3
# _*_ coding=utf-8 _*_

from mLib.Huffman import decodefile
from mLib.midst import write4bits
from mLib.bch import init, debch

import time

def file_recv(buf, redun):
    #以下，进行纠错译码
    print("Starting BCH decode...")
    
    n = 15
    t = 3

    mInit = init(n, t, True)
    n, k, t = mInit[0]

    name = '-'.join([str(i) for i in time.gmtime(time.time())[:6]])
    outfile = name + '.mid'
    with open(outfile, 'w') as o:        
        last = 0
        for i in range(int(len(buf)/n)):
            msg = buf[i*n : (i+1)*n]
            value = debch(msg, mInit).ljust(k, '0')
            if i == int(len(buf)/n)-1:
                value = value[:-redun]
            o.write(value)
            o.flush()

            tmp = int(i * n / len(buf) * 100)
            if tmp > last:
                print("bch_decode:", tmp, '%') #输出压缩进度
                last = tmp

    print("BCH decode successful.")

    write4bits(name + '.mid') #中间过渡
    decodefile(name + '.hfm') #压缩译码

    return name
            
