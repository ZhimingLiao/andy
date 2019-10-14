# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广州  志明  2019-07-24 16:51
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm

__author____ = 'Andy Liao'
__time__ = '2019-07-24 16:51'
"""
uuid = 时间(17)+性别(1)+随机数(4)+校验位(1)
"""

import numpy as np
import time
import random


def get_time_stamp():
    """
    获取当前时间戳
    :return:
    """
    import re
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    # 打印时间格式
    # print(time_stamp)
    # stamp = ("".join(time_stamp.split()[0].split("-"))+"".join(time_stamp.split()[1].split(":"))).replace('.', '')
    # stamp = time_stamp.replace("-", "").replace(".", "").replace(" ", "").replace(":", "")
    # 3,使用正则表达式去除特殊符号
    stamp = re.sub(r'[\s:.-]', "", time_stamp)
    return stamp


def get_num_random(n):
    """
    获取固定位数的随机数,不得超过6位
    :return:
    """
    return str(random.randint(1000000, 9999999))[:-(n + 1):-1] if n < 9 else "位数超过六位"


def get_code_verify(num):
    if len(num) != 31:
        return {'Code': 1, 'Desc': '数据长度不对'}
    else:
        coefficient = (7, 9, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 3, 1, 6, 1, 3, 6, 9, 9, 5, 2, 5, 0, 5, 3)
        checkCode_list = ('1', '0', '9', '8', '7', '6', '5', '4', '3', '2')
        Sum = 0
        for i in range(30):
            Sum += eval(num[i]) * coefficient[i]  # 身份证前17位分别与对应的系数相乘之和
        remainder = Sum % 10  # 余数只会是[0,9] 计算得到身份证最后一位 效验码
        checkCodeValue = checkCode_list[remainder]
        return checkCodeValue


if __name__ == '__main__':
    text = "20190726009130201010680084543713"
    print(len(text))
    text1 = get_time_stamp()
    text2 = '0' * 10
    text3 = get_num_random(4)
    text4 = text1 + text2 + text3
    # text4 = get_code_verify(text1+text2+text3)
    print(text1 + text2 + text3 + text4)
    for _ in range(10000):
        # # print(get_time_stamp())
        #     text1 = get_time_stamp()
        #     text2 = '0' * 10
        #     text3 = get_num_random(4)
        #     # text4 = text1+text2+text3
        #     text4 = get_code_verify(text1 + text2 + text3)
        print(text1 + text2 + text3 + text4)
