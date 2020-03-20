# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
#   Copyright (C) 2020 liaozhimingandy@qq.com Ltd. All Rights Reserved.
#
#   Editor      : PyCharm
#   Project     : zhiming
#   File Name   : xlsx_decrypt.py	
#   Author      : liaozhimingandy@qq.com
#   Created Date: 2020-02-09 10:44
#   Description : word密码尝试;使用模块为pywin32
#
# ======================================================================

__author__ = "zhiming"

import os
import datetime

from win32com.client import Dispatch


class ExcelTool(object):

    @staticmethod
    def word_decrypt(src_file: str) -> bool:
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
        # passwords = ('{:0>4}'.format(p) for p in range(0, 10 ** 4))
        # pw_lst = ['{:0>4}'.format(p) for p in range(0, 10**4)]
        # print(f"生成器所占空间：{sys.getsizeof(passwords)}，列表所占空间：{sys.getsizeof(pw_lst)}")
        start = ("HZ", "hz")
        datetimes = datetime.datetime(2016, 1, 1)
        passwords = ""
        while datetimes.year < 2017:
            for i in ('{:0>3}'.format(p) for p in range(0, 10 ** 3)):
                if int(i) > 10:
                    break
                pwd = 'Hz' + datetimes.strftime('%Y-%m-%d').replace("-", "") + i
                print(f"正在尝试密码打开(备注密码是：{pwd})")
                try:
                    wdapp = Dispatch("Word.Application")
                    wb = wdapp.Documents.Open(src_file, False, True, None, pwd)
                except (Exception,) as e:
                    # print(e)
                    pass
                else:
                    flag = True
                    print(f"解密成功!密码是：{pwd}")
                    wb.Close()
                    wdapp.Quit()
                    return flag
            datetimes += datetime.timedelta(days=1)
            # break
        # for pwd in passwords:
        #     print(f"正在尝试密码打开(备注密码是：{pwd})")
        #     try:
        #         wdapp = Dispatch("Word.Application")
        #         wb = wdapp.Documents.Open(src_file, False, True, None, pwd)
        #     except (Exception,) as e:
        #         # print(e)
        #         pass
        #     else:
        #         flag = True
        #         print(f"解密成功!密码是：{pwd}")
        #         wb.Close()
        #         wdapp.Quit()
        #         break
        #     # break
        print("尝试解密失败!请重新设置密码组合条件;")
        return flag


def main():
    file_path = r"D:\BaiduNetdiskDownload\随心录2016.01.docx"
    ExcelTool.word_decrypt(src_file=file_path)


if __name__ == "__main__":
    from Timer import Timer

    with Timer.timer():
        main()
