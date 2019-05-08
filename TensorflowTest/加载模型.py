# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-01-27 12:43
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-01-27 '

import tensorflow as tf

tf.reset_default_graph()

with tf.Session() as sess:
    print('加载模型...')
    Saver = tf.train.import_meta_graph('log/test.tmp.meta')
    Saver.restore(sess, tf.train.latest_checkpoint('log/'))
    print('x:', sess.run('x:3'))
