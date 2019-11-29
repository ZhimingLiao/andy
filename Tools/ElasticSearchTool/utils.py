# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-11-20 12:39
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm

# 生成32位uuid
import uuid

# 汉字转拼音
from pypinyin import pinyin


# 生成32位uuid
def get_uuid():
    """
    自动生成32位uuid,并且已经转小写
    :return: 小写uuid
    """
    return "".join(str(uuid.uuid4()).split("-")).lower()


def get_py(char=None):
    """
    根据传入中文提取中文首字母大写
    :param char: 需要提取的中文
    :return: 汉字首字母大写
    """
    if not char:
        return None
    data = ""
    for value in pinyin(char, style=0):
        data += value[0][0].upper()
    return data


if __name__ == "__main__":
    pass
