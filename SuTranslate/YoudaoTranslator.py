# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-05-22 14:20
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-22 14:20'

import requests
import hashlib
import time
from time import perf_counter
from contextlib import contextmanager
import random
from SuTranslate.Logger import Logger
import json

from SuTranslate.UserAgentInfos import UserAgentInfos


class YoudaoTranslator(object):
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    S = "fanyideskweb"
    r = str(int(time.time() * 1000) + random.randint(1, 10))
    D = "ebSeFb%=XZ%T[KZ)c(sy!"

    def __init__(self) -> None:
        super().__init__()
        self.headers = {
            "User-Agent": UserAgentInfos.GetUserAgent(),
            "Referer": "http://fanyi.youdao.com/",
            "Cookie": "OUTFOX_SEARCH_USER_ID=-1038070705@10.168.8.63; JSESSIONID=aaaP2Qy4ztAfyfZRXzktw; "
                      "OUTFOX_SEARCH_USER_ID_NCOO=570232601.9713346; fanyi-ad-id=47865; fanyi-ad-closed=1; ___"
                      "rl__test__cookies=1532406668184"}

    def translate(self, text):
        sign = hashlib.md5((self.S + text + self.r + self.D).encode('utf-8')).hexdigest()
        data = {"i": text,
                "from": "AUTO",
                "to": "AUTO",
                "smartresult": "dict",
                "client": "fanyideskweb",
                "salt": self.r,
                "sign": sign,
                "doctype": "json",
                "version": "2.1",
                "keyfrom": "fanyi.web",
                "action": "FY_BY_CLICKBUTTION",
                "typoResult": "false"}
        response = requests.post(self.url, headers=self.headers, data=data).content.decode('utf-8')
        try:
            result = json.loads(response)["translateResult"][0][0]["tgt"]
        except json.decoder.JSONDecodeError as e:
            # Logger().exception("JSON解析出错")
            return {"error": 2, "msg": "有道翻译接口被封!请稍后尝试,或者请切换到其它翻译接口!"}
        else:
            if not result:
                return {"error": 1, "msg": "有道翻译失败"}
            return {"error": 0, "msg": "有道翻译成功", "result": result}


@contextmanager
def times():
    """统计代码运行耗时 """

    try:
        start = perf_counter()
        yield
    finally:
        end = perf_counter()
        print(f'{end - start}秒')


if __name__ == '__main__':
    from SuTranslate.Timer import Timer

    yd = YoudaoTranslator()

    with Timer.timer():
        for i in range(10000):
            result = yd.translate('test')
            print(i, result)
            if int(result['error']) > 0:
                break
            time.sleep(random.random() * 2)
