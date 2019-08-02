# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州  志明  2019-07-03 8:46
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm

__author____ = 'Andy Liao'
__time__ = '2019-07-03 8:46'

import tensorflow as tf


def tensorflow_demo():
    '''
    tensorflow基础测试
    :return:
    '''
    # 占位符
    a = tf.placeholder(tf.float32, shape=[None, 3], name='test')
    with tf.Session(config=tf.ConfigProto(True)) as sess:
        print(sess.run(a, feed_dict={a: [[2, 4, 8]]}))
        print(a.name, a.dtype, a.op)
        print(a.graph)

    return None


def tensorflow_demo1():
    # a = tf.zeros([3, 4], tf.float32)
    # b = tf.constant(5)
    a = tf.Variable(tf.random_normal([2, 4], mean=0.0, stddev=0))

    # 变量需要初始化
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print(a.eval())
        # 程序结构写入事件文件
        fw = tf.summary.FileWriter('tmp', graph=sess.graph)
    return None


def tensorflow_demo2():
    '''
    线性回归
    :return:
    '''
    with tf.variable_scope("data..."):
        x = tf.random_normal([100, 1], mean=1.75, stddev=2, name='x')
        y = tf.matmul(x, [[0.7]]) + 0.8

    with tf.variable_scope('teset'):
        w = tf.Variable(tf.random_normal([1, 1], mean=0, stddev=0), name='w', trainable=True)
        b = tf.Variable(0.0, name='b')
    with tf.variable_scope('op'):
        y_pre = tf.matmul(x, w) + b

    loss = tf.reduce_mean(tf.square(y_pre - y))
    op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    init = tf.global_variables_initializer()
    # 收集变量
    tf.summary.scalar(name='loss', tensor=loss)
    # tf.summary.histogram(name='w', w)

    merg = tf.summary.merge_all()
    saver = tf.train.Saver([w, b], max_to_keep=5)
    with tf.Session() as sess:
        sess.run(init)
        fw = tf.summary.FileWriter('tmp', graph=sess.graph)
        for i in range(200):
            print(w.eval(), b.eval())
            sess.run(op)
            sum = sess.run(merg)
            print(w.eval(), b.eval())
            fw.add_summary(sum, i)
        saver.save(sess, './tmp/model/')
    return None


def tensorflow_demo3(files):
    """
    读取csv文件
    :return:
    """
    # 1.构建文件队列
    file_queue = tf.train.string_input_producer(files)
    # 2.构造csv阅读器
    reader = tf.TextLineReader()
    key, value = reader.read(file_queue)
    # 3.对每一行读取解析,record_defaults =[[1],[]]
    records = [['None'], ['None']]
    example, label = tf.decode_csv(value, record_defaults=records)
    print(example, label)
    return example, label


def main():
    import os
    file_name = os.listdir('./data')
    file_list = [os.path.join('./data', file) for file in file_name]
    print(file_name)
    example, label = tensorflow_demo3(file_list)
    with tf.Session() as sess:
        # 定义一个线程协调器
        coord = tf.train.Coordinator()
        # 开启会话运行线程
        threads = tf.train.start_queue_runners(sess, coord=coord)
        print(sess.run([example, label]))
        # 回收子线程
        coord.request_stop()
        coord.join(threads)


def picread(filelist):
    """
    读取图片并且转换成张量
    :param filelist:
    :return:
    """
    # 1, 构建图片文件队列
    file_queue = tf.train.string_input_producer(filelist)
    # 2, 构建图片阅读器
    reader = tf.WholeFileReader()
    # 3, 读取图片数据
    key, value = reader.read(file_queue)
    image = tf.image.decode_jpeg(value)
    print(image)
    # 4, 处理图片大小,统一大小
    image_resize = tf.image.resize_images(image, [200, 200])

    # 把样本的形状固定[200, 200, 3],必须定义通道数
    image_resize.set_shape([200, 200, 3])
    print(image_resize)
    # 5,进行批量处理
    image_batch = tf.train.batch([image_resize], batch_size=2, num_threads=1)
    print(image_batch)
    return image_resize


def main1():
    import os
    file_name = os.listdir('./pic')
    file_list = [os.path.join('./pic', file) for file in file_name]
    print(file_name)
    image_resize = picread(file_list)
    with tf.Session() as sess:
        # 定义一个线程协调器
        coord = tf.train.Coordinator()
        # 开启会话运行线程
        threads = tf.train.start_queue_runners(sess, coord=coord)
        print(sess.run([image_resize]))
        # 回收子线程
        coord.request_stop()
        coord.join(threads)


def main2():
    # 读取mnist数据集数据
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets("./mnist/", one_hot=True)
    print(mnist.test.lables)
    return None


if __name__ == '__main__':
    from tensorflow.examples.tutorials.mnist import input_data

    mnist = input_data.read_data_sets("./mnist/", one_hot=True)
    print(mnist.test.lables)
