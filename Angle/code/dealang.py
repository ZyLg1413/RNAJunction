#!/usr/bin/env python
# _*_coding:utf-8_*_


"""
将三分支和四分支中的角度全部归为相邻两个螺旋之间的角度的预测
"""

import sys

sys.path.append('../../CommonTool/')
import func_lib


def findangle_3(name, file):
    for line in open(file):
        if name == line.strip("").split(" ")[0]:
            angle1 = round(float(line.strip("").split(" ")[1]), 1)
            angle2 = round(float(line.strip("").split(" ")[2]), 1)
            angle3 = round(float(line.strip("").split(" ")[3]), 1)
    return angle1, angle2, angle3


def findangle_4(name, file):
    for line in open(file):
        if name == line.strip("").split(" ")[0]:
            angle1 = round(float(line.strip("").split(" ")[1]), 1)
            angle2 = round(float(line.strip("").split(" ")[2]), 1)
            angle3 = round(float(line.strip("").split(" ")[3]), 1)
            angle4 = round(float(line.strip("").split(" ")[4]), 1)
    return angle1, angle2, angle3, angle4


def main():
    ### 提取三分支环的部分特征
    for line in open("../data/3wj_feature.txt"):
        line = line.strip("").split(" ")
        name = line[0]
        helix1 = (line[1] + " " + line[2] + " " + line[3] + " " + line[4] + " " + line[7] + \
                  " " + line[10] + " " + line[13] + " " + line[22]).strip()
        helix2 = (line[1] + " " + line[2] + " " + line[3] + " " + line[5] + " " + line[8] + \
                  " " + line[11] + " " + line[14] + " " + line[23]).strip()
        helix3 = (line[1] + " " + line[2] + " " + line[3] + " " + line[6] + " " + line[9] + \
                  " " + line[12] + " " + line[15] + " " + line[24]).strip()
        angle1, angle2, angle3 = findangle_3(name, "../data/3wj_angle.txt")
        helix1 = helix1 + " " + str(angle1) + "\n"
        helix2 = helix2 + " " + str(angle2) + "\n"
        helix3 = helix3 + " " + str(angle3) + "\n"
        func_lib.writeToDisk(helix1, "../data/feature.txt")
        func_lib.writeToDisk(helix2, "../data/feature.txt")
        func_lib.writeToDisk(helix3, "../data/feature.txt")

    ### 提取四分支环的部分特征
    for line in open("../data/4wj_feature.txt"):
        line = line.strip("").split(" ")
        name = line[0]
        helix1 = (line[1] + " " + line[2] + " " + line[4] + " " + line[5] + " " + line[9] + " " + \
                  line[13] + " " + line[17] + " " + line[27]).strip()
        helix2 = (line[1] + " " + line[2] + " " + line[3] + " " + line[6] + " " + line[10] + " " + \
                  line[14] + " " + line[18] + " " + line[28]).strip()
        helix3 = (line[2] + " " + line[3] + " " + line[4] + " " + line[7] + " " + line[11] + " " + \
                  line[15] + " " + line[19] + " " + line[29]).strip()
        helix4 = (line[1] + " " + line[3] + " " + line[4] + " " + line[8] + " " + line[12] + " " + \
                  line[16] + " " + line[20] + " " + line[30]).strip()

        angle1, angle2, angle3, angle4 = findangle_4(name, "../data/4wj_angle.txt")
        helix1 = helix1 + " " + str(angle1) + "\n"
        helix2 = helix2 + " " + str(angle2) + "\n"
        helix3 = helix3 + " " + str(angle3) + "\n"
        helix4 = helix4 + " " + str(angle4) + "\n"
        func_lib.writeToDisk(helix1, "../data/feature.txt")
        func_lib.writeToDisk(helix2, "../data/feature.txt")
        func_lib.writeToDisk(helix3, "../data/feature.txt")
        func_lib.writeToDisk(helix4, "../data/feature.txt")


if __name__ == '__main__':
    main()
