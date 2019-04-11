import matplotlib
import matplotlib.pyplot as plt
import numpy as np


'''
统计三分环和四分支的loop区的长度的分布图
'''

def loop_len(arr):   ### 将列表中的每个元素的个数以字典中键值对存储
    ll = []
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)

    #mydict_new = dict(zip(result.values(), result.keys())) # 字典的键值对反转
    #ll = sorted(mydict_new.items(), key=lambda x: x[0], reverse=True)

    return result


def loop_line(file1,file2):  ### 将每个多分支的loop区的长度写入列表中

    arr = []
    for line in open(file1):
        tmp = line.strip("").replace("\n","").split(" ")
        loop1 = tmp[1]
        loop2 = tmp[2]
        loop3 = tmp[3]
        arr.append(loop1)
        arr.append(loop2)
        arr.append(loop3)

    for line in open(file2):
        tmp = line.strip("").replace("\n", "").split(" ")
        loop1 = tmp[1]
        loop2 = tmp[2]
        loop3 = tmp[3]
        loop4 = tmp[4]
        arr.append(loop1)
        arr.append(loop2)
        arr.append(loop3)
        arr.append(loop4)

    return  arr

def draw_bar(x_list,y_list):   ### 条形图绘制  输入两个列表
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    x = range(len(x_list))
    rect = plt.bar(left=x, height= y_list, width=0.4, alpha = 0.8, color='red', label = 'loops')
    plt.ylim(0,2630)
    plt.xlim(0,50)
    plt.ylabel("count")

    plt.xticks([index + 0.2 for index in x], x_list)
    plt.xlabel("loop长度")
    plt.title("三分支环和四分支环不同loop长度数量统计")
    plt.legend()

    for rect in rect:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, int(height), ha="center", va="bottom")
    plt.show()

def dict_list(dict):    ## 字典中的key,value按升序排序，并储存在两个列表中
    lis = []
    key = list(dict)
    key = list(map(int, key))  # 字符串转换成整数
    x = np.array(key)
    lis = np.argsort(x)  # 提取将x按从大到小排序对应的索引
    key.sort()

    #i = 0
    newvalue= []
    value = list(dict.values())
    for line in lis:
        newvalue.append(int(value[line]))
        #i = i + 1
    print(newvalue)
    return key,newvalue

def looplen(file1,file2):
    dict = {}
    x_list = []
    y_list = []
    dict = loop_len(loop_line(file1,file2))
    x_list,y_list = dict_list(dict)
    draw_bar(x_list, y_list)

def main():
    looplen("3WJ/feature.txt", "4WJ/feature.txt")
if __name__ == '__main__':
    main()