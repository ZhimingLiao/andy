# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-01-22 20:42
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-01-22 '

import tensorflow as tf

# 定义变量
x = tf.Variable([1, 3], name='x')
a = tf.constant([3, 4], name='y')
b = tf.Variable(0, name='z')
c = tf.Variable(3, name='t')

# 定义一个操作-
sub = tf.subtract(x, a)
add = tf.add(x, a)

# 赋值操作
update = tf.assign(b, c)
print('赋值后:', b)
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print('赋值后----:', sess.run(update))
    print(sess.run(sub))
    print(sess.run(add))
