# _*_coding:utf-8_*_
'''
目的：根据不同的特征预测两个螺旋之间的角度
'''
import re
import numpy as np
from sklearn import ensemble
from sklearn.model_selection import StratifiedKFold, KFold
# from sklearn.cross_validation import StratifiedKFold
import matplotlib.pyplot as plt
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from sklearn import preprocessing


def read_data(datafile):
    data = []
    with open(datafile, 'r') as f:
        for line in f:
            arr = re.split(r' +', line.strip('\n'))
            loopl, loop, loopr, Anum, Unum, Cnum, Gnum, energy1, angle = arr

            # Angle = int(float(angle) // 20)  ### 十分类问题
            Angle = int(float(angle) // 36)  ### 五分类问题

            data.append([Angle, float(loopl), float(loop), float(loopr), float(Anum), float(Unum), float(Cnum), \
                         float(Gnum), float(energy1)])
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


def assessfeature(X, Y, featurename):  ### 评估每个特征的重要性
    from sklearn.cross_validation import cross_val_score, ShuffleSplit
    from sklearn.datasets import load_boston
    from sklearn.ensemble import RandomForestRegressor
    import numpy as np

    rf = RandomForestRegressor(n_estimators=20, max_depth=4)
    scores = []
    for i in range(X.shape[1]):
        score = cross_val_score(rf, X[:, i:i + 1], Y, scoring="r2",
                                cv=ShuffleSplit(len(X), 3, .3))
        scores.append((round(np.mean(score), 3), featurename[i]))
    print(sorted(scores, reverse=True))


def plot_import(X, y):
    # Build a forest and compute the feature importances
    forest = ExtraTreesClassifier(n_estimators=200,
                                  random_state=0)

    forest.fit(X, y)
    importances = forest.feature_importances_

    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]
    '''
    i = 0
    for line in indices:
        tmp = feature[int(line)]
        indices[i] = tmp
        i+=1
    print(indices)
    '''
    '''
    # Print the feature ranking
    print("Feature ranking:")

    for f in range(X.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
    '''
    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices],
            color="r", yerr=std[indices], align="center")
    # indices = ['energy', 'Gnum', 'Anum', 'Cnum', 'Unum', 'loop', 'l3', 'loopl', 'loopr',\
    #             'l1l3', 'l2l3', 'l2', 'l1l2','l1']
    plt.xticks(range(X.shape[1]), indices)
    plt.xlim([-1, X.shape[1]])
    plt.show()


def plot_K(repeat, score_avg1):
    x = [i for i in range(1, repeat + 1)]
    y1 = score_avg1
    plt.plot(x, y1, "r-", linewidth=2, label="Angle")
    # plt.plot(x, y1, 'r*', markersize=15, alpha=0.75)
    # plt.plot(x, y2, "b-", linewidth=2, label="Angle2")
    # plt.plot(x, y3, "y-", linewidth=2, label="Angle3")
    plt.legend(loc='lower right')
    plt.grid(True)  # 是否需要网格
    plt.xlabel("10-fold cross-validation repeats")
    plt.ylabel("Accuracy of Helix_Angle")
    plt.show()
    plt.savefig("Accuracy.png")


def main():
    input_data = np.array(read_data("../data/feature.txt"))
    np.random.shuffle(input_data)
    repeat = 50

    data_x = np.array([i for i in input_data[:, 1:]], dtype=np.float32)
    # data_x2 = np.array([i for i in input_data[:, -1]], dtype=np.float32)
    # data_x = np.hstack((data_x1, data_x2))
    data_y = np.array([i for i in input_data[:, 0]], dtype=np.float32)

    # 数据标准化
    data_x = preprocessing.scale(data_x)

    # encode class values as integers
    '''
    encoder = LabelEncoder()  # 字符串编码为整数
    encoded_Y = encoder.fit_transform(data_y)
    # convert integers to dummy variables (one hot encoding)
    data_y = np_utils.to_categorical(encoded_Y)  # 整数转换成热编码
    '''
    score = S_KFold(data_x, data_y, repeat)
    plot_K(repeat, score)

    plot_import(data_x, data_y)
    #### 评估每个特征的重要性
    # assessfeature(data_x, data_y, featurename)


if __name__ == '__main__':
    main()
