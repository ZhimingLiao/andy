# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-04-10 16:59
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-04-10 '

# 1.导入tensorflow和numpy包
import tensorflow as tf
import numpy as np

if __name__ == "__main__":
    XData = np.float32(np.random.rand(100))
    YData = XData * 2 + 1
    print(XData, YData)

    # 清除之前所有图
    tf.reset_default_graph()

    x = tf.placeholder(tf.float32)

    # tensorflow定义变量
    w = tf.Variable(2.0, name='w')
    b = tf.Variable(2.0, name='b')
    y = w * x + b

    loss = tf.reduce_mean(tf.square(y - YData))
    op = tf.train.GradientDescentOptimizer(0.5)
    train = op.minimize(loss)

    # 获取全局得变量并且进行初始化
    init = tf.global_variables_initializer()
    saver = tf.train.Saver(max_to_keep=0)

    # 启动会话执行图
    with tf.Session() as sess:
        sess.run(init)
        # print(sess.run(b))
        # print(sess.run(b), sess.run(w))
        print("模型开始训练...")
        for i in range(100):
            sess.run(train, feed_dict={x: XData})
            print(i, sess.run(b), sess.run(w))
        saver.save(sess, 'logs/aa.ckpt', global_step=1)
        print(sess.run([w, b]))
        print(sess.run(y, feed_dict={x: 3.0}))
        tf.summary.FileWriter("logs/", sess.graph)

        # tensorboard - -logdir logs cmd查看
    print("模型训练完毕!")
