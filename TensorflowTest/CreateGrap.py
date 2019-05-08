# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2019-01-22 20:30
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-01-22 '

import tensorflow as tf

# 1.创建一个常量
m1 = tf.constant([[3, 3]])
m2 = tf.constant([[2], [3]])

# 2.创建一个操作+
product = tf.matmul(m1, m2)
print('操作类型:', product)

# 3.使用with不需要关闭会话,程序会自动关闭,打开文件亦如此
with tf.Session() as sess:
    result = sess.run(product)
    print(result)

# # 3.定义一个图,会自动使用默认图
# sess = tf.Session()
# result = sess.run(product)
# print(result)
#
# # 4.关闭会话
# sess.close()
