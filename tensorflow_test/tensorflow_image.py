# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# 广州  志明  2019-07-02 18:38
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm

__author____ = 'Andy Liao'
__time__ = '2019-07-02 18:38'

import tensorflow as tf
import os


def _parse_function(filename):
    # print(filename)
    image_string = tf.read_file(filename)
    print(image_string)
    image_decoded = tf.image.decode_image(image_string)  # (375, 500, 3)
    '''
        Tensor` with type `uint8` with shape `[height, width, num_channels]` for
          BMP, JPEG, and PNG images and shape `[num_frames, height, width, 3]` for
          GIF images.
    '''

    # image_resized = tf.image.resize_images(label, [200, 200])
    '''  images 三维，四维的都可以
         images: 4-D Tensor of shape `[batch, height, width, channels]` or
            3-D Tensor of shape `[height, width, channels]`.
        size: A 1-D int32 Tensor of 2 elements: `new_height, new_width`.  The
              new size for the images.

    '''
    image_resized = tf.image.resize_image_with_crop_or_pad(image_decoded, 200, 200)

    # return tf.squeeze(mage_resized,axis=0)
    return image_resized


def image_read(file_list):
    # 构建文件队列
    # file_queue = tf.train.string_input_producer(file_list)
    file_queue = tf.data.Dataset.from_tensor_slices(file_list)
    print(file_queue)
    # 读取与解码
    # reader = tf.WholeFileReader()
    # key, value = reader.read(file_queue, name='reader')
    dataset = tf.data.Dataset.from_tensor_slices(file_list)
    t = dataset.map(_parse_function)
    # print(key, value)
    print(t)
    # with tf.Session() as sess:
    #     coord = tf.train.Coordinator()
    #     threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    #     key_new, value_new = sess.run([key, value])
    #     print(key_new, value_new)
    #
    #     coord.request_stop()
    #     coord.join(threads)

    return None


if __name__ == '__main__':
    # 构建目录_文件名
    filename = os.listdir('./pic')
    # 文件路径 = 目录名称+文件名
    file_list = [os.path.join('./pic', file) for file in filename]
    print(file_list)
    image_read(filename)
