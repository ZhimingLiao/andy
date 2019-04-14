# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2018-12-06 15:12
# 当前计算机登录名称 :广州医科大学附属第五医院
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '{2018-12-06} '


if __name__ == '__main__':

    # 查
    my_list = ['小黑','小白','小爱',1,2.2,1,1.5]
    print(my_list[-1])
    print(my_list[0])
    print(my_list.count(5))  # 查询某个元素在list里面出现的次数，若不存在的元素则输入为0,。
    print(my_list.count(1))
    print(my_list.count('小黑'))
    print('index方法：', my_list.index(1))  # 查找元素的下标，若查找元素不存在的话，会报错
    print('reverse方法：', my_list.reverse())  # 反转的意思，将list反转，无返回值，直接打印reverse结果为none。
    print(my_list)
    # my_list.clear() #清空整个list
    # print(my_list)

    nums = [9, 7, 6, 5, 5.6, 9.9, -1, -3, 0]
    nums.sort()  # 升序排序
    print('sort 升序排序：', nums)
    nums.reverse()
    print('reverse 反转后降序排序：', nums)

    # 如果指定了reverse则是降序
    nums.sort(reverse=True)
    print('指定了reverse，降序排序：', nums)

    # 把一个list里面的元素加入进去
    nums.extend(my_list)
    print('把一个list里面的元素加入nums：', nums)

    # 取100以内的偶数
    nums = list(range(1, 101))[1::2]
    print(nums)

    # 取100以内的奇数
    nums2 = list(range(1, 101))[::2]
    print(nums2)

