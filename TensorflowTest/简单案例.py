# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-01-22 21:10
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-01-22 '

import tensorflow as tf
import numpy as np

# 1. 使用numpy生成100个随机数
x_data = np.random.rand(100)
y_data = x_data * 2 + 5
print('x:', x_data)
print('y:', y_data)

#  2.定义变量
b = tf.Variable(1.)
k = tf.Variable(1.)
y = k * x_data + b

# 3.定义损失函数
loss = tf.reduce_mean(tf.square(y_data - y))
# 4.定义一个梯度下降优化器
optimizer = tf.train.GradientDescentOptimizer(0.2)
# 5.最小化代价函数
train = optimizer.minimize(loss)

# 初始化变量
init = tf.global_variables_initializer()

with tf.Session() as sess:
    # 初始化写训练日志
    # writer = tf.summary.FileWriter('logs', sess.graph)
    # merged = tf.summary.merge_all()
    sess.run(init)
    for step in range(500):
        sess.run(train)
        if step % 4 == 0:
            # result = sess.run(merged, feed_dict={'k': k, 'b': b})
            result = sess.run([k, b])
            print(step, result)
            # 写入到日志
            # writer.add_summary(result, step)
