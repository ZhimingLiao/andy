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
# 用于绘制图
import matplotlib.pyplot as plt

# 2.准备数据,TODO 此方法不适合[1, 1]的数字
InputDataX = np.linspace(-1, 1, 200)[:, np.newaxis]
Noise = np.random.normal(-0.05, 0.05, InputDataX.shape)
# InputDataY = 2*InputDataX + 5 + Noise
InputDataY = np.square(InputDataX) + Noise

# 3.清除之前所有图
tf.reset_default_graph()

# 4.创建模型
# 1)定义输入变量
x = tf.placeholder(tf.float32, [None, 1], name='x')
y = tf.placeholder(tf.float32, [None, 1], name='y')

# 2)创建模型,定义神经元
a1 = tf.Variable(tf.random_normal([1, 10]), name='a1')
b1 = tf.Variable(tf.zeros([1, 10]), name='b1')
w1 = tf.matmul(x, a1) + b1
l1 = tf.nn.tanh(w1)

# 输出神经元
a2 = tf.Variable(tf.random_normal([10, 1]), name='a2')
b2 = tf.Variable(tf.zeros([1, 1]), name='b2')
w2 = tf.matmul(l1, a2) + b2
Prediction = tf.nn.tanh(w2)

# 3)定义损失函数和学习率
loss = tf.reduce_mean(tf.square(y - Prediction))
RateLearn = 0.1

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

    for i in range(200):
        sess.run(TrainOp, feed_dict={x: InputDataX, y: InputDataY})
        # 可以使用sess.run([a2, b2])
        print('第{num}轮训练值,a={a},b={b}'.format(num=i + 1, a=sess.run(a2), b=sess.run(b2)))

    # 1)保存模型数据
    # 如果图不变,模型不需要每次都保存
    Saver.save(sess, SaveDir + 'test2', global_step=1)
    # 2)进行预测
    print('预测值:', sess.run(Prediction, feed_dict={x: [[0.6]]}))
    Pre = sess.run(Prediction, feed_dict={x: InputDataX})

    plt.figure()
    plt.scatter(InputDataX, InputDataY)
    plt.plot(InputDataX, Pre, 'r-', lw=1)
    plt.show()
