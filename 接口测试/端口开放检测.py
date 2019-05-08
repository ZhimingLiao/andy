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
    # 获取本机电脑名
    myname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    myaddr = socket.gethostbyname(myname)
    print('本机ip:{0};本机计算机名称为:{1}'.format(myaddr, myname))
    print("-" * 50)
    EnablePort("192.168.6.2", 3300)
    EnablePort("192.168.6.188", 3100)
    EnablePort("192.168.111.165", 5020)
    # EnablePort("192.168.111.220", 5715)
    EnablePort("192.168.6.189", 5715)
