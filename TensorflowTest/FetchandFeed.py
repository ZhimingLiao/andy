# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-01-22 21:01
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-01-22 '

import tensorflow as tf

# 定义变量
input1 = tf.constant(3.0)
input2 = tf.constant(4.0)
input3 = tf.constant(5.0)

# 定义操作
add = tf.add(input1, input2)
mul = tf.multiply(input3, add)

# 启动会话
with tf.Session() as sess:
    result = sess.run([mul, add])
    print(result)

# 创建占位符
input4 = tf.placeholder(tf.float32)
input5 = tf.placeholder(tf.float32)

# 定义操作
op = tf.multiply(input5, input4)

with tf.Session() as sess:
    print(sess.run(op, feed_dict={input4: [3, ], input5: [4, ]}))
