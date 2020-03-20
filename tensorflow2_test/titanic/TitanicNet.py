# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
#   Copyright (C) 2020 liaozhimingandy@qq.com Ltd. All Rights Reserved.
#
#   Editor      : PyCharm
#   Project     : andy
#   File Name   : TitanicNet.py	
#   Author      : liaozhimingandy@qq.com
#   Created Date: 2020-01-14 9:30
#   Description : 泰塔尼克数据模型训练及预测;属于根据多个特征值进行对数据进行预测;
#
# ======================================================================

from __future__ import absolute_import, division, print_function, unicode_literals

import os

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn import preprocessing
from tensorflow import keras

from IBaseNet import IBaseNet

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
assert tf.__version__.startswith('2.')

# 关闭gpu转使用cpu,判断gpu是否可用
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# gpu_ok = tf.test.is_gpu_available()
# print(gpu_ok)


class TitanicNet(IBaseNet):

    def preprocess_data(self, *args, **kwargs):
        file_path = "titanic.xlsx"
        data_frame = pd.read_excel(file_path)

        # print(data_frame.describe())
        cols = [
            'survived', 'pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'body', 'embarked'
        ]
        data_frame = data_frame[cols]
        # 查看空值的列统计
        # print(data_frame.isnull().sum())

        ndarray = TitanicNet.preprocessing(data_frame=data_frame)

        features = ndarray[:, 1:]
        label = ndarray[:, 0]

        return features, label

    @staticmethod
    def preprocessing(data_frame):
        # 用平均值填充空值
        for val in ('fare', 'body', 'age'):
            # inplace = True：不创建新的对象，直接对原始对象进行修改；
            # inplace = False：对数据进行修改，创建并返回新的对象承载其修改结果。
            data_frame[val].replace(np.nan, 0, inplace=True)
            data_frame[val].replace(np.inf, 0, inplace=True)
            data_frame[val] = data_frame[val].fillna(data_frame[val].mean())

        # 类别列数据处理;将字符类别转换成数字类型数据
        data_frame = TitanicNet.deal_nan_inf(data_frame, index="sex", label={'female': 0, 'male': 1}, _type=int)
        data_frame = TitanicNet.deal_nan_inf(data_frame, index="embarked", label={'S': 1, 'C': 2, 'Q': 3, 'N': 0},
                                             _type=int, default="N")

        # 查看空值的列统计
        # print(data_frame.isnull().sum())
        # print(data_frame[168: 175])
        # data_frame.to_excel("tmp.xlsx", index=False)

        # 将data_frame总能够确定范围的列数据转成one-hot编码
        x_one_hot_df = pd.get_dummies(data=data_frame, columns=['embarked'])
        ndarray = x_one_hot_df.values

        # 将所有特征列数值转成[0, 1]范围,归一处理
        minmax_scale = preprocessing.MinMaxScaler(feature_range=(0, 1))
        scaled_features = minmax_scale.fit_transform(ndarray)

        return scaled_features

    @staticmethod
    def deal_nan_inf(data_frame, index, label: dict, _type, default='N'):
        assert isinstance(data_frame, pd.core.frame.DataFrame)
        data_frame[index] = data_frame[index].fillna(default)
        # inplace = True：不创建新的对象，直接对原始对象进行修改；
        # inplace = False：对数据进行修改，创建并返回新的对象承载其修改结果。
        data_frame[index].replace(np.nan, 0, inplace=True)
        data_frame[index].replace(np.inf, 0, inplace=True)
        # 检查是否字典遗漏
        # print(data_frame[(data_frame['embarked'] != 'S') & (data_frame['embarked'] != 'C') & (data_frame['embarked'] != 'Z')][index])
        data_frame[index] = data_frame[index].map(label).astype(_type)

        return data_frame

    def batch_dataset(self, x, y, *args, **kwargs):
        pass

    def compile_model(self, *args, **kwargs):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation=keras.activations.relu, name="h0"),
            tf.keras.layers.Dense(64, activation=keras.activations.relu, name="h1"),
            # 关闭 25% 的神经元
            tf.keras.layers.Dropout(0.25),
            tf.keras.layers.Dense(32, activation=keras.activations.relu, name="h2"),
            tf.keras.layers.Dense(1, activation=keras.activations.sigmoid, name="output")
        ])

        # 损失函数请使用:binary_crossentropy
        model.compile(loss=keras.losses.binary_crossentropy, optimizer=keras.optimizers.Adam(),
                      metrics=[keras.metrics.SparseCategoricalAccuracy()])

        return model

    def callbacks(self, *args, **kwargs):
        pass

    def train(self, model, *args, **kwargs):
        return model.fit(x=kwargs.get('x'), y=kwargs.get('y'), batch_size=128,
                         epochs=10, validation_split=0.2, verbose=2)

    def evaluate(self, model, x, y):
        pass

    def predict(self, model, x):
        pass

    def save(self, model, *args, **kwargs):
        pass

    def load(self, file_path):
        pass

    def main(self):
        pass


