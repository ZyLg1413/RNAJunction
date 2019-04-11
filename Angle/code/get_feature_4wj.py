#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
Author: ZhangYi
Purpose: get some features of 4WJ to predict the angle of adjacent helix

"""
import sys

sys.path.append("../../CommonTool/")
import func_lib

sys.path.append(".")
import  get_feature_3wj


def dealFile(line):
    pdbName = line.strip("").split(" ")[0]
    # file = open("Loop/" + pdbName + '.txt', "w")
    seq = line.strip("").split(" ")[3]
    ss = line.strip("").split(" ")[4]
    index1 = ss.index("()")
    index2 = ss.index("()", index1 + 1)
    index3 = ss.index("()", index2 + 1)

    # 统计第二个helix上面的碱基配对个数num2
    num2 = 0
    while True:
        if ss[index1 - num2] == '(' and ss[index1 + num2 + 1] == ')':
            num2 += 1
        else:
            break

    # 统计第三个螺旋上面碱基配对个数num3
    num3 = 0
    while True:
        if ss[index2 - num3] == '(' and ss[index2 + num3 + 1] == ')':
            num3 += 1
        else:
            break

    # 首先获得第一个螺旋碱基配对的个数，用num1表示
    num1 = 0
    while True:
        if ss[num1] == '(' and ss[-(num1 + 1)] == ')' and num1 <= index1 - num2:
            num1 += 1
        else:
            break

    # 统计第四个helix上面的碱基配对的个数
    num4 = 0
    while True:
        if ss[index3 - num4] == '(' and ss[index3 + num4 + 1] == ')':
            num4 += 1
        else:
            break

    return pdbName, seq, ss, index1, index2, index3, num1, num2, num3, num4


def loop_len(seq, ss, index1, index2, index3, num1, num2, num3, num4):
    lis = []
    loop1 = index1 + 1 - num1 - num2
    loop2 = index2 + 1 - (index1 + 1) - num2 - num3
    loop3 = index3 + 1 - (index2 + 1) - num3 - num4
    loop4 = len(ss) - (index3 + 1) - num4 - num1

    lis.append(loop1), lis.append(loop2), lis.append(loop3), lis.append(loop4)
    lis.sort()
    l1 = lis[0]
    l2 = lis[1]
    l3 = lis[2]
    l4 = lis[3]

    ### 得到三个loop区上面碱基A和U的个数
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
    Aloop4 = 0
    if loop4 != 0:
        for i in range(loop4):
            if seq[num1 + i] == 'A':
                Aloop4 += 1
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
    Uloop4 = 0
    if loop4 != 0:
        for i in range(loop4):
            if seq[num1 + i] == 'U':
                Uloop4 += 1

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
    Cloop4 = 0
    if loop4 != 0:
        for i in range(loop4):
            if seq[num1 + i] == 'C':
                Cloop4 += 1

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
    Gloop4 = 0
    if loop4 != 0:
        for i in range(loop4):
            if seq[num1 + i] == 'G':
                Gloop4 += 1

    l1l3 = min(loop1, loop3)
    l2l4 = min(loop2, loop4)

    return loop1, loop2, loop3, loop4, Aloop1, Aloop2, Aloop3, Aloop4, Uloop1, Uloop2, Uloop3, Uloop4, \
           Cloop1, Cloop2, Cloop3, Cloop4, Gloop1, Gloop2, Gloop3, Gloop4, l1l3, l2l4, l1, l2, l3, l4


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


def get_wcpair(line, file, seq, num1, num2, num3, num4, loop1, loop2, loop3, loop4):
    #### 获得helix末端只包含标准碱基配对的数据集（一对）

    index1l = num1 - 1
    index2l = index1l + loop1 + 1
    index2r = index2l + 2 * num2 - 1
    index3l = index2r + loop2 + 1
    index3r = index3l + 2 * num3 - 1
    index4l = index3r + loop3 + 1
    index4r = index4l + 2 * num4 - 1
    index1r = index4r + loop4 + 1

    # print(seq[index1l],seq[index1r],seq[index2l],seq[index2r],seq[index3l],seq[index3r])
    if ifwc(seq[index1l], seq[index1r]) > 0 and (ifwc(seq[index2l], seq[index2r])) > 0 \
            and (ifwc(seq[index3l], seq[index3r])) > 0 and (ifwc(seq[index4l], seq[index4r])) > 0:
        func_lib.writeToDisk(line, file)


def get_index_pair(num1, num2, num3, num4, loop1, loop2, loop3, loop4):
    index1l = num1 - 1
    index2l = index1l + loop1 + 1
    index2r = index2l + 2 * num2 - 1
    index3l = index2r + loop2 + 1
    index3r = index3l + 2 * num3 - 1
    index4l = index3r + loop3 + 1
    index4r = index4l + 2 * num4 - 1
    index1r = index4r + loop4 + 1
    return index1l, index1r, index2l, index2r, index3l, index3r, index4l, index4r


def main():
    cout = 0

    for line in open("../data/4wj_wc_1.txt"):
        pdbName, seq, ss, index1, index2, index3, num1, num2, num3, num4 = dealFile(line)
        loop1, loop2, loop3, loop4, Aloop1, Aloop2, Aloop3, Aloop4, Uloop1, Uloop2, Uloop3, Uloop4, \
        Cloop1, Cloop2, Cloop3, Cloop4, Gloop1, Gloop2, Gloop3, Gloop4 \
            , l1l3, l2l4, l1, l2, l3, l4 \
            = loop_len(seq, ss, index1, index2, index3, num1, num2, num3, num4)

        index1l, index1r, index2l, index2r, index3l, index3r, index4l, index4r = \
            get_index_pair(num1, num2, num3, num4, loop1, loop2, loop3, loop4)
        energy1 = get_feature_3wj.get_energy(loop1, seq[index1l], seq[index1r], seq[index1l + 1], seq[index1r - 1])
        energy2 = get_feature_3wj.get_energy(loop2, seq[index2l], seq[index2r], seq[index2l + 1], seq[index2r - 1])
        energy3 = get_feature_3wj.get_energy(loop3, seq[index3l], seq[index3r], seq[index3l + 1], seq[index3r - 1])
        energy4 = get_feature_3wj.get_energy(loop4, seq[index4l], seq[index4r], seq[index4l + 1], seq[index4r - 1])

        feature = pdbName + " " + str(loop1) + " " + str(loop2) + " " + str(loop3) + " " + str(loop4) \
                  + " " + str(Aloop1) + " " + str(Aloop2) + " " + str(Aloop3) + " " + str(Aloop4) \
                  + " " + str(Uloop1) + " " + str(Uloop2) + " " + str(Uloop3) + " " + str(Uloop4) \
                  + " " + str(Cloop1) + " " + str(Cloop2) + " " + str(Cloop3) + " " + str(Cloop4) \
                  + " " + str(Gloop1) + " " + str(Gloop2) + " " + str(Gloop3) + " " + str(Gloop4) \
                  + " " + str(l1l3) + " " + str(l2l4) + " " + str(l1) + " " + str(l2) + " " + str(l3) \
                  + " " + str(l4) \
                  + " " + str(energy1) + " " + str(energy2) + " " + str(energy3) + " " + str(energy4) \
                  + "\n"
        func_lib.writeToDisk(feature, "../data/4wj_feature.txt")

        # get_wcpair(line, "../../dataSet/4wj_wc_1.txt", seq, num1, num2, num3,num4, loop1, loop2, loop3,loop4)


if __name__ == '__main__':
    main()
