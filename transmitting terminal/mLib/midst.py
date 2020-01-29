#!/usr/bin/python3
# _*_ coding=utf-8 _*_

def read2bits(infile):
    with open(infile, 'rb') as f:
        f.seek(0, 2)
        eof = f.tell()
        f.seek(0)
        
        outfile = infile.replace(infile[infile.index('.'):], '.mid')
        with open(outfile, 'w') as o:
            for i in range(eof):
                value = int.from_bytes(f.read(1), byteorder= 'big')
                o.write(bin(value).replace('0b', '').rjust(8, '0'))
                if i == 0:
                    print(value, bin(value).replace('0b', '').rjust(8, '0'))

def write4bits(infile):
    with open(infile, 'r') as f:
        f.seek(0, 2)
        eof = f.tell()
        f.seek(0)
        print(eof)
        outfile = infile.replace(infile[infile.index('.'):], '.hfm_')
        with open(outfile, 'wb') as o:
            raw = 0b1
            for i in range(int(eof/8)):
                value = f.read(8)
                for x in value:
                    raw = raw << 1
                    if x == '1':
                        raw = raw | 1
                    if raw.bit_length() == 9:
                        raw = raw & (~(1 << 8))
                        o.write(int.to_bytes(raw ,1 , byteorder= 'big'))
                        o.flush()

                        raw = 0b1
        

if __name__ == '__main__':
    n = eval(input('1 编码 2 译码：'))
    if n == 1:
        read2bits(input('请输入文件名：'))
    else:
        write4bits(input('请输入文件名：'))
