# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : PyCharm
#   File name   : andy	
#   Author      : liaozhimingandy@qq.com
#   Created date: 2020-01-10 10:42
#   Description :基本模型接口规范
#
# ================================================================

from abc import ABCMeta, abstractmethod


class IBaseModel(metaclass=ABCMeta):

    @abstractmethod
    def preprocess_data(self, input_data):
        """
        数据预处理,得到numpy数据集
        :return: numpy数据集(包括数据和对应标签以及字典参照[如果有])
        """
        pass

    @abstractmethod
    def batch_dataset(self, x, y, train_pre=0.7, valid_pre=0.2, test_pre=0.1):
        """
        将整个数据集按一定比例分成训练集,验证集,测试集
        :param x: 需要分割的数据集
        :param y:标签值,和数据值数量一致
        :param train_pre:训练数据占总数据集的比例
        :param valid_pre:验证数据占总数据的比例
        :param test_pre:测试数据占总数据的比例
        :return: 训练集,验证集,测试集
        """
        pass

    @abstractmethod
    def compile_model(self):
        """
        :return:返回一个已经编译好的模型
        """
        pass

    @abstractmethod
    def callbacks(self, log_dir=None, file_name=None):
        """
        自定义回调需要处理的内容,如:TensorBoard,ModelCheckpoint,EarlyStopping
        :param log_dir: 训练好的日志目录
        :param file_name: 文件名称
        :return: None
        """
        pass

    @abstractmethod
    def train(self, model, train_x, train_y, valid_x, valid_y, epochs=5, callbacks=None):
        """
        :param model: 已经编译好的model
        :param train_x: 需要训练的数据
        :param train_y: 需要训练的标签
        :param valid_x: 验证的数据
        :param valid_y: 验证的标签
        :param epochs: 训练的次数
        :param callbacks: 回调函数
        :return:
        """
        pass

    @abstractmethod
    def evaluate(self, model, x, y):
        """
        :param model:已编译好的model
        :param x: 评估的数据集
        :param y: 评估的标签
        :return:
        """
        pass

    @abstractmethod
    def predict(self, model, pre_data):
        """
        :param model: 已编译好的model
        :param pre_data: 需要预测的数据
        :return:
        """
        pass

    @abstractmethod
    def save(self, model, file_path=None, file_name=None):
        """
        :param model: 已编译好的model
        :param file_path: 保存路径
        :param file_name: 文件名称
        :return:
        """
        pass

    @abstractmethod
    def load(self, file_name):
        """
        :param file_name: 保存的模型的文件地址
        :return:
        """
        pass

    @abstractmethod
    def main(self):
        # 此处定义基本操作步骤;根据需要选择非必选步骤
        # *1.得到数据集, 数据集打乱处理;返回numpy, preprocess_data
        # *2.分批得到训练, 验证, 测试数据集, batch_dataset
        # 3.得到已编译好的模型, compile_model
        # 4.设置回调函数, callback
        # 5.模型训练, 返回训练好的模型, train
        # 6.模型评估, evaluate
        # 7.模型预测, predict
        # 8.模型保存, save
        # 9.模型加载, load
        pass


def main():
    pass


if __name__ == "__main__":
    main()
