# -*- coding:utf-8 -*-
import re
import sys

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder

sys.path.append("../../../CommonTool")
import func_lib


def dealdate(file):
    a1 = 0
    a2 = 0
    a3 = 0
    a4 = 0
    a5 = 0
    lis = []
    for line in open("feature.txt"):

        line = line.strip().split(" ")
        f1 = line[0]
        angle = line[-1]
        angle = int(float(angle) // 36)
        if angle == 0:
            a1 += 1
        elif angle == 1:
            a2 += 1
        elif angle == 2:
            a3 += 1
        elif angle == 3:
            a4 += 1
        elif angle == 4:
            a5 += 1
        ss = line[0] + "," + line[1] + "," + line[2] + "," + line[3] + "," + line[4] + "," + line[5] + "," \
             + line[6] + "," + line[7] + "," + str(angle) + "\n"
        # func_lib.writeToDisk(ss, "angleFeature.txt")
    lis.append(a1)
    lis.append(a2)
    lis.append(a3)
    lis.append(a4)
    lis.append(a5)
    print(lis)


# define model structure
def baseline_model():
    model = Sequential()
    model.add(Dense(output_dim=20, input_dim=8, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim=5, input_dim=20, activation='softmax'))
    # Compile model 损失函数：高效Adam梯度下降优化算法
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def predict(file):
    # fix random seed for reproducibility
    seed = 7
    np.random.seed(seed)

    # load dataset
    dataframe = pd.read_csv("angleFeature.csv", header=None)
    dataset = dataframe.values
    X = dataset[:, 0:8].astype(float)
    Y = dataset[:, 8]

    # encode class values as integers
    encoder = LabelEncoder()  # 字符串编码为整数
    encoded_Y = encoder.fit_transform(Y)
    # convert integers to dummy variables (one hot encoding)
    dummy_y = np_utils.to_categorical(encoded_Y)  # 整数转换成热编码

    # estimator = KerasClassifier(build_fn=baseline_model, nb_epoch=200, batch_size=5)
    estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)

    # splitting data into training set and test set. If random_state is set to an integer, the split datasets are fixed.
    X_train, X_test, Y_train, Y_test = train_test_split(X, dummy_y, test_size=0.2, random_state=0)
    estimator.fit(X_train, Y_train)

    # make predictions
    pred = estimator.predict(X_test)

    # inverse numeric variables to initial categorical labels
    init_lables = encoder.inverse_transform(pred)

    # k-fold cross-validate
    seed = 42
    np.random.seed(seed)
    kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
    results = cross_val_score(estimator, X, dummy_y, cv=kfold)
    print("Baseline: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))

def main():
    #dealdate("feature.txt")
    predict("angleFeature.csv")


if __name__ == '__main__':
    main()
