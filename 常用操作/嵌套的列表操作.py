# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 中山二院  志明  2019-05-09 19:14
# 当前计算机登录名称 :andy
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-09 19:14'

if __name__ == "__main__":
    names = ['关羽', '张飞', '赵云', '马超', '黄忠']
    courses = ['语文', '数学', '英语']
    # 录入五个学生三门课程的成绩
    # 错误 - 参考http://pythontutor.com/visualize.html#mode=edit
    scores = [[None] * len(courses)] * len(names)
    scores = [[None] * len(courses) for _ in range(len(names))]
    for row, name in enumerate(names):
        for col, course in enumerate(courses):
            scores[row][col] = float(input(u'请输入{name}的{course}成绩: '.format(name=col, course=name)))
            print(scores)
    # xxxx.encode / decode('unicode-escape')
    # a = u"请输入".encode("unicode-escape")
    # b1 = f'请输'
    # c = r'请输'
    # print(type(a), type(u'请输入'), a)
    # print(type(b1))
    # print(type(c))
    # print(a.decode("unicode-escape"))
