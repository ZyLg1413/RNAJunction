import numpy as np
import re
from sklearn import ensemble, preprocessing
from sklearn.model_selection import StratifiedKFold, KFold
import matplotlib.pyplot as plt
from sklearn.ensemble import ExtraTreesClassifier


'''dict1 = dict(zip(['100', '010', '001', '011', '110', '101'], \
                 ([0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0], \
                  [0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0])))
dict1 = dict(zip(['100', '010', '001', '011', '110'], \
                 ([0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0], \
                  [0, 1, 0, 0, 0], [1, 0, 0, 0, 0])))'''

dict1 = dict(zip(['100', '010', '001', '011', '110','101'], \
                 [0, 1, 2, 3, 4, 5]))

def stack_map(hel_stack):
    return dict1[hel_stack]

def read_data_stack(datafile):
    data = []
    with open(datafile, 'r') as f:
        for line in f:
            arr = re.split(r' +', line.strip('\n'))
            pdb, loop1, loop2, loop3, Aloop1, Aloop2, Aloop3, \
            Uloop1, Uloop2, Uloop3, Cloop1, Cloop2, Cloop3, Gloop1, Gloop2, Gloop3, \
            l2l3, l1l3, l1l2, l1, l2, l3, energy1, energy2, energy3, \
            hel_stack = arr
            data.append(
                [stack_map(hel_stack), float(loop1), float(loop2), float(loop3), \
                 float(Aloop1), float(Aloop2), float(Aloop3), \
                 float(Uloop1), float(Uloop2), float(Uloop3), \
                 float(Cloop1), float(Cloop2), float(Cloop3), \
                 float(Gloop1), float(Gloop2), float(Gloop3), \
                 float(l2l3), float(l1l3), float(l1l2), \
                 float(l1), float(l2), float(l3), \
                 float(energy1), float(energy2), float(energy3), \
                 ])

    return data

def S_KFold(data_x, data_y, repeat):
    count = 0
    score_k = []
    score_avg = []
    while count < repeat:
        model = ensemble.RandomForestClassifier()
        scores = []

        kfold = KFold(n_splits=10, shuffle=True)

        for train_index, test_index in kfold.split(data_x, data_y):
            model.fit(data_x[train_index], data_y[train_index])
            score = model.score(data_x[test_index], data_y[test_index])
            scores.append(score)
            print('准确度: %.3f' % (score), count)
        '''
        kfold = StratifiedKFold(n_splits=10,random_state=0,shuffle=False)  # n_folds参数设置为10份
        for train_index, test_index in kfold.split(data_x, data_y):
            model.fit(data_x[train_index], data_y[train_index])
            score = model.score(data_x[test_index], data_y[test_index])
            scores.append(score)
            # print('准确度: %.3f' % (score), count)'''
        avg = np.mean(scores)  ####   求出每次十倍交叉验证评估的平均值
        score_k.append(avg)  ####   保留每次交叉验证的精度
        score_avg.append(np.mean(score_k))  ####   保留n次交叉验证的平均值
        count += 1

    return score_avg



def plot_K_3(repeat, score_avg):
    x = [i for i in range(1, repeat + 1)]
    y = score_avg
    plt.plot(x, y, "r-", linewidth=2, label="Coaxial-stacking")
    plt.legend(loc='lower right')
    plt.grid(True)  # 是否需要网格
    plt.xlabel("10-fold cross-validation repeats")
    plt.ylabel("Accuracy of 3WJ")
    plt.show()
    plt.savefig("../result/Accuracy_3.png")


def plot_import(X, Y):   ### 每一个特征的重要性
    # Build a forest and compute the feature importances
    forest = ExtraTreesClassifier(n_estimators=200,
                                  random_state=0)

    forest.fit(X, Y)
    importances = forest.feature_importances_

    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]
    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices],
            color="r", yerr=std[indices], align="center")
    plt.xticks(range(X.shape[1]), indices)
    plt.xlim([-1, X.shape[1]])
    plt.show()


def plot_bar():
    import matplotlib.pyplot as plt
    import numpy as np
    plt.figure(figsize=(8, 6), dpi=80)
    plt.subplot(1, 1, 1)
    N = 6
    values = (25, 32, 34, 20, 41, 50)
    index = np.arange(N)
    width = 0.35
    p2 = plt.bar(index, values, width, label="rainfall", color="#87CEFA")
    plt.xlabel('Months')
    plt.ylabel('rainfall (mm)')
    plt.title('Monthly average rainfall')
    plt.xticks(index, ('Jan', 'Fub', 'Mar', 'Apr', 'May', 'Jun'))
    plt.yticks(np.arange(0, 81, 10))
    plt.legend(loc="upper right")
    plt.show()


def main():
    # 预测三分支环同轴预测精度（angle = 130）
    input_data = np.array(read_data_stack('../data/feature_3.txt'))
    np.random.shuffle(input_data)
    repeat = 20
    data_x = np.array([i for i in input_data[:, 1:]], dtype=np.float32)
    data_y = np.array([i for i in input_data[:, 0]], dtype=np.float32)
    data_x = preprocessing.scale(data_x)

    ### 考察每类特征的重要性，总共有8类特征
    '''
    data_x1 = np.array([i for i in input_data[:, 1:4]], dtype=np.float32)
    data_x2 = np.array([i for i in input_data[:, 4:7]], dtype=np.float32)
    data_x3 = np.array([i for i in input_data[:, 7:10]], dtype=np.float32)
    data_x4 = np.array([i for i in input_data[:, 10:13]], dtype=np.float32)
    data_x5 = np.array([i for i in input_data[:, 13:16]], dtype=np.float32)
    data_x6 = np.array([i for i in input_data[:, 16:19]], dtype=np.float32)
    data_x7 = np.array([i for i in input_data[:, 19:22]], dtype=np.float32)
    data_x8 = np.array([i for i in input_data[:, 22:25]], dtype=np.float32)
    score = []
    list = [data_x1, data_x2, data_x3, data_x4, data_x5, data_x6, data_x7, data_x8]
    for line in list:
        score_avg = S_KFold(line, data_y, repeat)
        #print(score_avg)
        score.append(score_avg[-1])
    print(score)
    x_axis = ['looplen', 'Anum', 'Unum', 'Cnum', 'Gnum', 'min', 'loop\'','energy']
    plt.bar(range(len(score)), score, color='b', tick_label=x_axis)
    plt.ylabel('accuracy of 3wj')
    plt.show()'''


    score_avg = S_KFold(data_x, data_y, repeat)
    plot_K_3(repeat, score_avg)
    # plot_import(data_x, data_y)

if __name__ == "__main__":
    main()
