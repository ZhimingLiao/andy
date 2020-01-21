# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
#   Copyright (C) 2020 liaozhimingandy@qq.com Ltd. All Rights Reserved.
#
#   Editor      : PyCharm
#   Project     : andy
#   File Name   : xlsx_decrypt.py	
#   Author      : liaozhimingandy@qq.com
#   Created Date: 2020-01-21 10:44
#   Description : excel密码尝试
#
# ======================================================================

__author__ = "zhiming"

import os

from win32com.client import Dispatch


class ExcelTool(object):

    @staticmethod
    def excel_decrypt(src_file: str) -> bool:
        """
        Excel自动解密
        :param src_file:待解密Excel文件路径
        :param password:密码,多个密码用英文逗号隔开
        :param del_src:是否删除原始加密文件
        :return:
        """
        # 判断文件是否存在
        if not os.path.exists(src_file):
            raise OSError(f"文件:{src_file},不存在,请重新查看是否存在该文件！")

        flag = False
        passwords = ('{:0>4}'.format(p) for p in range(0, 10 ** 4))
        # pw_lst = ['{:0>4}'.format(p) for p in range(0, 10**4)]
        # print(f"生成器所占空间：{sys.getsizeof(passwords)}，列表所占空间：{sys.getsizeof(pw_lst)}")
        for pwd in passwords:
            print(f"正在尝试密码打开(备注密码是：{pwd})")
            try:
                xlapp = Dispatch("Excel.Application")
                wb = xlapp.Workbooks.Open(src_file, False, True, None, pwd)
            except (Exception,) as e:
                # print(e)
                pass
            else:
                flag = True
                print(f"解密成功,密码是：{pwd}")
                wb.Close()
                xlapp.Quit()
                break
            # break

        return flag


def main():
    file_path = r"C:\Users\andy\Desktop\test\201806.xlsx"
    ExcelTool.excel_decrypt(src_file=file_path)


if __name__ == "__main__":
    from Timer import Timer

    with Timer.timer():
        main()
