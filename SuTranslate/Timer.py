# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州  志明  2019-05-29 8:56
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-29 8:56'

from time import perf_counter
from contextlib import contextmanager


class Timer(object):

    @staticmethod
    @contextmanager
    def timer():
        """计算代码运行的时间"""
        try:
            start = perf_counter()
            yield
        finally:
            end = perf_counter()
            print(f'花费时间<{end - start}>秒')


if __name__ == '__main__':
    with Timer.timer():
        for i in range(10000):
            print(i)
            # pass
