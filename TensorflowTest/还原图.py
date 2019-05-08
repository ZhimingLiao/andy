# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-01-28 7:27
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-01-28 '

import tensorflow as tf

sess = tf.Session()
saver = tf.train.import_meta_graph('log/test-29.meta')
saver.restore(sess, tf.train.latest_checkpoint('log/'))

graph = tf.get_default_graph()
w1 = graph.get_tensor_by_name("w:0")
w2 = graph.get_tensor_by_name("b:0")
print('还原图', w1, w2)
print(sess.run(wb, feed_dict={x: 3}))
# feed_dict ={w1:13.0,w2:17.0}
