# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2018-12-06 14:49
# 当前计算机登录名称 :广州医科大学附属第五医院
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '{2018-12-06} '


if __name__ == '__main__':
    Str = 'abcdERF1 23中国'

    # 1. 判断输入的字符串是否为数字
    print(Str.isdigit())
    # 如果字符串至少有一个字符并且所有字符都是字母则返回True, 否则返回False
    print(Str.isalpha())
    print(Str.isalnum())

    # 2. 去除字符串的空格
    print(Str.strip())
    print('  ab fs'.lstrip())  # 默认去掉字符串左边的空格和换行,执行结果：ab fs
    print('hello  '.rstrip())  # 默认去掉字符串右边的空格和换行，执行结果：hello
    print('\nmysql abcd'.strip())  # 默认去掉两边的空格和换行,执行结果：mysql abcd，中间的空格不可去除
    print('mysqlmy'.strip('m'))  # 去除指定的字符串，例如：去除两边的m元素,执行结果：ysqlm   y

    # 3.字符串随机生成大小写字母、数字
    import string

    print(string.ascii_letters + string.digits)  # 输出所有的大小写字母+（0-9）的数字
    print(string.ascii_letters)  # 输出大小写的英文字母,执行结果：abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    print(string.ascii_lowercase)  # 输出小写英文字母，执行结果：abcdefghijklmnopqrstuvwxyz
    print(string.ascii_uppercase)  # 输出小写英文字母，执行结果：ABCDEFGHIJKLMNOPQRSTUVWXYZ

    # 4. count计数
    print(Str.count('a'))

    # 5.对字符串的首字母进行大写
    name = 'hello world is world'
    print(name.capitalize())  # 首字母大写，执行结果：Hello world
    print(name.center(50, '*'))  # 长度总共为50，将name字符串的值放在中间，两边补充*号显示

