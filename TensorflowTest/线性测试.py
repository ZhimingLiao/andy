# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-02-05 20:37
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-02-05 '

'''
形如 y = 2*x + 5 创建模型
'''
# 1.导入对应库
import tensorflow as tf
# 用于产生数据
import numpy as np

# 2.准备数据
InputDataX = np.linspace(-10, 10, 100).astype(dtype=np.float32)
Noise = np.random.normal(-0.05, 0.05, InputDataX.shape)
InputDataY = 2 * InputDataX + Noise

# 3.清除之前所有图
tf.reset_default_graph()

# 4.创建模型
# 1)定义输入变量
x = tf.placeholder(tf.float32, name='x')
y = tf.placeholder(tf.float32, name='y')

# 2)创建模型
a = tf.Variable(tf.random_uniform([1], -50.0, 50.0), dtype=tf.float32, name='a')
b = tf.Variable(tf.random_uniform([1], -50.0, 50.0), dtype=tf.float32, name='b')
w = a * x + b

# 3)定义损失函数和学习率
loss = tf.reduce_mean(tf.square(y - w))
RateLearn = 0.01

# 4)定义训练操作
TrainOp = tf.train.GradientDescentOptimizer(RateLearn).minimize(loss)

# 5.初始化保存模型数据数据
SaveDir = 'log/'
Saver = tf.train.Saver()

# 6.清除当前所有运行的图，以及初始化所有变量
init = tf.global_variables_initializer()

# 7.开始训练模型
with tf.Session() as sess:
    sess.run(init)
    print('模型正在训练中...')

    for i in range(10):
        for X, Y in zip(InputDataX, InputDataY):
            sess.run(TrainOp, feed_dict={x: X, y: Y})
            print('第{num}轮训练值,a={a},b={b}'.format(num=i, a=sess.run(a), b=sess.run(b)))

    # 1)保存模型数据
    # 如果图不变,模型不需要每次都保存
    Saver.save(sess, SaveDir + 'test', global_step=1)
    # 2)进行预测
    print('预测值:', sess.run(w, feed_dict={x: 5.0}))
