'''
由于这部分工作是统计的多分支环相邻两两螺旋之间的角度问题
所以对于四分支环我们对于每个多分支环只统计了四个相邻的螺旋角度

'''
import math
import os
import sys
sys.path.append("../../code/")
import func_lib

def pol_Rec(a,b): # 极坐标转换成对应的直角坐标x、y、z

    x = math.sin(a) * math.cos(b)
    y = math.sin(a)* math.sin(b)
    z = math.cos(a)
    return x, y, z

def cal_Angle(x1, y1, z1, x2, y2, z2):

    dot_pro = x1 * x2 + y1 * y2 + z1 * z2
    mode = math.sqrt(math.pow(x1, 2) + math.pow(y1, 2) + math.pow(z1, 2)) * math.sqrt(
        math.pow(x2, 2) + math.pow(y2, 2) + math.pow(z2, 2))
    return math.acos(dot_pro / mode) * 360 / (2 * math.pi)

def helix_Angle(file):

    xyz = []
    Angle = []
    for line in open(file):
        line = line.strip("").split(" ")

        sita1 = float(line[0].split(":")[0])
        arfa1 = float(line[0].split(":")[1])
        x1,y1,z1 = pol_Rec(sita1, arfa1)

        sita2 = float(line[1].split(":")[0])
        arfa2 = float(line[1].split(":")[1])
        x2,y2,z2 = pol_Rec(sita2, arfa2)

        sita3 = float(line[2].split(":")[0])
        arfa3 = float(line[2].split(":")[1])
        x3,y3,z3 = pol_Rec(sita3, arfa3)

        sita4 = float(line[3].split(":")[0])
        arfa4 = float(line[3].split(":")[1])
        x4,y4,z4 = pol_Rec(sita4, arfa4)

        xyz.append(x1)
        xyz.append(y1)
        xyz.append(z1)


        xyz.append(x2)
        xyz.append(y2)
        xyz.append(z2)

        xyz.append(x3)
        xyz.append(y3)
        xyz.append(z3)

        xyz.append(x4)
        xyz.append(y4)
        xyz.append(z4)

        angle1 = cal_Angle(xyz[0], xyz[1], xyz[2], xyz[3], xyz[4], xyz[5])
        angle2 = cal_Angle(xyz[3], xyz[4], xyz[5], xyz[6], xyz[7], xyz[8])
        angle3 = cal_Angle(xyz[6], xyz[7], xyz[8], xyz[9], xyz[10], xyz[11])
        angle4 = cal_Angle(xyz[0], xyz[1], xyz[3], xyz[9], xyz[10], xyz[11])
        angles = str(angle1) + " " + str(angle2) + " " + str(angle3) + " " + str(angle4)
        Angle.append(angles)
        xyz.clear()

    return  Angle

def list_file(list,file):
    fp = open(file, 'w')
    for line in list:
        fp.write(line+'\n')
    fp.close()



def main():

    allAngle = []
    allAngle = helix_Angle("../../dataSet/4wj_polcor.txt")
    #print(allAngle)
    list_file(allAngle,'tmp.txt')
    fp = open("4wjangle.txt", 'w')
    func_lib.merge_file("../../dataSet/4wjpdbName.txt", "tmp.txt", "4wjangle.txt")
    os.remove("tmp.txt")
    fp.close()


if __name__ == '__main__':
    main()