import numpy as np
import re
from sklearn import ensemble
from sklearn.model_selection import StratifiedKFold, KFold
import matplotlib.pyplot as plt

'''
dict1 = dict(zip(['100', '010', '001', '011', '110', '101'], \
                 ([0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0], \
                  [0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0])))
dict2 = dict(zip('ABC', ([0, 0, 1], [0, 1, 0], [1, 0, 0])))'''

dict1 = dict(zip(['1000', '0100', '0010', '0001', '1100', '0110', '0011'], \
                 [0, 1, 2, 3, 4, 5, 6]))
dict2 = dict(zip('ABC', [0, 1, 2]))


def stack_map(hel_stack):
    return dict1[hel_stack]


def read_data_stack(datafile):
    data = []
    with open(datafile, 'r') as f:
        for line in f:
            arr = re.split(r' +', line.strip('\n'))
            pdb, loop1, loop2, loop3, loop4, Aloop1, Aloop2, Aloop3, Aloop4, \
            Uloop1, Uloop2, Uloop3, Uloop4, Cloop1, Cloop2, Cloop3, Cloop4, Gloop1, Gloop2, Gloop3, Gloop4, \
            l1l3, l2l4, l1, l2, l3, l4, energy1, energy2, energy3, energy4, \
            hel_stack = arr
            data.append(
                [stack_map(hel_stack), float(loop1), float(loop2), float(loop3), float(loop4), \
                 float(Aloop1), float(Aloop2), float(Aloop3), float(Aloop4), \
                 float(Uloop1), float(Uloop2), float(Uloop3), float(Uloop4), \
                 float(Cloop1), float(Cloop2), float(Cloop3), float(Cloop4), \
                 float(Gloop1), float(Gloop2), float(Gloop3), float(Gloop4), \
                 float(l1l3), float(l2l4), \
                 float(l1), float(l2), float(l3), float(l4), \
                 float(energy1), float(energy2), float(energy3), float(energy4) \
                 ])

    return data


def S_KFold(data_x, data_y, repeat):
    count = 0
    score_k = []
    score_avg = []
    while count < repeat:
        # model = ensemble.RandomForestClassifier(n_estimators=200,max_features=5)
        model = ensemble.RandomForestClassifier()
        scores = []
        kfold = KFold(n_splits=10)
        # kfold = StratifiedKFold(y=data_y, n_folds=10, random_state=1)  # n_folds参数设置为10份

        for train_index, test_index in kfold.split(data_x, data_y):
            model.fit(data_x[train_index], data_y[train_index])
            score = model.score(data_x[test_index], data_y[test_index])
            scores.append(score)
            print('准确度: %.3f' % (score), count)
        avg = np.mean(scores)  ####   求出每次十倍交叉验证评估的平均值
        score_k.append(avg)  ####   保留每次交叉验证的精度
        score_avg.append(np.mean(score_k))  ####   保留n次交叉验证的平均值
        count += 1

    return score_avg


def plot_K_4(repeat, score_avg):
    x = [i for i in range(1, repeat + 1)]
    y = score_avg
    plt.plot(x, y, "r-", linewidth=2, label="Coaxial-stacking")
    plt.legend(loc='lower right')
    plt.grid(True)  # 是否需要网格
    plt.xlabel("10-fold cross-validation repeats")
    plt.ylabel("Accuracy of 4WJ")
    plt.show()
    plt.savefig("../result/Accuracy_4.png")


def main():
    # 预测三分支环同轴预测精度（angle = 130）
    input_data = np.array(read_data_stack('../data/feature_4.txt'))
    np.random.shuffle(input_data)
    repeat = 500
    data_x = np.array([i for i in input_data[:, 1:]], dtype=np.float32)
    data_y = np.array([i for i in input_data[:, 0]], dtype=np.float32)
    score_avg = S_KFold(data_x, data_y, repeat)
    plot_K_4(repeat, score_avg)

    '''
    data_x1 = np.array([i for i in input_data[:, 1:5]], dtype=np.float32)
    data_x2 = np.array([i for i in input_data[:, 5:9]], dtype=np.float32)
    data_x3 = np.array([i for i in input_data[:, 9:13]], dtype=np.float32)
    data_x4 = np.array([i for i in input_data[:, 13:17]], dtype=np.float32)
    data_x5 = np.array([i for i in input_data[:, 17:21]], dtype=np.float32)
    data_x6 = np.array([i for i in input_data[:, 21:23]], dtype=np.float32)
    data_x7 = np.array([i for i in input_data[:, 23:27]], dtype=np.float32)
    data_x8 = np.array([i for i in input_data[:, 27:31]], dtype=np.float32)

    score = []
    list = [data_x1, data_x2, data_x3, data_x4, data_x5, data_x6, data_x7, data_x8]
    for line in list:
        score_avg = S_KFold(line, data_y, repeat)
        # print(score_avg)
        score.append(score_avg[-1])
    print(score)
    x_axis = ['looplen', 'Anum', 'Unum', 'Cnum', 'Gnum', 'min', 'loop\'', 'energy']
    plt.bar(range(len(score)), score, color='b', tick_label=x_axis)
    plt.ylabel('accuracy of 4wj')
    plt.show()'''

if __name__ == "__main__":
    main()
