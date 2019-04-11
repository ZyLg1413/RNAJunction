import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

def getFeature_3(wj):
    count = 0
    A_num = 0
    U_num = 0
    C_num = 0
    G_num = 0
    for line in open(wj):
        # 最终保存结果的文件
        count += 1
        tmp = line.strip("").split(" ")[0]
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
                # 得到三个junction的碱基个数
        loop1 = index1 + 1 - num1 - num2
        loop2 = index2 + 1 - (index1 + 1) - num2 - num3
        loop3 = len(ss) - (index2 + 1) - num3 - num1
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
        # 寻找每个环区上面的碱基U的个数
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
        # 寻找每个环区上面的碱基C的个数

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

        #
        # 寻找每个环区上面的碱基G的个数
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

        A_num = A_num + Aloop1 + Aloop2 + Aloop3
        U_num = U_num + Uloop1 + Uloop2 + Uloop3
        C_num = C_num + Cloop1 + Cloop2 + Cloop3
        G_num = G_num + Gloop1 + Gloop2 + Gloop3

    return A_num, U_num, C_num, G_num
def getFeature_4(wj):
    count = 0
    A_num = 0
    U_num = 0
    C_num = 0
    G_num = 0
    for line in open(wj):
        # 最终保存结果的文件
        count += 1
        pdbName = line.strip("").split(" ")[0]
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


         # 得到四个junction的碱基个数
        loop1 = index1 + 1 - num1 - num2
        loop2 = index2 + 1 - (index1 + 1) - num2 - num3
        loop3 = index3 + 1 - (index2 + 1) - num3 - num4
        loop4 = len(ss) - (index3 + 1) - num4 - num1
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
                if seq[index3 + num4 + 1 + i] == 'A':
                            Aloop4 += 1

        # 寻找每个环区上面的碱基U的个数
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
                if seq[index3 + num4 + 1 + i] == 'U':
                    Uloop4 += 1
        # 寻找每个环区上面的碱基C的个数

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
                if seq[index3 + num4 + 1 + i] == 'C':
                    Cloop4 += 1
        # 寻找每个环区上面的碱基G的个数
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
                if seq[index3 + num4 + 1 + i] == 'G':
                    Gloop4 += 1

        A_num = A_num + Aloop1 + Aloop2 + Aloop3 + Aloop4
        U_num = U_num + Uloop1 + Uloop2 + Uloop3 + Uloop4
        C_num = C_num + Cloop1 + Cloop2 + Cloop3 + Cloop4
        G_num = G_num + Gloop1 + Gloop2 + Gloop3 + Gloop4

    return A_num, U_num, C_num, G_num



def main():
    A, U, C, G = getFeature_3("../dataSet/3wj_wc_1.txt")
    a, u, c, g = getFeature_4("../dataSet/4wj_wc_1.txt")
    #print(A, U, C, G,a, u, c, g)
    A_num = A + a
    U_num = U + u
    C_num = C + c
    G_num = G + g
    sum = A_num + U_num + C_num + G_num
    print(A_num/sum, U_num/sum, C_num/sum, G_num/sum)

    n_groups = 4
    means_men = (A_num, U_num, C_num, G_num)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = ax.bar(index, means_men, bar_width,
                    alpha=opacity, color='b',
                     error_kw=error_config)
    ax.set_xlabel('A,U,C,G')
    ax.set_ylabel('Count')
    #ax.set_title('Scores by group and gender')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('A', 'U', 'C', 'G'))
    ax.legend()

    fig.tight_layout()
    plt.show()



if __name__ == '__main__':
    main()