def main():
    t = TitanicNet()
    features, label = t.preprocess_data()
    # print(label)
    model = t.compile_model()
    # model.fit(x=features, y=label)
    history = t.train(model=model, x=features, y=label)
    print(history)

    Jack = pd.Series([1, 'Jack', 3, 'male', 23, 1, 0, 5.000, '', 'S'])
    Rose = pd.Series([0, 'Rose', 1, 'female', 20, 1, 0, 100.000, '', 'C'])

    JR_df = pd.DataFrame([list(Jack), list(Rose)],
                         columns=[
                             'survived', 'name', 'pclass', 'sex', 'age', 'sibsp',
                             'parch', 'fare', 'body', 'embarked'
                         ])

    # 将空格使用nan替换
    JR_df.replace(to_replace=r'^\s*$', value=np.nan, regex=True, inplace=True)
    file_path = "titanic.xlsx"
    data_frame = pd.read_excel(file_path)

    df = data_frame[['survived', 'name', 'pclass', 'sex', 'age', 'sibsp',
                     'parch', 'fare', 'body', 'embarked']]
    df = pd.concat([df, JR_df])
    # 剔除不需要的列
    JR_df = JR_df.drop(['name', 'survived'], axis=1)

    cols = [
        'pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'body', 'embarked'
    ]
    data_frame = data_frame[cols]
    # 将需要预测的数据与原数据进行拼接进行一起预测;弥补数据不足,导致数据维度不足
    all_df = pd.concat([data_frame, JR_df])
    pred_jr_df = TitanicNet.preprocessing(data_frame=all_df)

    pre = model.predict(pred_jr_df)
    # 将预测结果和原数据进行拼接,方便对照
    df.insert(len(df.columns), 'probability', pre)
    print(df[(df['name'] == 'Jack') & (df['probability'] > 0.1)])


def PreprocessData(raw_df):
    df = raw_df.drop(['name'], axis=1)
    age_mean = df['age'].mean()
    df['age'] = df['age'].fillna(age_mean)
    fare_mean = df['fare'].mean()
    df['fare'] = df['fare'].fillna(age_mean)
    df['sex'] = df['sex'].map({'female': 0, 'male': 1}).astype(int)
    x_Onehot_df = pd.get_dummies(data=df, columns=['embarked'])

    ndarray = x_Onehot_df.values
    Features = ndarray[:, 1:]
    Label = ndarray[:, 0]

    minmax_scale = preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaledFeatures = minmax_scale.fit_transform(Features)

    return scaledFeatures, Label


def test():
    file_path = "titanic.xlsx"
    all_df = pd.read_excel(file_path)
    cols = [
        'survived', 'name', 'pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked'
    ]
    all_df = all_df[cols]
    print(all_df, all_df[:2])
    df = all_df.drop(['name'], axis=1)
    print(all_df.isnull().sum())
    age_mean = df['age'].mean()
    df['age'] = df['age'].fillna(age_mean)
    fare_mean = df['fare'].mean()
    df['fare'] = df['fare'].fillna(fare_mean)
    df['sex'] = df['sex'].map({'female': 0, 'male': 1}).astype(int)
    x_Onehot_df = pd.get_dummies(data=df, columns=['embarked'])
    print(x_Onehot_df[:2], x_Onehot_df.isnull().sum())
    ndarray = x_Onehot_df.values
    print(ndarray[:2], ndarray.shape)
    Label = ndarray[:, 0]
    Features = ndarray[:, 1:]

    minmax_Scale = preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaledFeatures = minmax_Scale.fit_transform(Features)
    msk = np.random.rand(len(all_df)) < 0.8
    print(f"msk:{msk}")
    train_df = all_df[msk]
    test_df = all_df[msk]
    print(train_df)
    train_Features, train_Label = PreprocessData(train_df)
    test_Features, test_Label = PreprocessData(test_df)
    print(train_Features)
    model = tf.keras.Sequential()
    model.add(
        tf.keras.layers.Dense(units=40,
                              input_dim=9,
                              kernel_initializer='uniform',
                              activation='relu'))

    model.add(tf.keras.layers.Dense(units=30, kernel_initializer='uniform', activation='relu'))
    model.add(tf.keras.layers.Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    train_history = model.fit(x=train_Features,
                              y=train_Label,
                              validation_split=0.1,
                              batch_size=30,
                              epochs=10,
                              verbose=2)

    scores = model.evaluate(x=test_Features, y=test_Label)

    Jack = pd.Series([0, 'Jack', 3, 'male', 23, 1, 0, 5.000, 'S'])
    Rose = pd.Series([1, 'Rose', 1, 'female', 20, 1, 0, 100.000, 'S'])

    JR_df = pd.DataFrame([list(Jack), list(Rose)],
                         columns=[
                             'survived', 'name', 'pclass', 'sex', 'age', 'sibsp',
                             'parch', 'fare', 'embarked'
                         ])

    all_df = pd.concat([all_df, JR_df])
    print(all_df[2:])
    all_Features, Label = PreprocessData(all_df)

    all_probability = model.predict(all_Features)
    print(all_probability[:10])
    pd2 = all_df
    pd2.insert(len(all_df.columns),
               'probability', all_probability)
    print(pd2[(pd2['survived'] == 1) & (pd2['probability'] > 0.9)])


if __name__ == "__main__":
    from Timer import Timer

    with Timer.timer():
        main()
        # test()
