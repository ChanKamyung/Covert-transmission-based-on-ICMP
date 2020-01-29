#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

from mLib.polymath \
     import poly, add, mul, div, getGF, getMinPoly, getValue, getValue2, \
            det, inv, mat_mul, dis, strip
from math import log
from random import randint

def init(n, t, debug=False):
    #本原多项式
    prims = {2: poly(0, 1, 2),
             3: poly(0, 1, 3),
             4: poly(0, 1, 4),
             5: poly(0, 2, 5),
             6: poly(0, 1, 6),
             7: poly(0, 3, 7),
             8: poly(0, 2, 3, 4, 8),
             9: poly(0, 4, 9),
             10: poly(0, 3, 10)}

    m = log(n + 1, 2)
    if m - int(m) != 0:
        m += 1
    m = int(m)
    n = 2**m - 1
    if t > int(n/2):
        print('最多只能纠%d位' % int((2**m - 1)/2))

    #本原多项式prim、GF(2**m - 1)瓦域元素mGF、极小多项式列表mMinPoly
    prim = prims[m]
    mGF = getGF(prim)
    mMinPoly = getMinPoly(prim, mGF)

    #生成多项式Q
    Q = '1'
    tmp = list(set(mMinPoly[1:2*t + 1]))
    for i in range(len(tmp)):
        Q = mul(Q, tmp[i])

    #获得原始消息长度k
    k = n - len(Q) + 1
    
    #debug
    if debug:
        print('本原多项式【%s】得到的GF(%d)的元素' % (prim, n + 1))
        for i, j in enumerate(mGF):
            print(i, '\t', j)
        print()
        print('本原多项式【%s】得到的极小多项式' % prim)
        for i, j in enumerate(mMinPoly):
            print(i, '\t', j)
        print()
        print('纠【t = %d】的生成多项式\t%s' % (t, Q))
        print('该BCH码为【(%d, %d)码】' % (n, k))

    return (n, k, t), prim, mGF, mMinPoly, Q

    
def enbch(msg, mInit, debug=False):
    (n, k, t), prim, mGF, mMinPoly, Q = mInit
    if len(msg) > k:
        print('原始消息长度不应超过%d' % k)
        return None
    
    #对msg编码
    res = mul(msg, Q).ljust(n, '0')

    #debug
    if debug:
        print('待发送\t%s' % msg)
        print('编码 ->', res)

    return res


def debch(msg, mInit, debug=False):
    (n, k, t), prim, mGF, mMinPoly, Q = mInit
    if msg == None or len(msg) != n:
        print('无效编码')
        return None

    v = div(msg, Q)
    if v[1] == '0':
        if debug:
            print('传输无错误')
            
        return v[0]
    else:
        e = v[1]

        #计算伴随式S
        S = []
        for i in range(2*t + 1):
            S.append(div(getValue(e, mGF[i]), prim)[1])

        #获得伴随式矩阵行列式M、错误个数cntr
        for i in range(t, 0, -1):
            M = []
            for j in range(i):
                M.append([])
                for k in range(i):
                    M[j].append(S[j + k + 1])

            if div(det(M), prim)[1] != '0':
                break
        cntr = len(M)

        #获得错误多项式系数gamma
        Sd = []
        for i in range(cntr + 1, 2*cntr + 1):
            Sd.append([S[i]])
        gamma = mat_mul(inv(M, prim, mGF), Sd, prim)

        #获得错误多项式err_poly
        err_poly = []
        for i in gamma:
            err_poly = i + err_poly
        err_poly = ['1'] + err_poly

        #获得错误位置err_pos [使用chien氏搜索法]
        err_pos = []
        for i in range(1, len(mGF)):
            if div(getValue2(err_poly, mGF[i]), prim)[1] == '0':
                err_pos.append(i if mGF[i] == '0' else n - i)
        err_pos.sort()

        #恢复msg
        msg = dis(msg, err_pos, n)

        #debug
        if debug:
            print('错误多项式 ->', e)
            print('伴随式')
            for i, j in enumerate(S):
                print('S%d' % i, '\t', j)
            print()
            print('错误个数 ->', cntr)
            print('伴随式矩阵行列式')
            for i in range(len(M)):
                for j in range(len(M)):
                    print('S%s [\'%s\']' % (S.index(M[i][j]), M[i][j]))
                print()
            print()
            print('错误位置多项式系数')
            for i, j in enumerate(gamma):
                print(len(gamma) - i, '\t', j)
            print()
            print('错误位置多项式 ->', err_poly)
            print('错误位置 ->', err_pos)
            print('编码恢复 ->', msg)
            
        return div(msg, Q)[0]


def random_dis(msg, mInit, israndom=True, debug=False):
    n, k, t = mInit[0]
    
    pos = []
    if israndom:
        for i in range(randint(0, t)):
            pos.append(randint(0, n-1))
        pos = list(set(pos))
    else:
        while len(pos) < t:
            pos.append(randint(0,n-1))
            pos = list(set(pos))

    #干扰
    res = dis(msg, pos, n)

    #debug
    if debug:
        print('干扰 ->', res, pos)

    return res


if __name__ == '__main__':
    n = 15
    t = 3

    mInit = init(n, t)
    n, k, t = mInit[0]

    msg = input('请输入长度：')
    X = enbch(msg, mInit)
    print(X)
    Y = random_dis(X, mInit)
    Z = debch(Y, mInit)
    print(Z)

    
