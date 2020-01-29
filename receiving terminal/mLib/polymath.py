#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

from random import *

def poly(*arg):
    res = ['0'] * (max(arg)+1)
    for i in arg:
        res[i] = '1'
    return ''.join(res)

def strip(num):
    while num[-1] == '0' and len(num) != 1:
        num = num[:-1]
    return num
    
def add(a, b):
    a = strip(a)
    b = strip(b)
    
    res = [0] * min(len(a), len(b))
    
    for i in range(len(res)):
        res[i] = str((eval(a[i]) + eval(b[i])) % 2)
    res = ''.join(res)

    if len(a) > len(b):
        res += a[i+1:]
    else:
        res += b[i+1:]
        
    return strip(res)
            
def mul(a, b):
    a = strip(a)
    b = strip(b)
    
    res = [0] * (len(a) + len(b) - 1)

    for i in range(len(res)):
        s = 0
        for j in range(len(a)):
            k = i - j
            if 0 <= k < len(b):
                s += eval(a[j]) * eval(b[k])
        s %= 2
        res[i] = str(s)

    return strip(''.join(res))

def div(a, b):
    a = strip(a)
    b = strip(b)
    if b == '0':
        return None, None
        
    q = [0] * (len(a) - len(b) + 1)
    i = len(a) - len(b)
    while i >= 0:
        q[i] = a[-1]
        if q[i] == '1':
            a = add(a, '0'*i + b)
            a = a.ljust(len(b) + i, '0')
        i -= 1
        a = a[:-1]
    q = '0' if len(q) == 0 else ''.join(q)
    a = '0' if len(a) == 0 else a
    
    q = strip(q)
    r = strip(a)
    return q, r

def getGF(prim):
    prim = strip(prim)
    if prim == '0':
        return None
    
    res = ['0'] * 2**(len(prim)-1)
    res[1] = '01'
    for i in range(2, len(res)):
        res[i] = div(mul(res[i-1], '01'), prim)[1]
    return res

def getCoeff(p, arg):
    res = '1'
    for i in arg:
        res = mul(res, p[i])
        
    if arg[-1] - arg[0] == len(arg) - 1 and arg[-1] == len(p) - 1:
        return res
    else:
        if arg[-1] != len(p) - 1:
            arg[-1] += 1
        else:
            for i in range(1, len(arg)+1):
                if arg[-i] != len(p) - i:
                    break
            arg[-i] += 1
            for j in range(1, i):
                arg[-i+j] = arg[-i+j-1] + 1
        return add(res, getCoeff(p, arg))
    
def getPolyCoeff(p, prim):
    res = [0] * (len(p)+1)
    res[-1] = '1'
    for i in range(len(p)):
        arg = [j for j in range(len(p)-i)]
        res[i] = div(getCoeff(p, arg), prim)[1][0]
    return ''.join(res)
    
def getMinPoly(prim, mGF):
    GF_elements = mGF
    res = [None]*len(GF_elements)

    for i in range(1, len(res)):
        if res[i] == None:
            p = []
            index = []
            p.append(GF_elements[i])
            index.append(i)
            j = i * 2 % (len(GF_elements)-1)
            
            while j != i and j != 0:
                p.append(GF_elements[j])
                index.append(j)
                j = j * 2 % (len(GF_elements)-1)

            coeff = getPolyCoeff(p, prim)

            for j in index:
                res[j] = coeff
    return res
        
def getValue(p, arg):
    res = '0'
    for i in range(len(p)):
        if p[i] == '1':
            tmp = '1'
            for j in range(i):
                tmp = mul(tmp, arg)
            res = add(res, tmp)
    return res

def getValue2(l, arg):
    res = '0'
    for i in range(len(l)):
        if l[i] != '0':
            tmp = '1'
            for j in range(i):
                tmp = mul(tmp, arg)
            tmp = mul(tmp, l[i])
            res = add(res, tmp)
    return res

def adj(mat, u, v):
    n= len(mat)
    
    res = []
    for i in range(n):
        if i != u:
            res.append([])
            for j in range(n):
                if j != v:
                    res[-1].append(mat[i][j])
    return res
    
def det(mat):
    n = len(mat)
    
    res = '0'
    if n == 1:
        return mat[0][0]
    else:
        for i in range(n):
            res = add(res, mul(mat[0][i], det(adj(mat, 0, i))))
        return res

def inv(mat, prim, mGF):
    n = len(mat)
    det_mat = div(det(mat), prim)[1]
    if det_mat == '0':
        return None

    det_mat_inv = det_mat if det_mat == '1' \
                  else mGF[len(mGF)-mGF.index(det_mat)-1]
    if n == 1:
        return [[det_mat_inv]]
    
    res = []
    for i in range(n):
        res.append([])
        for j in range(n):
            tmp = adj(mat, j, i)
            res[-1].append(div(mul(det(tmp), det_mat_inv), prim)[1])
    return res

def mat_mul(a, b, prim):
    l = len(a)
    m = len(a[0])
    n = len(b[0])
    
    res = []
    for i in range(l):
        res.append([])
        for j in range(n):
            tmp = '0'
            for k in range(m):
                tmp = div(add(tmp, mul(a[i][k], b[k][j])), prim)[1]
            res[-1].append(tmp)
    return res
                    
def dis(r, arg, n):
    arg.sort()
    res = ''
    cntr = 0
    for i in arg:
        tmp = '1' if r[i] == '0' else '0'
        res += r[cntr:i] + tmp
        cntr = i + 1
    res += r[cntr:]
    return res.ljust(n, '0')

