# -*- coding:utf-8 -*-
# 志明
__author__ = '广州医科大学附属第五医院'
__time__ = '2018-11-22 20:34'

import os
import time


# import sys


class PingTools:

    @staticmethod
    def getEnableIPS(StartIP, EndIP):
        StartIP = StartIP.lstrip().rstrip()
        EndIP = EndIP.lstrip().rstrip()

        if len(StartIP) > 19 or len(StartIP) < 7 or len(EndIP) > 19 or len(EndIP) < 7:
            return {'Code': '1', 'Desc': 'ip地址不对!'}

        IPEnable = []
        IP1 = StartIP.split('.')[0]
        IP2 = StartIP.split('.')[1]
        IP3 = StartIP.split('.')[2]
        IP4 = StartIP.split('.')[-1]
        IPend_last = EndIP.split('.')[-1]

        if IP1 != EndIP.split('.')[0] or IP2 != EndIP.split('.')[1] or IP3 != EndIP.split('.')[2]:
            return {'Code': '2', 'Desc': 'ip地址不在同一个网段!'}
        count_True = 0

        if int(IP1) > 255 or int(IP1) < 0 or int(IP2) > 255 or int(IP2) < 0 or int(IP3) > 255 or \
                int(IP3) < 0 or int(IP3) > 255 or int(IP3) < 0 or int(EndIP.split('.')[0]) < 0 or int(
            EndIP.split('.')[0]) > 255 or \
                int(EndIP.split('.')[1]) < 0 or int(EndIP.split('.')[1]) > 255 or int(EndIP.split('.')[2]) < 0 or int(
            EndIP.split('.')[2]) > 255 \
                or int(EndIP.split('.')[3]) < 0 or int(EndIP.split('.')[3]) > 255:
            return {'Code': '3', 'Desc': 'ip地址不正确!'}

        for ip in range(int(IP4), int(IPend_last) + 1):
            ip = str(IP1 + '.' + IP2 + '.' + IP3 + '.' + str(ip))
            return1 = os.system('ping -n 1 -w 1 {0}'.format(ip))
            if return1:
                # print('ping{0}失败,此IP不可用!'.format(ip))
                # count_False += 1
                IPEnable.append(ip)
            else:
                # print('ping{0},此IP可用!'.format(ip))
                # ip_True.write(ip+'\n')
                count_True += 1
        return {'Code': '0', 'Desc': '', 'IPS': IPEnable, 'CountTrue': count_True}


if __name__ == '__main__':
    print('欢迎使用Ping测试工具!')
    import socket

    # 获取本机电脑名
    myname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    myaddr = socket.gethostbyname(myname)
    print('本机ip:{0},本机计算机名称为:{1}'.format(myaddr, myname))
    while True:
        # StartIP = (input(u'请输入起始查询IP： '))
        # EndIP = input(u'请输入终止查询IP： ')
        StartIP = "192.168.6.2"
        EndIP = "192.168.6.220"
        Result = PingTools.getEnableIPS(StartIP, EndIP)
        if Result['Code'] == '0':
            print('可用IP为:{0},共计{1}个'.format(Result['IPS'], Result['CountTrue']))
        else:
            print(PingTools.getEnableIPS(StartIP, EndIP)['Desc'])
        print('*' * 30)
        if input('是否退出...y/n:').lstrip().rstrip() == 'y':
            break
    input('按回车键退出...')
