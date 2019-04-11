# _*_coding:utf-8_*_

"""
将三分支和四分支中的角度全部归为相邻两个螺旋之间的角度的预测
"""

import sys

sys.path.append('../code/')
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
    for line in open("3WJ/feature_wc_1.txt"):
        line = line.strip("").split(" ")
        name = line[0]
        helix1 = line[1] + " " + line[2] + " " + line[3] + " " + line[4] + " " + line[7] + \
                 " " + line[10] + " " + line[13] + " " + line[16]
        helix2 = line[1] + " " + line[2] + " " + line[3] + " " + line[5] + " " + line[8] + \
                 " " + line[11] + " " + line[14] + " " + line[17]
        helix3 = (line[1] + " " + line[2] + " " + line[3] + " " + line[6] + " " + line[9] + \
                  " " + line[12] + " " + line[15] + " "+  line[18]).strip()
        angle1, angle2, angle3 = findangle_3(name, "3WJ/3wjangle.txt")
        helix1 = helix1 + " " + str(angle1) + "\n"
        helix2 = helix2 + " " + str(angle2) + "\n"
        helix3 = helix3 + " " + str(angle3) + "\n"
        func_lib.writeToDisk(helix1, "feature.txt")
        func_lib.writeToDisk(helix2, "feature.txt")
        func_lib.writeToDisk(helix3, "feature.txt")

    for line in open("4WJ/feature_wc_1.txt"):
        line = line.strip("").split(" ")
        name = line[0]
        helix1 = line[1] + " " + line[2] + " " + line[4] + " " + line[5] + " " + line[9] + " " + \
                 line[13] + " " + line[17] + " " + line[21]
        helix2 = line[1] + " " + line[2] + " " + line[3] + " " + line[6] + " " + line[10] + " " + \
                 line[14] + " " + line[18] + " " + line[22]
        helix3 = line[2] + " " + line[3] + " " + line[4] + " " + line[7] + " " + line[11] + " " + \
                 line[15] + " " + line[19] + " " + line[23]
        helix4 = (line[1] + " " + line[3] + " " + line[4] + " " + line[8] + " " + line[12] + " " + \
                  line[16] + " " + line[20] + " " + line[24]).strip()

        angle1, angle2, angle3, angle4 = findangle_4(name, "4WJ/4wjangle.txt")
        helix1 = helix1 + " " + str(angle1) + "\n"
        helix2 = helix2 + " " + str(angle2) + "\n"
        helix3 = helix3 + " " + str(angle3) + "\n"
        helix4 = helix4 + " " + str(angle4) + "\n"
        func_lib.writeToDisk(helix1, "feature.txt")
        func_lib.writeToDisk(helix2, "feature.txt")
        func_lib.writeToDisk(helix3, "feature.txt")
        func_lib.writeToDisk(helix4, "feature.txt")


if __name__ == '__main__':
    main()
