# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 中山二院  志明  2019-05-13 10:49
# 当前计算机登录名称 :andy
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-13 10:49'

import csv

from translate import Translator
import TranslateTool


def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


if __name__ == "__main__":
    translator = Translator(to_lang="zh")
    ll = list()
    import time

    tt1 = time.time()
    print("当前时间:" + time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))
    with open("c:/Users/andy/Desktop/zh_CN.locale.csv", "r") as f:
        reader = csv.reader(f)
        a, b = 0, 0
        for rows in reader:
            if rows:
                a += 1
                t = rows[1]
                if not is_contain_chinese(t):
                    # t1 = translator.translate(t)
                    t1 = TranslateTool.translate_func(t)
                    print("正在翻译第%d个;%s==>%s" % (b + 1, t, t1))
                    rows[1] = t1
                    ll.append(list((rows[0], t1)))
                    b += 1
                    continue
                ll.append(rows)
    print(ll)
    with open("c:/Users/andy/Desktop/zh_CN.locale.csv", "w") as f:
        w = csv.writer(f)
        w.writerows(ll)
    print("完成时间:" + time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))
    print("共花费时间:" + str(tt1 - time.time()))
