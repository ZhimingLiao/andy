# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
#   Copyright (C) 2020 liaozhimingandy@qq.com Ltd. All Rights Reserved.
#
#   Editor      : PyCharm
#   Project     : andy
#   File Name   : HeartNet.py	
#   Author      : liaozhimingandy@qq.com
#   Created Date: 2020-01-13 11:11
#   Description : 心脏病模型
#
# ======================================================================

from __future__ import absolute_import, division, print_function, unicode_literals

import pandas as pd
import tensorflow as tf
from tensorflow.compat.v2 import feature_column
from tensorflow.keras import layers

from IBaseNet import IBaseNet


# 将数组或矩阵拆分为随机的训练子集和测试子集


class HeartNet(IBaseNet):

    def preprocess_data(self, input_data):
        data_frame = pd.read_csv(input_data)
        # print(data_frame)
        # print(data_frame.describe())
        # print(data_frame.shape)
        # print(data_frame.columns)
        # print(data_frame.isnull().sum())
        # data_frame.dropna(axis=0, how='all')
        # print(data_frame.shape)
        # data_frame.replace('normal', 3, inplace=True)
        # data_frame.replace('fixed', 6, inplace=True)
        # data_frame.replace('reversible', 7, inplace=True)
        # data_frame['chol'].median()
        # data_frame.reset_index()

        # 训练、验证、测试三个数据集都转换成Dataset类型，其中训练集需要重新排序
        train_ds = self.__df_to_dataset(data_frame)
        val_ds = self.__df_to_dataset(data_frame, shuffle=False)
        test_ds = self.__df_to_dataset(data_frame, shuffle=False)
        return train_ds, val_ds, test_ds

    def __df_to_dataset(self, data_frame, shuffle=True, batch_size=32):
        data_frame = data_frame.copy()
        labels = data_frame.pop('target')
        ds = tf.data.Dataset.from_tensor_slices((dict(data_frame), labels))
        if shuffle:
            ds = ds.shuffle(buffer_size=len(data_frame))
        ds = ds.batch(batch_size).repeat()
        return ds

    def batch_dataset(self, x, y, train_pre=0.7, valid_pre=0.2, test_pre=0.1):
        pass

    def compile_model(self, *args, **kwargs):
        model = tf.keras.Sequential([
            tf.keras.layers.DenseFeatures(kwargs.get("feature_columns")),
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'], verbose=2)

        return model

    def callbacks(self, log_dir=None, file_name=None):
        pass

    def train(self, model, *args, **kwargs):
        return

    def evaluate(self, model, x, y):
        pass

    def predict(self, model, pre_data):
        pass

    def save(self, model, file_path=None, file_name=None):
        pass

    def load(self, file_name):
        pass

    def main(self):
        # 此处定义基本操作步骤;根据需要选择非必选步骤
        # *1.得到数据集, 数据集打乱处理;返回numpy, preprocess_data
        # *2.分批得到训练, 验证, 测试数据集, batch_dataset
        # 3.得到已编译好的模型, compile_model
        # 4.设置回调函数, callback
        # 5.模型训练, 返回训练好的模型, train
        # 6.模型评估, evaluate
        # 7.模型预测, predict
        # 8.模型保存, save
        # 9.模型加载, load
        file_path = "heart.csv"
        batch_size = 32
        feature_columns = []
        train_ds, val_ds, test_ds = self.preprocess_data(input_data=file_path)
        # 用于保存所需的数据列
        feature_columns = []

        # 根据字段名，添加所需的数据列
        for header in ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'slope', 'ca']:
            # vocabulary = dftrain[feature_name].unique()
            feature_columns.append(feature_column.numeric_column(header))

        # 取出年龄数据
        age = feature_column.numeric_column("age")
        # 按照18-25/25-30/30-35/.../60-65为年龄分段，最后形成one-hot编码
        age_buckets = feature_column.bucketized_column(age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])
        # 数据段作为一个新参量添加到数据集
        feature_columns.append(age_buckets)

        # 获取thal字段原始数据
        thal = feature_column.categorical_column_with_vocabulary_list(
            'thal', ['fixed', 'normal', 'reversible'])
        # 做one-hot编码
        thal_one_hot = feature_column.indicator_column(thal)
        # 作为新的数据列添加
        feature_columns.append(thal_one_hot)

        # 将thal嵌入8维空间做向量化
        thal_embedding = feature_column.embedding_column(thal, dimension=8)
        feature_columns.append(thal_embedding)

        # 把年龄段和thal字段作为关联属性加入新列
        crossed_feature = feature_column.crossed_column([age_buckets, thal], hash_bucket_size=1000)
        crossed_feature = feature_column.indicator_column(crossed_feature)
        feature_columns.append(crossed_feature)

        model = self.compile_model(feature_columns=feature_columns)
        # 样本数量steps_per_epoch*batch_size;validation_split: 0 和 1 之间的浮点数。用作验证集的训练数据的比例
        model.fit(train_ds, epochs=5, validation_data=val_ds, steps_per_epoch=300 // batch_size, validation_steps=1)

        # # 训练、验证、测试三个数据集都转换成Dataset类型，其中训练集需要重新排序
        # train_ds = self.__df_to_dataset(train, shuffle=True, batch_size=batch_size)
        # val_ds = self.__df_to_dataset(val, shuffle=False, batch_size=batch_size)
        # test_ds = self.__df_to_dataset(test, shuffle=False, batch_size=batch_size)
        #
        # for feature_batch, label_batch in train_ds:
        #     print('所有特征:', list(feature_batch.keys()))
        #     print('其中年龄:', feature_batch['age'])
        #     print('目标值:', label_batch)
        #     break

        # 评估
        test_loss, test_acc = model.evaluate(test_ds, steps=1)
        print(test_acc)
        # 预测
        pre = model.predict(test_ds, steps=1)
        print(pre.shape, pre)
        for d in test_ds:
            print(d[0], d[1])
            break


def main():
    net = HeartNet()
    net.main()


if __name__ == "__main__":
    from Timer import Timer

    with Timer.timer():
        main()
