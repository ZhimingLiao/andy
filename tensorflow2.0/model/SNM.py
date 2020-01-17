# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : PyCharm
#   File name   : andy	
#   Author      : liaozhimingandy@qq.com
#   Created date: 2020-01-10 16:10
#   Description :
#
# ================================================================

import tensorflow as tf
from tensorflow import keras


class SNM(tf.keras.Model):
    def __init__(self):
        super(SNM, self).__init__(name="SNM")
        """
        定义函数模型层数
        """
        # self.conv1 = keras.layers.Conv2D(32, 3, activation='relu')
        self.h0 = keras.layers.Flatten(name="h0")
        self.h1 = keras.layers.Dense(300, activation=keras.activations.relu, name="h1")
        self.h2 = keras.layers.Dense(100, activation=keras.activations.relu, name="h2")
        self.h3 = keras.layers.Dense(10, activation=keras.activations.softmax, name="h2")

    def call(self, inputs, training=None, mask=None):
        """完成模型正向计算"""
        # h0 = self.conv1(input)
        h1 = self.h0(inputs)
        h2 = self.h1(h1)
        h3 = self.h2(h2)
        output = self.h3(h3)

        return output


def main():
    network = SNM()
    network.build(input_shape=(None, 28, 28))
    network.summary()


if __name__ == "__main__":
    main()
