# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-01-27 15:20
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-01-27 '

import tensorflow as tf
# 用于产生数据
import numpy as np

# 1.准备数据
XData = np.linspace(-10, 10, 200)[:, np.newaxis]
# 创建模型假设 Y = 5 * X + 10
Noice = np.random.normal(0, 0.05, XData.shape)  # 产生干扰数据
YData = 5 * XData + 1 + Noice

# 2.准备tensor模型
# 2.1定义使用的变量
x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)

# 2.2初始化要学习到的a和b,以及定义操作,第一个神经元
w = tf.Variable(tf.truncated_normal(shape=[1], mean=0.0, stddev=1), name='A')
b = tf.Variable(tf.zeros([1]), name='B')
Matmul = w * x + b
# OutData = tf.nn.tanh(Matmul)

# 2.3定义损失函数和学习率
Loss = tf.reduce_mean(tf.square(y - Matmul))
RateLearn = 0.02

TrainOP = tf.train.GradientDescentOptimizer(RateLearn).minimize(Loss)

# 3.保存模型数据
SaverDir = 'log/'
Saver = tf.train.Saver()

# 4.清除当前所有运行的图，以及初始化所有变量
tf.reset_default_graph
init = tf.global_variables_initializer()
# 5.开始训练
with tf.Session() as sess:
    sess.run(init)
    for X, Y in zip(XData, YData):
        sess.run(Matmul, feed_dict={x: X, y: Y})
    # 保存参数
    Saver.save(sess, SaverDir + 'test')
    # print('预测值:', sess.run(TrainOP, feed_dict={x: XData}))
