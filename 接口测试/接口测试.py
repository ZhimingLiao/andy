# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-04-15 8:48
# 当前计算机登录名称 :andy
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-04-15 8:48'

# from suds.client import Client
from SOAPpy import WSDL

if __name__ == "__main__":
    URL = "http://192.168.8.234:9000/services/HIPMessageServer?wsdl"
    test = WSDL.Proxy(URL)
    print(test.methods)