if __name__ == '__main__':
    prim = poly(0, 1, 4)
    mGF = getGF(prim)
    mMinPoly = getMinPoly(prim, mGF)
    
    print('>>Get a poly:', poly(6, 9, 12) == '0000001001001')
    print('>>test add:', add('01011', '1011000') == '11101')
    print('>>test mul:', mul('11', '11') == '101')
    print('>>test div:', div(poly(0,10,30,35,45,50,65), prim)[1] == '0')
    print('>>test getGF:', getGF(prim) == \
          ['0', '01', '001', '0001', \
           '11', '011', '0011', '1101', \
           '101', '0101', '111', '0111', \
           '1111', '1011', '1001', '1'])
    print('>>test getCoeff:',div(getCoeff(['01','001','110','101'],[0,1]),prim)\
          == ('1', '0'))
    print('>>test getPolyCoeff:', getPolyCoeff(['01','001','110','101'], prim)\
          == '11001')
    print('>>test getMinPoly:', getMinPoly(prim, mGF) == \
          [None, '11001', '11001', '11111', \
           '11001', '111', '11111', '10011', \
           '11001', '11111', '111', '10011', \
           '11111', '10011', '10011', '11'])
    print('>>test getValue:', div(getValue('11111', poly(3)), prim)[1] == '0')
    print('>>test getValue2:', div(getValue2(['1','0111','101'], '111'), prim)[1]\
          == '0')

    mat2 = [[mGF[11], mGF[7]], \
            [mGF[7], mGF[7]]]
    mat3 = [[mGF[11], mGF[7], mGF[7]], \
            [mGF[7], mGF[7], mGF[14]], \
            [mGF[7], mGF[14], mGF[5]]]
    mat2_inv = [[mGF[7], mGF[7]], \
                [mGF[7], mGF[11]]]

    print('>>test det:', div(det(mat2), prim)[1] == '1' \
                         and div(det(mat3), prim)[1] == '0')
    
    print('>>test inv:', inv(mat2, prim, mGF) == mat2_inv \
                         and inv(mat3, prim, mGF) == None)
    
    print('>>test mat_mul:', mat_mul(mat2_inv, [[mGF[7]], [mGF[14]]], prim) \
                             == [[mGF[8]], [mGF[11]]])    
    print('---------------------')
    
    n = 2**(len(prim)-1)-1
    t = 3

    print('本原多项式【%s】得到的GF(%d)的元素' % (prim, n + 1))
    for i, j in enumerate(mGF):
        print(i, '\t', j)
    print()
    
    print('本原多项式【%s】得到的极小多项式' % prim)
    for i, j in enumerate(mMinPoly):
        print(i, '\t', j)
    print()
    
    Q = '1'
    tmp = list(set(mMinPoly[1:2*t+1]))
    for i in range(len(tmp)):
        Q = mul(Q, tmp[i])
    print('纠【t = %d】的生成多项式\t%s' % (t, Q))

    k = n - len(Q) + 1
    print('该BCH码为 (%d, %d) 码' % (n, k))

    m = []
    for i in range(n):
        m.append(str(randint(0,1)))
    m = ''.join(m)[:k]
    print('待发送\t%s' % m)

    r = mul(m, Q).ljust(n, '0')
    rr = r
    print('编码 ->', r)

    tmp = []
    for i in range(randint(1, t)):
        tmp.append(randint(0, 14))
    tmp = list(set(tmp))
    r = dis(r, tmp, n)
    print('干扰 ->', r, tmp)
    
    '''cntr = 0
    for i in range(t):
        tmp = 2*(i + 1) - 1
        arg = '0'*tmp + '1' 
        if div(getValue(r, arg), prim)[1] != '0':
            cntr += 1
    print('错误个数\t%d' % cntr)'''

    e = div(r, Q)[1]
    print('错误多项式 ->', e)

    S = []
    for i in range(2*t + 1):
        S.append(div(getValue(e, mGF[i]), prim)[1])
    print('伴随式')
    for i, j in enumerate(S):
        print(i, '\t', j)
    print()

    for i in range(t, 0, -1):
        M = []
        for j in range(i):
            M.append([])
            for k in range(i):
                M[j].append(S[j + k + 1])

        if div(det(M), prim)[1] != '0':
            break
    cntr = len(M)
    print('错误个数 ->', cntr)
    print('伴随式矩阵行列式')
    for i in range(len(M)):
        for j in range(len(M)):
            print(M[i][j])
        print()
    print()

    Sd = []
    for i in range(cntr + 1, 2*cntr + 1):
        Sd.append([S[i]])
    gamma = mat_mul(inv(M, prim, mGF), Sd, prim)
    print('错误位置多项式系数')
    for i, j in enumerate(gamma):
        print(len(gamma) - i, '\t', j)
    print()

    err_poly = []
    for i in gamma:
        err_poly = i + err_poly
    err_poly = ['1'] + err_poly
    print('错误位置多项式 ->', err_poly)

    res = []
    for i in range(1, len(mGF)):
        if div(getValue2(err_poly, mGF[i]), prim)[1] == '0':
            res.append(i if mGF[i] == '0' else n - i)
    res.sort()
    print('错误位置 ->', res)

    print('恢复的结果 ->', dis(r, res, n), dis(r,res, n) == rr)
