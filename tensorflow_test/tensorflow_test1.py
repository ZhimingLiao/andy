# !/usr/bin/env python3
# -*- coding:utf-8 -*-

'''tensorflow测试'''

# 广州  志明  2019-07-02 14:53
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm

__author____ = 'Andy Liao'
__time__ = '2019-07-02 14:53'

import tensorflow as tf


def tensorflow_demo():
    '''
    tensorflow基础结构
    :parameter
    :return:
    '''
    # 定义图
    new_graph = tf.Graph()
    with new_graph.as_default():
        a = tf.constant(3, name='a')
        b = tf.constant(4, name='b')
        c = a + b

    # 打印图
    print(b.graph, tf.get_default_graph, new_graph)

    # 开启会话
    with tf.Session(graph=new_graph) as session:
        print(f'c={session.run(c)}')
        print(f'{session.graph}')
    return None


if __name__ == '__main__':
    '''代码1 tensorflow基础结构'''
    tensorflow_demo()
