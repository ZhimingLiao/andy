# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州  志明  2019-06-12 16:21
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-06-12 16:21'

if __name__ == '__main__':
    import numpy as np
    import tensorflow as tf

    var1 = np.float32(np.random.rand(2, 100))
    var2 = np.dot([0.100, 0.200], var1) + 0.5

    b = tf.Variable(tf.zeros([1]), name='b')
    w = tf.Variable(tf.random_uniform([1, 2], -1.0, 1.0), name='w')
    y = tf.matmul(w, var1) + b

    loss = tf.reduce_mean(tf.square(y - var2))
    op = tf.train.GradientDescentOptimizer(0.5)
    train = op.minimize(loss)

    init = tf.global_variables_initializer()

    sess = tf.Session()
    sess.run(init)
    print(f'{sess.run(w)}, {sess.run(b)}')
    for step in range(200):
        sess.run(train)
        if step % 20 == 0:
            print(f'{sess.run(w)}, {sess.run(b)}, {step}')
