# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-01-22 21:45
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-01-22 '

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

x_data = np.linspace(-0.5, 0.5, 200)[:, np.newaxis]
print(x_data)
noise = np.random.normal(0, 0.02, x_data.shape)
print(noise)
y_data = np.square(x_data) + noise

# 定义变量
x = tf.placeholder(tf.float32, [None, 1])
y = tf.placeholder(tf.float32, [None, 1])

# 定义神经元中间层
w = tf.Variable(tf.random_normal([1, 10]))
b = tf.Variable(tf.zeros([1, 10]))
wb = tf.matmul(x, w) + b
L1 = tf.nn.tanh(wb)

# 定义神经元输出层
w2 = tf.Variable(tf.random_normal([10, 1]))
b2 = tf.Variable(tf.zeros([1, 1]))
wb2 = tf.matmul(L1, w2) + b2
p = tf.nn.tanh(wb2)

# 定义损失函数和梯度算法
loss = tf.reduce_mean(tf.square(y - p))
optimizer = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

# 初始化变量
init = tf.global_variables_initializer()

# 开启会话
with tf.Session() as sess:
    sess.run(init)
    for _ in range(500):
        sess.run(optimizer, feed_dict={x: x_data, y: y_data})

    pre = sess.run(p, feed_dict={x: x_data})

    plt.figure()
    plt.scatter(x_data, y_data)
    plt.plot(x_data, pre, 'r-', lw=5)
    plt.show()
