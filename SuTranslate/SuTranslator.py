# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-05-14 19:24
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-14 19:24'

from translate import Translator
from SuTranslate.BaiDuTranslator import BaiDuTranslator


class SuTranslator:
    translators = set()
    BD = None
    tr = None


def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return 1
    return 0


if __name__ == '__main__':
    import time
    import random
    import csv
    import os
    from SuTranslate.BaiDuTranslator import BaiDuTranslator
    from SuTranslate.GoogleTranslator import GoogleTranslator
    from SuTranslate.YoudaoTranslator import YoudaoTranslator
    from googletrans import Translator
    from SuTranslate.Logger import Logger

    go = GoogleTranslator()
    yd = YoudaoTranslator()
    bd = BaiDuTranslator()
    fy = bd
    lg = Logger()
    with open("c:/Users/andy/Desktop/test.csv", "r") as f:
        reader = csv.reader(f)
        datas = list()
        dss = list()
        if os.path.exists("c:/Users/andy/Desktop/test-1.csv"):
            with open("c:/Users/andy/Desktop/test-1.csv", "r") as fs:
                rr = csv.reader(fs)
                for rrow in rr:
                    datas.append(rrow)
            fs.close()
        for va in datas:
            dss.append(va[0])
        w = open("c:/Users/andy/Desktop/test-1.csv", "a", newline="")
        writer = csv.writer(w)
        for row in reader:
            if row[0] in dss:
                pass
            elif not is_contain_chinese(row[1]) and (row[0] not in dss) and row[1] != '':
                print("正在翻译", row[1])
                text = fy.translate(row[1])
                # text = fy.translate(row[1], dest='zh-cn', src='en')
                t1 = random.random() * 2
                time.sleep(t1)
                print("翻译结果{text},随机休息{t1}秒,防止被禁用!".format(text=text, t1=t1))
                if text['Status'] == 0:
                    writer.writerow((row[0], text['Result']))
                elif text['Status'] == 1:
                    lg.info(text["Desc"] + ";翻译网络被封!正在切换有道翻译")
                    if fy == bd:
                        fy = yd
                        print("正在翻译", row[1])
                        text = fy.translate(row[1])
                        if not text['Status']:
                            writer.writerow((row[0], text['Result']))
                    elif fy == yd:
                        lg.info(text["Desc"] + ";翻译网络被封!正在切换谷歌翻译")
                        fy = go
                        print("正在翻译", row[1])
                        text = fy.translate(row[1])
                        if text['Status']:
                            writer.writerow((row[0], text['Result']))
                    else:
                        exit(1)
            else:
                writer.writerow((row[0], row[1]))
