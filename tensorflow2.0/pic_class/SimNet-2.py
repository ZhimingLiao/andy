# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
#   Copyright (C) 2020 liaozhimingandy@qq.com Ltd. All Rights Reserved.
#
#   Editor      : PyCharm
#   Project     : andy
#   File Name   : SimNet-2.py
#   Author      : liaozhimingandy@qq.com
#   Created Date: 2020-01-13 9:12
#   Description : 卷积神经网络训练,分类图片
#
# ======================================================================
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import pathlib
import random
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tqdm import tqdm

from IBaseNet import IBaseNet


class SimNet2(IBaseNet):
    def __init__(self):
        self._name = "SimNet-2"

    def __generate_paths_lable(self, dir_path: str, flag_random=True) -> tuple:
        assert len(dir_path) > 1
        root = pathlib.Path(dir_path)
        paths = [str(path) for path in list(root.glob("*/*"))]
        # 随机打乱数据
        if flag_random:
            random.shuffle(paths)
        label = sorted(item.name for item in root.glob('*/') if item.is_dir())
        index = dict((name, index) for index, name in enumerate(label))
        index_label = [index[pathlib.Path(path).parent.name] for path in paths]
        return paths, index_label, index

    def preprocess_data(self, input_data):
        x, y, names = self.__generate_paths_lable(dir_path=input_data)
        ds = tf.data.Dataset.from_tensor_slices((x, y))
        # 数据集预处理
        ds = ds.shuffle(128).map(self.__preprocess)

        # 转换成numpy对象
        np_ds_x = np.zeros([len(y), 28, 28, 1], dtype=np.float32)
        np_ds_y = np.zeros([len(y), ], dtype=np.uint8)

        with tqdm(total=len(y)) as pbar:
            i = 0
            pbar.set_description("样本处理进度")
            for a, b in ds:
                np_ds_x[i] = a
                np_ds_y[i] = b
                i += 1
                pbar.update(1)
            del i

        return np_ds_x, np_ds_y, names

    def batch_dataset(self, x, y, train_pre=0.7, valid_pre=0.2, test_pre=0.1):
        train_x, train_y = x[:int(len(y) * train_pre)], y[:int(len(y) * train_pre)]
        valid_x, valid_y = x[int(len(y) * train_pre): int(len(y) * (train_pre + valid_pre))], y[int(
            len(y) * train_pre): int(len(y) * (train_pre + valid_pre))]
        test_x, test_y = x[int(len(y) * (train_pre + valid_pre)):], y[(int(len(y) * (train_pre + valid_pre))):]

        return (train_x, train_y), (valid_x, valid_y), (test_x, test_y)

    def compile_model(self):
        """
        使用卷积神经网络进行训练
        :return: 已编译好的model
        """
        model = keras.models.Sequential([
            # 网格采用 32 个卷积滤波器，每个大小是 3 × 3 。输出的维度和输入的形状相同 padding='same' 所以也应该是 32 × 32
            keras.layers.Conv2D(32, (3, 3), padding='same', input_shape=(28, 28, 1), activation=keras.activations.relu),
            # 进行 2 × 2, 大小的最大池化运算
            keras.layers.MaxPooling2D(pool_size=(2, 2)),
            # 关闭 25% 的神经元
            keras.layers.Dropout(0.25),
            keras.layers.Flatten(name="flat"),
            keras.layers.Dense(300, activation=keras.activations.relu, name="h1"),
            keras.layers.Dense(10, activation=keras.activations.softmax, name="output")
        ])

        model.compile(loss=keras.losses.sparse_categorical_crossentropy, optimizer=keras.optimizers.Adam(),
                      metrics=[keras.metrics.SparseCategoricalAccuracy()])
        return model

    def callbacks(self, log_dir=None, file_name="fashion_model.h5"):
        # 设置回调函数
        # 如果直接使用字符串,则报错;找问题找很久了
        if log_dir is None:
            dir_log = os.path.join("../callbacks")
        else:
            dir_log = os.path.join(log_dir, "callbacks")

        if not os.path.exists(dir_log):
            os.mkdir(dir_log)

        output_model_file = os.path.join(dir_log, file_name)
        callbacks = [
            keras.callbacks.TensorBoard(log_dir=dir_log),
            keras.callbacks.ModelCheckpoint(output_model_file, save_best_only=True),
            keras.callbacks.EarlyStopping(patience=5, min_delta=1e-3),
        ]
        return callbacks

    def train(self, model, *args, **kwargs):
        history = model.fit(x=kwargs.get('train_x'), y=kwargs.get('train_y'), epochs=kwargs.get('epochs'), verbose=2,
                            validation_data=(kwargs.get('valid_x'), kwargs.get('valid_y')))
        return history

    def evaluate(self, model, x, y):
        return model.evaluate(x, y)

    def predict(self, model, pre_data):
        predictions = model.predict(pre_data)
        # 找出角标最大的数据
        # predict = np.argmax(predictions, axis=1)
        # "可能性:" + '{:.5f}%'.format(100 * np.max(predictions[0])
        return predictions

    def save(self, model, file_path=None, file_name=None):
        if file_path is None or file_path == "":
            file_path = os.path.join("models")
        else:
            file_path = os.path.join(file_path, "models")

        if not os.path.exists(file_path):
            os.mkdir(file_path)

        if file_name is None or file_name == "":
            file_name = os.path.join(file_path, f'my_model_{time.strftime("%Y%m%d", time.localtime())}.h5')
        else:
            file_name = os.path.join(file_path, file_name)
        model.save(file_name)

    def load(self, file_name):
        return tf.keras.models.load_model(file_name)

    def main(self):
        file_dir = r"C:\Users\andy\Desktop\models\test"
        SIZE = 6000
        print("第一步,处理需要训练的数据...")
        x, y, names = self.preprocess_data(input_data=file_dir)

        (train_x, train_y), (valid_x, valid_y), (test_x, test_y) = self.batch_dataset(x, y)
        model = self.compile_model()
        # return
        print("模型开始训练...")
        history = self.train(model=model, train_x=train_x, train_y=train_y,
                             valid_x=valid_x, valid_y=valid_y, epochs=10, callbacks=self.callbacks())
        # print("正在评估...")
        # eval = self.evaluate(model=model, x=test_x, y=test_y)
        # print(eval)
        pre = self.predict(model=model, pre_data=test_x)
        print(names, test_y[0], "实际标签:" + "".join(self.__get_key(names, np.argmax(pre, axis=1)[0])),
              "可能性:" + '{:.6f}%'.format(100 * np.max(pre[0])) + "->", "".join(self.__get_key(names, test_y[0])))

        # self.save(model)
        # 绘制学习率
        self.plot_learning_curves(history=history)

        self.show_imgs(test_x[0], self.__get_key(names, test_y[0]), self.__get_key(names, np.argmax(pre, axis=1)[0]),
                       100 * np.max(pre[0]))

    def __preprocess(self, path, label):
        img = tf.io.read_file(path)
        img = tf.io.decode_jpeg(img, channels=1)
        img = tf.image.resize(img, [28, 28])
        img = tf.image.random_flip_up_down(img)
        img = tf.image.random_crop(img, [28, 28, 1])
        # 自己添加,卷积网络,不需要重置矩阵
        # img = tf.reshape(img, [28, 28])
        img = tf.cast(img, dtype=tf.float32) / 255.
        label = tf.convert_to_tensor(int(label))
        # 热编码,暂不使用
        # label = tf.one_hot(label, depth=10)
        return img, label

    def __get_key(self, dct: dict, value):
        return list(filter(lambda k: dct[k] == value, dct))

    def plot_learning_curves(self, history):
        pd.DataFrame(history.history).plot(figsize=(8, 5))
        plt.grid()
        plt.gca().set_ylim(0, 1)
        plt.show()

    def show_imgs(self, img, title, lable, chance):
        img = img.reshape(28, 28)
        plt.figure()
        # 设置图例并且设置图例的字体及大小
        plt.imshow(img, cmap="binary", interpolation="nearest")
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        plt.title("".join(title))
        plt.xlabel("{}(Likely:{:.6f}%)".format("".join(lable), chance), color="blue")
        plt.show()


def main():
    s = SimNet2()
    s.main()


if __name__ == "__main__":
    from Timer import Timer

    with Timer.timer():
        main()
