# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : PyCharm
#   File name   : andy	
#   Author      : liaozhimingandy@qq.com
#   Created date: 2020-01-10 13:57
#   Description :
#
# ================================================================
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

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
assert tf.__version__.startswith('2.')

from IBaseModel import IBaseModel


class SNNModel(IBaseModel):
    def __init__(self):
        self.__name = "SNNModel"

    def __generate_paths_lable(self, dir_path: str, flag_random=True) -> tuple:
        assert len(dir_path) > 1
        root = pathlib.Path(dir_path)
        paths = [str(path) for path in list(root.glob("*/*"))]
        # 随机打乱数据
        if flag_random:
            random.shuffle(paths)
        lables = sorted(item.name for item in root.glob('*/') if item.is_dir())
        index = dict((name, index) for index, name in enumerate(lables))
        index_lables = [index[pathlib.Path(path).parent.name] for path in paths]
        return paths, index_lables, index

    def preprocess_data(self, input_data):
        x, y, names = self.__generate_paths_lable(dir_path=input_data)
        ds = tf.data.Dataset.from_tensor_slices((x, y))
        # 数据集预处理
        ds = ds.shuffle(128).map(self.__preprocess)

        # 转换成numpy对象
        np_ds_x = np.zeros([len(y), 28, 28], dtype=np.float32)
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
        # 4.构建模型
        # 或者添加层数不一定会提高准确率,合适就好
        model = keras.models.Sequential([
            keras.layers.Flatten(input_shape=[28, 28], name="input"),
            keras.layers.Dense(300, activation=keras.activations.relu, name="h1"),
            keras.layers.Dense(100, activation=keras.activations.relu, name="h2"),
            keras.layers.Dense(10, activation=keras.activations.softmax, name="output")
        ])
        # 使用类对象无法使用保存函数,无法使用callback参数
        # model = SNN()
        # model.build(input_shape=(None, 28, 28))
        model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        return model

    def callbacks(self, log_dir=None, file_name="fashion_model.h5"):
        # 设置回调函数
        # 如果直接使用字符串,则报错;找问题找很久了
        if log_dir is None:
            dir_log = os.path.join("callbacks")
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

    def train(self, model, train_x, train_y, valid_x, valid_y, epochs=5, callbacks=None):
        history = model.fit(x=train_x, y=train_y, epochs=epochs, verbose=2,
                            validation_data=(valid_x, valid_y))
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
        print(names, test_y[0], self.__get_key(names, np.argmax(pre, axis=1)[0]),
              "可能性:" + '{:.1f}%'.format(100 * np.max(pre[0])), self.__get_key(names, test_y[0]))

        # self.save(model)
        # 绘制学习率
        # self.plot_learning_curves(history=history)

        self.show_imgs(test_x[0], self.__get_key(names, test_y[0]), self.__get_key(names, np.argmax(pre, axis=1)[0]),
                       100 * np.max(pre[0]))

    def __preprocess(self, path, label):
        img = tf.io.read_file(path)
        img = tf.io.decode_jpeg(img, channels=1)
        img = tf.image.resize(img, [28, 28])
        img = tf.image.random_flip_up_down(img)
        img = tf.image.random_crop(img, [28, 28, 1])
        # 自己添加,重置矩阵
        img = tf.reshape(img, [28, 28])
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
        plt.figure()
        # 设置图例并且设置图例的字体及大小
        plt.imshow(img, cmap="binary", interpolation="nearest")
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        plt.title(title)
        plt.xlabel("{}(Probability:{:.1f}%)".format(lable, chance), color="red")
        plt.show()


def main():
    s = SNNModel()
    # s.callback(log_dir=r"D:\test", file_name="test")
    s.main()


if __name__ == "__main__":
    from Timer import Timer

    with Timer.timer():
        main()
