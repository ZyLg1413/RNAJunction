#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
Author: ZhangYi
Purpose: get some features of 3WJ to predict the angle of adjacent helix

"""

import math
import sys

sys.path.append("../../CommonTool/")
import func_lib


def dealFile(line):
    name = line.strip("").split(" ")[0]
    seq = line.strip("").split(" ")[3]
    ss = line.strip("").split(" ")[4]
    index1 = ss.index("()")
    index2 = ss.index("()", index1 + 1)

    # 统计第二个helix上面的碱基配对个数num2
    num2 = 0
    while True:
        if ss[index1 - num2] == '(' and ss[index1 + num2 + 1] == ')':
            num2 += 1
        else:
            break

    # 首先获得第一个螺旋碱基配对的个数，用num1表示
    num1 = 0
    while True:
        if ss[num1] == '(' and ss[-(num1 + 1)] == ')' and num1 <= index1 - num2:
            num1 += 1
        else:
            break

    # 统计第三个helix上面的碱基配对的个数
    num3 = 0
    while True:
        if ss[index2 - num3] == '(' and ss[index2 + num3 + 1] == ')':
            num3 += 1
        else:
            break

    return name, seq, ss, index1, index2, num1, num2, num3


def compare(x, y, z):
    t = 0
    if y < x:
        t = x
        x = y
        y = t
    if z < x:
        t = x
        x = z
        z = t
    if z < y:
        t = y
        y = z
        z = t
    sortlen = str(x) + ' ' \
              + str(y) + ' ' \
              + str(z) + ' \n'
    return sortlen


def loop_len(seq, ss, index1, index2, num1, num2, num3):
    ### 得到三分支环三个loop区的长度
    loop1 = index1 + 1 - num1 - num2
    loop2 = index2 + 1 - (index1 + 1) - num2 - num3
    loop3 = len(seq) - (index2 + 1) - num3 - num1

    ### 得到三个loop区上面碱基A、U、C、G的个数
    # 寻找每个环区上面的碱基A的个数
    Aloop1 = 0
    if loop1 != 0:
        for i in range(loop1):
            if seq[num1 + i] == 'A':
                Aloop1 += 1
    Aloop2 = 0
    if loop2 != 0:
        for i in range(loop2):
            if seq[index1 + num2 + 1 + i] == 'A':
                Aloop2 += 1
    Aloop3 = 0
    if loop3 != 0:
        for i in range(loop3):
            if seq[index2 + num3 + 1 + i] == 'A':
                Aloop3 += 1

    Uloop1 = 0
    if loop1 != 0:
        for i in range(loop1):
            if seq[num1 + i] == 'U':
                Uloop1 += 1

    Uloop2 = 0
    if loop2 != 0:
        for i in range(loop2):
            if seq[index1 + num2 + 1 + i] == 'U':
                Uloop2 += 1

    Uloop3 = 0
    if loop3 != 0:
        for i in range(loop3):
            if seq[index2 + num3 + 1 + i] == 'U':
                Uloop3 += 1

    Cloop1 = 0
    if loop1 != 0:
        for i in range(loop1):
            if seq[num1 + i] == 'C':
                Cloop1 += 1
    Cloop2 = 0
    if loop2 != 0:
        for i in range(loop2):
            if seq[index1 + num2 + 1 + i] == 'C':
                Cloop2 += 1
    Cloop3 = 0
    if loop3 != 0:
        for i in range(loop3):
            if seq[index2 + num3 + 1 + i] == 'C':
                Cloop3 += 1
    Gloop1 = 0
    if loop1 != 0:
        for i in range(loop1):
            if seq[num1 + i] == 'G':
                Gloop1 += 1
    Gloop2 = 0
    if loop2 != 0:
        for i in range(loop2):
            if seq[index1 + num2 + 1 + i] == 'G':
                Gloop2 += 1
    Gloop3 = 0
    if loop3 != 0:
        for i in range(loop3):
            if seq[index2 + num3 + 1 + i] == 'G':
                Gloop3 += 1

    # 比较loop2与loop3大小（l2l3）,loop1与loop3的大小（l1l3）,loop1与loop2的大小（l1l2）
    l2l3 = min(loop2, loop3)
    l1l3 = min(loop1, loop3)
    l1l2 = min(loop1, loop2)
    # 将loop1、loop2、loop3进行一个排序
    sortlen = compare(loop1, loop2, loop3)

    return loop1, loop2, loop3, Aloop1, Aloop2, Aloop3, Uloop1, Uloop2, Uloop3, Cloop1, Cloop2, \
           Cloop3, Gloop1, Gloop2, Gloop3, l1l2, l2l3, l1l3, sortlen


def ifwc(helixl, helixr):
    ### 判断一对碱基配对是否是标准碱基配对 AU,CG,GU
    if (helixl == 'A' and helixr == 'U') or \
            (helixl == 'U' and helixr == 'A') or \
            (helixl == 'C' and helixr == 'G') or \
            (helixl == 'G' and helixr == 'C') or \
            (helixl == 'G' and helixr == 'U') or \
            (helixl == 'U' and helixr == 'G'):
        result = 1
    else:
        result = -1
    return result


def get_wcpair(line, file, seq, num1, num2, num3, loop1, loop2, loop3):
    #### 获得helix末端只包含标准碱基配对的数据集（一对）

    index1l = num1 - 1
    index1r = num1 + 2 * num2 + 2 * num3 + loop1 + loop2 + loop3
    index2l = num1 + loop1
    index2r = index2l + 2 * num2 - 1
    index3l = num1 + loop1 + 2 * num2 + loop2
    index3r = index3l + 2 * num3 - 1
    # print(seq[index1l],seq[index1r],seq[index2l],seq[index2r],seq[index3l],seq[index3r])
    if ifwc(seq[index1l], seq[index1r]) > 0 and (ifwc(seq[index2l], seq[index2r])) > 0 and (
            ifwc(seq[index3l], seq[index3r])) > 0:
        func_lib.writeToDisk(line, file)


def get_index_pair(num1, num2, num3, loop1, loop2, loop3):
    index1l = num1 - 1
    index1r = num1 + 2 * num2 + 2 * num3 + loop1 + loop2 + loop3
    index2l = num1 + loop1
    index2r = index2l + 2 * num2 - 1
    index3l = num1 + loop1 + 2 * num2 + loop2
    index3r = index3l + 2 * num3 - 1
    return index1l, index1r, index2l, index2r, index3l, index3r


def loop_0(seq1, seq2, seq3, seq4):
    free = 0
    if seq1 == 'A' and seq2 == 'U':
        if seq3 == 'A' and seq4 == 'U':
            free = -0.9
        elif seq3 == 'C' and seq4 == 'G':
            free = -2.2
        elif seq3 == 'G' and seq4 == 'C':
            free = -2.1
        elif seq3 == 'G' and seq4 == 'U':
            free = -0.6
        elif seq3 == 'U' and seq4 == 'A':
            free = -1.1
        elif seq3 == 'U' and seq4 == 'G':
            free = -1.4
    elif seq1 == 'C' and seq2 == 'G':
        if seq3 == 'A' and seq4 == 'U':
            free = -2.1
        elif seq3 == 'C' and seq4 == 'G':
            free = -3.3
        elif seq3 == 'G' and seq4 == 'C':
            free = -2.4
        elif seq3 == 'G' and seq4 == 'U':
            free = -1.4
        elif seq3 == 'U' and seq4 == 'A':
            free = -2.1
        elif seq3 == 'U' and seq4 == 'G':
            free = -2.1
    elif seq1 == 'G' and seq2 == 'C':
        if seq3 == 'A' and seq4 == 'U':
            free = -2.4
        elif seq3 == 'C' and seq4 == 'G':
            free = -3.4
        elif seq3 == 'G' and seq4 == 'C':
            free = -3.3
        elif seq3 == 'G' and seq4 == 'U':
            free = -1.5
        elif seq3 == 'U' and seq4 == 'A':
            free = -2.2
        elif seq3 == 'U' and seq4 == 'G':
            free = -2.5
    elif seq1 == 'G' and seq2 == 'U':
        if seq3 == 'A' and seq4 == 'U':
            free = -1.3
        elif seq3 == 'C' and seq4 == 'G':
            free = -2.5
        elif seq3 == 'G' and seq4 == 'C':
            free = -2.1
        elif seq3 == 'G' and seq4 == 'U':
            free = -0.5
        elif seq3 == 'U' and seq4 == 'A':
            free = -1.4
        elif seq3 == 'U' and seq4 == 'G':
            free = 1.3
    elif seq1 == 'U' and seq2 == 'A':
        if seq3 == 'A' and seq4 == 'U':
            free = -1.3
        elif seq3 == 'C' and seq4 == 'G':
            free = -2.4
        elif seq3 == 'G' and seq4 == 'C':
            free = -2.1
        elif seq3 == 'G' and seq4 == 'U':
            free = -1.0
        elif seq3 == 'U' and seq4 == 'A':
            free = -0.9
        elif seq3 == 'U' and seq4 == 'G':
            free = -1.3
    elif seq1 == 'U' and seq2 == 'G':
        if seq3 == 'A' and seq4 == 'U':
            free = -1.0
        elif seq3 == 'C' and seq4 == 'G':
            free = -1.5
        elif seq3 == 'G' and seq4 == 'C':
            free = -1.4
        elif seq3 == 'G' and seq4 == 'U':
            free = 0.3
        elif seq3 == 'U' and seq4 == 'A':
            free = -0.6
        elif seq3 == 'U' and seq4 == 'G':
            free = -0.5
    return free


def loop_1(seq1, seq2, seq3, seq4):
    tmp = 2.1
    if seq1 == 'A' and seq2 == 'U':
        if seq3 == 'A' and seq4 == 'A':
            energy = -0.8
        elif seq3 == 'A' and seq4 == 'C':
            energy = -1.0
        elif seq3 == 'A' and seq4 == 'G':
            energy = -0.8
        elif seq3 == 'A' and seq4 == 'U':
            energy = -1.0
        elif seq3 == 'C' and seq4 == 'A':
            energy = -0.6
        elif seq3 == 'C' and seq4 == 'C':
            energy = -0.7
        elif seq3 == 'C' and seq4 == 'G':
            energy = -0.6
        elif seq3 == 'C' and seq4 == 'U':
            energy = -0.7
        elif seq3 == 'G' and seq4 == 'A':
            energy = -0.8
        elif seq3 == 'G' and seq4 == 'C':
            energy = -1.0
        elif seq3 == 'G' and seq4 == 'G':
            energy = -0.8
        elif seq3 == 'G' and seq4 == 'U':
            energy = -1.0
        elif seq3 == 'U' and seq4 == 'A':
            energy = -0.6
        elif seq3 == 'U' and seq4 == 'C':
            energy = -0.8
        elif seq3 == 'U' and seq4 == 'G':
            energy = -0.6
        elif seq3 == 'U' and seq4 == 'U':
            energy = -0.8

    elif seq1 == 'C' and seq2 == 'G':
        if seq3 == 'A' and seq4 == 'A':
            energy = -1.5
        elif seq3 == 'A' and seq4 == 'C':
            energy = -1.5
        elif seq3 == 'A' and seq4 == 'G':
            energy = -1.4
        elif seq3 == 'A' and seq4 == 'U':
            energy = -1.5
        elif seq3 == 'C' and seq4 == 'A':
            energy = -1.0
        elif seq3 == 'C' and seq4 == 'C':
            energy = -1.1
        elif seq3 == 'C' and seq4 == 'G':
            energy = -1.0
        elif seq3 == 'C' and seq4 == 'U':
            energy = -0.8
        elif seq3 == 'G' and seq4 == 'A':
            energy = -1.4
        elif seq3 == 'G' and seq4 == 'C':
            energy = -1.5
        elif seq3 == 'G' and seq4 == 'G':
            energy = -1.6
        elif seq3 == 'G' and seq4 == 'U':
            energy = -1.5
        elif seq3 == 'U' and seq4 == 'A':
            energy = -1.0
        elif seq3 == 'U' and seq4 == 'C':
            energy = -1.4
        elif seq3 == 'U' and seq4 == 'G':
            energy = -1.0
        elif seq3 == 'U' and seq4 == 'U':
            energy = -1.2

    elif seq1 == 'G' and seq2 == 'C':
        if seq3 == 'A' and seq4 == 'A':
            energy = -1.1
        elif seq3 == 'A' and seq4 == 'C':
            energy = -1.5
        elif seq3 == 'A' and seq4 == 'G':
            energy = -1.3
        elif seq3 == 'A' and seq4 == 'U':
            energy = -1.5
        elif seq3 == 'C' and seq4 == 'A':
            energy = -1.1
        elif seq3 == 'C' and seq4 == 'C':
            energy = -0.7
        elif seq3 == 'C' and seq4 == 'G':
            energy = -1.1
        elif seq3 == 'C' and seq4 == 'U':
            energy = -0.5
        elif seq3 == 'G' and seq4 == 'A':
            energy = -1.6
        elif seq3 == 'G' and seq4 == 'C':
            energy = -1.5
        elif seq3 == 'G' and seq4 == 'G':
            energy = -1.4
        elif seq3 == 'G' and seq4 == 'U':
            energy = -1.5
        elif seq3 == 'U' and seq4 == 'A':
            energy = -1.1
        elif seq3 == 'U' and seq4 == 'C':
            energy = -1.0
        elif seq3 == 'U' and seq4 == 'G':
            energy = -1.1
        elif seq3 == 'U' and seq4 == 'U':
            energy = -0.7

    elif seq1 == 'G' and seq2 == 'U':
        if seq3 == 'A' and seq4 == 'A':
            energy = -0.3
        elif seq3 == 'A' and seq4 == 'C':
            energy = -1.0
        elif seq3 == 'A' and seq4 == 'G':
            energy = -0.8
        elif seq3 == 'A' and seq4 == 'U':
            energy = -1.0
        elif seq3 == 'C' and seq4 == 'A':
            energy = -0.6
        elif seq3 == 'C' and seq4 == 'C':
            energy = -0.7
        elif seq3 == 'C' and seq4 == 'G':
            energy = -0.6
        elif seq3 == 'C' and seq4 == 'U':
            energy = -0.7
        elif seq3 == 'G' and seq4 == 'A':
            energy = -0.6
        elif seq3 == 'G' and seq4 == 'C':
            energy = -1.0
        elif seq3 == 'G' and seq4 == 'G':
            energy = -0.8
        elif seq3 == 'G' and seq4 == 'U':
            energy = -1.0
        elif seq3 == 'U' and seq4 == 'A':
            energy = -0.6
        elif seq3 == 'U' and seq4 == 'C':
            energy = -0.8
        elif seq3 == 'U' and seq4 == 'G':
            energy = -0.6
        elif seq3 == 'U' and seq4 == 'U':
            energy = -0.6

    elif seq1 == 'U' and seq2 == 'A':
        if seq3 == 'A' and seq4 == 'A':
            energy = -1.0
        elif seq3 == 'A' and seq4 == 'C':
            energy = -0.8
        elif seq3 == 'A' and seq4 == 'G':
            energy = -1.1
        elif seq3 == 'A' and seq4 == 'U':
            energy = -0.8
        elif seq3 == 'C' and seq4 == 'A':
            energy = -0.7
        elif seq3 == 'C' and seq4 == 'C':
            energy = -0.6
        elif seq3 == 'C' and seq4 == 'G':
            energy = -0.7
        elif seq3 == 'C' and seq4 == 'U':
            energy = -0.5
        elif seq3 == 'G' and seq4 == 'A':
            energy = -1.1
        elif seq3 == 'G' and seq4 == 'C':
            energy = -0.8
        elif seq3 == 'G' and seq4 == 'G':
            energy = -1.2
        elif seq3 == 'G' and seq4 == 'U':
            energy = -0.8
        elif seq3 == 'U' and seq4 == 'A':
            energy = -0.7
        elif seq3 == 'U' and seq4 == 'C':
            energy = -0.6
        elif seq3 == 'U' and seq4 == 'G':
            energy = -0.7
        elif seq3 == 'U' and seq4 == 'U':
            energy = -0.5

    elif seq1 == 'U' and seq2 == 'G':
        if seq3 == 'A' and seq4 == 'A':
            energy = -1.0
        elif seq3 == 'A' and seq4 == 'C':
            energy = -0.8
        elif seq3 == 'A' and seq4 == 'G':
            energy = -1.1
        elif seq3 == 'A' and seq4 == 'U':
            energy = -0.8
        elif seq3 == 'C' and seq4 == 'A':
            energy = -0.7
        elif seq3 == 'C' and seq4 == 'C':
            energy = -0.6
        elif seq3 == 'C' and seq4 == 'G':
            energy = -0.7
        elif seq3 == 'C' and seq4 == 'U':
            energy = -0.5
        elif seq3 == 'G' and seq4 == 'A':
            energy = -0.5
        elif seq3 == 'G' and seq4 == 'C':
            energy = -0.8
        elif seq3 == 'G' and seq4 == 'G':
            energy = -0.8
        elif seq3 == 'G' and seq4 == 'U':
            energy = -0.8
        elif seq3 == 'U' and seq4 == 'A':
            energy = -0.7
        elif seq3 == 'U' and seq4 == 'C':
            energy = -0.6
        elif seq3 == 'U' and seq4 == 'G':
            energy = -0.7
        elif seq3 == 'U' and seq4 == 'U':
            energy = -0.5
    return energy + tmp


def get_energy(looplen, seq1, seq2, seq3, seq4):
    a, b, c, h = 9.3, -0.3, -0.9, 2
    if looplen == 0:
        ener = loop_0(seq1, seq2, seq3, seq4)
    elif looplen == 1:
        ener = loop_1(seq1, seq2, seq3, seq4)
    elif looplen <= 6 and looplen >= 2:
        ener = a + b * looplen + c * h
    else:
        ener = a + 6 * b + 1.1 * math.log(looplen / 6, math.e) + c * h
    return round(ener, 1)


def main():
    cout = 0
    for line in open("../data/3wj_wc_1.txt"):
        name, seq, ss, index1, index2, num1, num2, num3 = dealFile(line)
        loop1, loop2, loop3, Aloop1, Aloop2, Aloop3, Uloop1, Uloop2, Uloop3, \
        Cloop1, Cloop2, Cloop3, Gloop1, Gloop2, Gloop3, \
        l1l2, l2l3, l1l3, sortlen \
            = loop_len(seq, ss, index1, index2, num1, num2, num3)

        ### 获得helix末端只包含标准碱基配对的一些数据集
        # get_wcpair(line, "../../dataSet/3wj_wc_1.txt",seq,num1, num2, num3, loop1, loop2, loop3)

        ## 获得相邻螺旋之间的末端碱基配对之间的自由能
        index1l, index1r, index2l, index2r, index3l, index3r = get_index_pair(num1, num2, num3, loop1, loop2,
                                                                              loop3)
        energy1 = get_energy(loop1, seq[index1l], seq[index1r], seq[index1l + 1], seq[index1r - 1])
        energy2 = get_energy(loop2, seq[index2l], seq[index2r], seq[index2l + 1], seq[index2r - 1])
        energy3 = get_energy(loop3, seq[index3l], seq[index3r], seq[index3l + 1], seq[index3r - 1])

        feature = name + " " + str(loop1) + " " + str(loop2) + " " + str(loop3) + " " + str(Aloop1) \
                  + " " + str(Aloop2) + " " + str(Aloop3) + " " + str(Uloop1) + " " + str(Uloop2) \
                  + " " + str(Uloop3) + " " + str(Cloop1) + " " + str(Cloop2) + " " + str(Cloop3) \
                  + " " + str(Gloop1) + " " + str(Gloop2) + " " + str(Gloop3) + " " + str(l1l2) \
                  + " " + str(l2l3) + " " + str(l1l3) + " " + str(sortlen).strip() + " " + str(energy1) \
                  + " " + str(energy2) + " " + str(energy3) + "\n"
        func_lib.writeToDisk(feature, "../data/3wj_feature.txt")


if __name__ == '__main__':
    main()
