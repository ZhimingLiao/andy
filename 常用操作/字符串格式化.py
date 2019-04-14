# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2018-12-06 15:22
# 当前计算机登录名称 :广州医科大学附属第五医院
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '{2018-12-06}'


if __name__ == '__main__':

    hash = {'name': 'hoho', 'age': 18}
    # 1.使用关键字参数
    print('姓名:{name},年龄:{age}'.format(**hash))

    # 2.填充与格式化 :[填充字符][对齐方式 <^>][宽度]
    print('{0:*>10}'.format(10))  ##右对齐
    print('{0:*<10}'.format(10))  ##左对齐
    print('{0:*^10}'.format(10))  ##居中对齐

    # 3.精度与进制
    print('{0:.8f}'.format(1/3))
    print('{0:b}'.format(10))    #二进制
    print('{0:o}'.format(10))  # 八进制
    print('{0:x}'.format(10))  # 十六进制
    print('{:,}'.format(12369132698))  #千分位格式化

    # 4.使用索引
    print('姓名:{0[0]},年龄:{0[1]}'.format(list(hash.values())))