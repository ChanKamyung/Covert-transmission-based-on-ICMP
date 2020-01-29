#!/usr/bin/python3
# _*_ coding=utf-8 _*_

import sys
sys.setrecursionlimit(1000000) #压缩大文件实时会出现超出递归深度，故修改限制

#定义哈夫曼树的节点类
class node(object):
    def __init__(self, value=None, left=None, right=None, father=None):
        self.value = value
        self.left = left
        self.right = right
        self.father = father

    def build_father(left, right):
    	n = node(value= left.value + right.value, left= left, right= right)
    	left.father = right.father = n
    	return n

    def encode(n):
        if n.father == None:
            return b''
        if n.father.left == n:
            return node.encode(n.father) + b'0' #左节点编号'0'
        else:
            return node.encode(n.father) + b'1' #右节点编号'1'


#哈夫曼树构建
def build_tree(l):
    if len(l) == 1:
        return l
    sorts = sorted(l, key= lambda x: x.value, reverse= False) #升序排列
    n = node.build_father(sorts[0], sorts[1])
    sorts.pop(0)
    sorts.pop(0)
    sorts.append(n)
    return build_tree(sorts)


def encode(node_dict, debug=False):
    ec_dict = {}
    for x in node_dict.keys():
        ec_dict[x] = node.encode(node_dict[x])
        if debug == True: #输出编码表（用于调试）
            print(x)
            print(ec_dict[x])
    return ec_dict


def encodefile(inputfile):
    #数据初始化
    node_dict = {} #建立原始数据与编码节点的映射，便于稍后输出数据的编码
    count_dict = {}
    
    print("Starting encode...")

    with open(inputfile,"rb") as f:
        bytes_width = 1 #每次读取的字节宽度
        i = 0

        f.seek(0,2)
        count = f.tell() / bytes_width
        print('length =', count)
        nodes = [] #结点列表，用于构建哈夫曼树
        buff = [b''] * int(count)
        f.seek(0)

        #计算字符频率,并将单个字符构建成单一节点
        while i < count:
            buff[i] = f.read(bytes_width)
            if count_dict.get(buff[i], -1) == -1:
                count_dict[buff[i]] = 0
            count_dict[buff[i]] = count_dict[buff[i]] + 1
            i = i + 1
        print("Read OK")
        #print(count_dict) #输出权值字典,可注释掉
        for x in count_dict.keys():
            node_dict[x] = node(count_dict[x])
            nodes.append(node_dict[x])
    
    tree = build_tree(nodes) #哈夫曼树构建
    ec_dict = encode(node_dict) #构建编码表
    print("Encode OK")

    head = sorted(count_dict.items(), \
                  key= lambda x: x[1] ,reverse= True) #对所有根节点降序排序
    bit_width = 1
    print("head:",head[0][1]) #动态调整编码表的字节长度，优化文件头大小
    if head[0][1] > 255:
        bit_width = 2
        if head[0][1] > 65535:
            bit_width = 3
            if head[0][1] > 16777215:
                bit_width = 4
    print("bit_width:", bit_width)
    
    name = inputfile.split('.')
    with open(name[0]+'.hfm', 'wb') as o:
        name = inputfile.split('/')
        o.write((name[-1] + '\n').encode('utf-8')) #写出原文件名
        o.write(int.to_bytes(len(ec_dict), 2, byteorder= 'big')) #写出结点数量
        o.write(int.to_bytes(bit_width, 1, byteorder= 'big')) #写出编码表字节宽度
        for x in ec_dict.keys(): #编码文件头
            o.write(x)
            o.write(int.to_bytes(count_dict[x], bit_width, byteorder= 'big'))
        print('head OK')

        raw = 0b1
        last = 0
        for i in range(int(count)): #开始压缩数据
            for x in ec_dict[buff[i]]:
                raw = raw << 1
                if x == 49:
                    raw = raw | 1
                if raw.bit_length() == 9:
                    raw = raw & (~(1 << 8))
                    o.write(int.to_bytes(raw ,1 , byteorder= 'big'))
                    o.flush()
                    
                    raw = 0b1
                    tmp = int(i  / len(buff) * 100)
                    if tmp > last:
                        print("encode:", tmp, '%') #输出压缩进度
                        last = tmp

        if raw.bit_length() > 1: #处理文件尾部不足一个字节的数据
            offset = 8 - (raw.bit_length() - 1)
            raw = raw << offset
            raw = raw & (~(1 << raw.bit_length() - 1))
            o.write(int.to_bytes(raw ,1 , byteorder = 'big'))
            o.write(int.to_bytes(offset, 1, byteorder = 'big')) ###

    print("File encode successful.")


def decodefile(inputfile):
    print("Starting decode...")
    
    with open(inputfile, 'rb') as f:
        f.seek(0, 2)
        eof = f.tell()
        f.seek(-1, 1)
        offset = int.from_bytes(f.read(1), byteorder= 'big')
        f.seek(0)
        name = inputfile.split('/')
        outputfile = inputfile.replace(name[-1], \
                                       f.readline().decode('utf-8'))

        #删除 NULL byte
        outputfile = list(outputfile)
        for i in range(len(outputfile) - 1): #最后一个'\n'不用管
            if ord(outputfile[i]) < 32:
                outputfile[i] = '_'
        outputfile = ''.join(outputfile)

        with open(inputfile.replace('.hfm', '') + outputfile.replace('\n','') ,'wb') as o:
            count = int.from_bytes(f.read(2), \
                                   byteorder= 'big') #取出结点数量
            bit_width = int.from_bytes(f.read(1), \
                                       byteorder= 'big') #取出编码表字宽

            de_dict = {}
            for i in range(int(count)): #解析文件头
                key = f.read(1)
                value = int.from_bytes(f.read(bit_width), byteorder= 'big')
                de_dict[key] = value

            node_dict = {}
            nodes = []
            inverse_dict = {}
            for x in de_dict.keys():
                node_dict[x] = node(de_dict[x])
                nodes.append(node_dict[x])
            tree = build_tree(nodes) #重建哈夫曼树
            ec_dict = encode(node_dict) #建立编码表
            for x in ec_dict.keys(): #反向字典构建
                inverse_dict[ec_dict[x]] = x

            data = b''
            raw = 0
            last = 0
            for i in range(f.tell(), eof - 1): #efo处记录的是offset，故此处-1
                raw = int.from_bytes(f.read(1), byteorder= 'big')
                #print("raw:",raw)
                j = 8
                while j > 0:
                    if (raw >> (j - 1)) & 1 == 1:
                        data = data + b'1'
                        raw = raw & (~(1 << (j - 1)))
                    else:
                        data = data + b'0'
                        raw = raw & (~(1 << (j - 1)))
                        
                    if inverse_dict.get(data, -1) != -1:
                        o.write(inverse_dict[data])
                        o.flush()
                        if i == eof - 2 and j - offset == 1:
                            break
                        #print("decode",data,":",inverse_dict[data])
                        data = b''
                    j = j - 1
            
                tep = int(i / eof * 100)
                if tep > last:							
                    print("decode:", tep,'%') #输出解压进度
                    last = tep
                raw = 0

    print("File decode successful.")

if __name__ == '__main__':

    if input("1：压缩文件\t2：解压文件\n请输入你要执行的操作：") == '1':
        encodefile(input("请输入要压缩的文件："))
    else:
        decodefile(input("请输入要解压的文件："))  
