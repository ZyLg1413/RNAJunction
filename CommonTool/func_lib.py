# _*_coding:utf-8_*_

'''
merge_file   将两个有相同行的文件合并为一个文件，file1放在左边列，file2放到右边列
'''
import itertools


def merge_file(file1, file2, file3):
    with open(file1) as f:
        txt1 = [r.rstrip("\n") for r in f.readlines()]
    with open(file2) as f:
        txt2 = [r.rstrip("\n") for r in f.readlines()]

    result = itertools.zip_longest(txt1, txt2, fillvalue='')
    # [print(r) for r in result]

    with open(file3, 'w') as f:
        [f.write(' '.join(r) + "\n") for r in result]


### 将字符串str写入文件file
def writeToDisk(str, file):
    fp = open(file, "a")
    fp.write(str)
    fp.close()


### 列表list写入文件并换行
def list_file(lis, file):
    fp = open(file, 'a')
    for line in lis:
        fp.write(line + '\n')
    fp.close()


def plot_figure():
    import matplotlib.pyplot as plt
    import numpy as np
    # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
    plt.figure(figsize=(8, 6), dpi=80)
    # 再创建一个规格为 1 x 1 的子图
    plt.subplot(1, 1, 1)
    # 柱子总数
    N = 6
    # 包含每个柱子对应值的序列
    values = (25, 32, 34, 20, 41, 50)
    # 包含每个柱子下标的序列
    index = np.arange(N)
    # 柱子的宽度
    width = 0.35
    # 绘制柱状图, 每根柱子的颜色为紫罗兰色
    p2 = plt.bar(index, values, width, label="rainfall", color="#87CEFA")
    # 设置横轴标签
    plt.xlabel('Months')
    # 设置纵轴标签
    plt.ylabel('rainfall (mm)')
    # 添加标题
    plt.title('Monthly average rainfall')
    # 添加纵横轴的刻度
    plt.xticks(index, ('Jan', 'Fub', 'Mar', 'Apr', 'May', 'Jun'))
    plt.yticks(np.arange(0, 81, 10))
    # 添加图例
    plt.legend(loc="upper right")
    plt.show()


## 根据列表数据画柱状图
import numpy as np
import pylab
import matplotlib.pyplot as plt


def list_bar(list1, list2, list3):
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    skeresult = [0.9009584664536742, 0.9585987261146497, 0.9555555555555556, 0.8575949367088608, 0.945859872611465,
                 0.9741100323624595, 0.9367088607594937, 0.9240506329113924, 0.9588607594936709, 0.9810126582278481,
                 0.9648562300319489]
    '''rgbresult = [0.9201277955271565, 0.9936305732484076, 0.9746031746031746, 0.9082278481012658, 0.9522292993630573,
                 0.9838187702265372, 0.9651898734177216, 0.939873417721519, 0.9746835443037974, 0.9968354430379747,
                 0.9968051118210862]
    fusionresult = [0.964856, 1.0, 0.993650, 0.977848, 0.974522, 0.993527, 0.984177, 0.971518, 0.990506, 1.0, 0.993610]
    '''
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, *height, '%s' % float(height))

    name = ['punch', 'kick', 'push', 'pat', 'point', 'hug', 'pass', 'pocket', 'handshake', 'toward', 'away']
    total_width, n = 0.6, 3
    width = total_width / n

    a = plt.bar(x, skeresult, width=width, label='ske', fc='y')
    for i in range(len(x)):
        x[i] = x[i] + width
    '''
    b = plt.bar(x, rgbresult, width=width, label='rgb', tick_label=name, fc='g')
    for i in range(len(x)):
        x[i] = x[i] + width
    c = plt.bar(x, fusionresult, width=width, label='fusion', fc='r')'''

    plt.xlabel('class')
    plt.ylabel('acc')
    plt.title('NTUtp Classification Accuracy')
    plt.xticks(rotation=45)
    plt.xlim(x[0] - 0.5, x[i] + 0.1)
    plt.ylim(0.85, 1.0)
    plt.savefig("NTUtpAccuracy.png")
    plt.show()
