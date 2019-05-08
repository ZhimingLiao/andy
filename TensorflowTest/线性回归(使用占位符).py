# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-01-27 15:20
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-01-27 '

import tensorflow as tf
from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file as ptf
# 用于产生数据
import numpy as np

# 1.准备数据
XData = np.linspace(-10, 10, 200).astype(dtype=np.float32)
# 创建模型假设 Y = 5 * X + 10
Noise = np.random.normal(0, 0.05, XData.shape)  # 产生干扰数据
YData = 5 * XData + 1

tf.reset_default_graph()
# 2.准备tensor模型
# 2.1定义使用的变量
x = tf.placeholder(tf.float32, name='x')
y = tf.placeholder(tf.float32, name='y')

# 2.2初始化要学习到的a和b,以及定义操作,第一个神经元
w = tf.Variable(tf.random_uniform([1], -100.0, 50.0), dtype=tf.float32, name='w')
b = tf.Variable(tf.random_uniform([1], -150.0, 50.0), dtype=tf.float32, name='b')
wb = w * x + b
# L1 = tf.nn.tanh(wb) 不适合张量为0的操作,适合一维以上的数据

# 2.3定义损失函数和学习率
Loss = tf.reduce_mean(tf.square(y - wb))
RateLearn = 0.001

TrainOP = tf.train.GradientDescentOptimizer(RateLearn).minimize(Loss)
#
# # 3.保存模型数据
SaverDir = 'log/'
Saver = tf.train.Saver()
# # 4.清除当前所有运行的图，以及初始化所有变量
init = tf.global_variables_initializer()
# 5.开始训练
# with tf.Session() as sess:
#     sess.run(init)
#     print("before the train, the W is %6f, the b is %6f" % (sess.run(w), sess.run(b)))
#     for i in range(30):
#         for X, Y in zip(XData, YData):
#             print('-'*30)
#             print('第'+ str(i) +'次测试W: %6f,b : %6f'%(sess.run(w), sess.run(b)))
#             # sess.run(TrainOP)
#             sess.run(TrainOP, feed_dict={x: X, y: Y})
#             print('-' * 30)
#     # 保存参数
#     Saver.save(sess, SaverDir+'test', global_step=i) #  图不会变,所以不需要每次都保存
#     # writer = tf.summary.FileWriter("log/mnist_nn_log", sess.graph)
#     # print('预测值:', sess.run(wb, feed_dict={x: 2}))

#
# 使用模型
saver2 = tf.train.import_meta_graph('log/test-29.meta')
# 打印所以图信息
ptf('log/test-29', None, True, True)
# tensor_name:  Variable
# [5.002444]
# tensor_name:  Variable_1
# [0.97671086]
# [5.9791546]
# with tf.Session() as sess2:
#     sess2.run(tf.global_variables_initializer())
#     test = tf.train.get_checkpoint_state('log/')
#     if test and test.model_checkpoint_path:
#         saver2.restore(sess2, tf.train.latest_checkpoint('log/'))
#         print(sess2.run(wb, feed_dict={x: 1}))
#     print('不存在!')


with tf.Session() as sess3:
    sess3.run(tf.global_variables_initializer())
    test = tf.train.get_checkpoint_state('log/')
    if test and test.model_checkpoint_path:
        saver2.restore(sess3, tf.train.latest_checkpoint('log/'))
        print(sess3.run(wb, feed_dict={x: 1}))
    else:
        print('不存在!')

# saver = tf.train.import_meta_graph('log/test.meta')
# saver.restore(sess, tf.train.latest_checkpoint('log/'))
#
# # Now, let's access and create placeholders variables and
# # create feed-dict to feed new data
#
# graph = tf.get_default_graph()
# w1 = graph.get_tensor_by_name("w:0")
# w2 = graph.get_tensor_by_name("b:0")
#
# # Now, access the op that you want to run.
# op = graph.get_tensor_by_name("wb:0")

# Add more to the current graph
# print(w1, w2, op)
