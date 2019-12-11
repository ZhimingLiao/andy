# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-11-20 12:39
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm

import os
# 生成32位uuid
import uuid

import xlrd
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


def get_data(file_name):
    """
    根据文件路径提取excle里面的code和name
    :param file_name:
    :return:
    """
    result = list()
    if not os.path.exists(file_name):
        return {"error": 1, "msg": f"文件路径:{file_name},不存在!"}
    files_xls = xlrd.open_workbook(file_name)
    for name in files_xls.sheet_names():
        sheet = files_xls.sheet_by_name(name)
        for row in range(1, sheet.nrows):
            result.append({"CODE": int(sheet.row(row)[0].value) if isinstance(sheet.row(row)[0].value, (float,))
            else sheet.row(row)[0].value, "NAME": sheet.row(row)[1].value})

    return result


if __name__ == "__main__":
    # res = get_data(r"C:\Users\andy\Desktop\test.xlsx")
    # print(res)
    pass
