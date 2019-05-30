# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 中山二院  志明  2019-05-06 9:44
# 当前计算机登录名称 :andy
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-06 9:44'
import socket


def EnablePort(ip, port):
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        Socket.settimeout(2)
        Socket.connect((ip, port))
        print("%s的IP的端口%d已连接!" % (ip, port))

    except WindowsError:
        print("-" * 50)
        print("%s的IP的端口%d未开放!" % (ip, port))
        print("-" * 50)

    except Exception as e:
        print(e)

    finally:
        Socket.close()


if __name__ == "__main__":
    import json
    import requests
    # 获取本机电脑名
    myname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    myaddr = socket.gethostbyname(myname)
    # 获取公网ip地址
    ip_out = requests.get('http://jsonip.com').json()['ip']
    print('局域网ip:{0};本机计算机名称为:{1},公网ip地址:{2}'.format(myaddr, myname, ip_out))
    EnablePort("120.234.63.196", 3128)
    EnablePort("218.60.8.83", 3129)
