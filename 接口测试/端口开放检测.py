# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 中山二院  志明  2019-05-06 9:44
# 当前计算机登录名称 :andy
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-06 9:44'
import socket


def do_port(ip='192.168.6.71', port=3300):
    '''
    检测指定的IP的端口是否开启监听
    :param ip: 测试ip地址
    :param port: 连接的端口号
    :return: 处理结果
    '''
    # 使用TCP连接方式
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        st.settimeout(2)
        st.connect((ip, port))
        # print("%s的IP的端口%d已连接!" % (ip, port))
    except WindowsError:
        result = False
        error = 1
    except Exception as e:
        result = False
        error = 2
    else:
        result = True
        error = 0
    finally:
        st.close()
        return {'error': error, 'msg': f'ip:{ip};端口号{port}连接成功' if error < 1 else f'ip:{ip};端口号{port}未开放',
                'result': result}


# 创建TCP套接字对象
def tcp_create(ip='192.168.111.176', port=3600):
    if do_port(ip=ip, port=port).get('error') > 0:
        return {'error': 3, 'msg': '远程ip或端口积极拒绝访问'}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return {'error': 0, 'msg': '套接字对象创建成功!', 'result': sock}


# 使用socket对象进行发送数据
def tcp_send(sock=None, datas=None, start=b'\x0b', end=b'\x1c'):
    '''
    使用指定的套接字对象发送字节码数据;适用于已经创建的套接字,原型来自于hl7消息测试
    :param sock: 套接字对象
    :param datas: 二进制数据
    :param start: 开始标识符
    :param end: 结束标识符
    :return:
    '''
    # 1. 对入参进行过滤处理
    if not sock:
        return {'error': 1, 'msg': '套接字对象Socket未提供!'}
    if not all((isinstance(datas, (bytes,)), isinstance(start, (bytes,)), isinstance(end, (bytes,)))):
        return {'error': 2, 'msg': '传入的参数含有非字节码!'}

    # 2. 发送数据到指定ip和端口
    sock.send(datas)
    # 循环接受套接字数据
    while True:
        rec = sock.recv(1024)
        if rec: break
    # print(t[t.find(b'\x0b')+1:t.find(b'\x1c')])
    sock.close()
    return {'error': 0, 'msg': '成功接受到数据!', 'result': rec[rec.find(start) + 1: rec.find(end)]}


if __name__ == "__main__":
    # import json
    # import requests
    # # 获取本机电脑名
    # myname = socket.getfqdn(socket.gethostname())
    # # 获取本机ip
    # myaddr = socket.gethostbyname(myname)
    # # 获取公网ip地址
    # ip_out = requests.get('http://jsonip.com').json()['ip']
    # print('局域网ip:{0};本机计算机名称为:{1},公网ip地址:{2}'.format(myaddr, myname, ip_out))
    # # 移动输液系统TCP连接测试
    ip_test = '192.168.6.220'
    port_test = 3070
    msg2 = 'MSH|^~\\&|LIS||NHIS||20190528085648||OUL^R21|793867|P|2.4|||AL|AL\r' \
           'PID|||^^^^IDCard~^^^^IdentifyNO~^^^^Outpatient~201940226^^^^PatientNO||朱子涵|||F\r' \
           'PV1||I|^^^696^儿1科||||||0545^朱晓虎||||||||||201940226|||||||||||||||||||||||||20190522100642\r' \
           'OBR|1|1005450034391|119052258274|06671^血培养(加药敏进口仪器）^MIC||20190522113802|||||||||0002&静脉全血|||儿1科|696|||20190528085648||||||||||0729|0209\r' \
           'NTE|1\r' \
           'OBX|14140288|TX|^^^05051104^培养7天无细菌生长||||||||F|||20190528085648\r'
    sock = tcp_create(ip=ip_test, port=port_test).get('result')
    # 需要加上前后切割字符
    t = tcp_send(sock=sock, datas=msg2.encode('utf-8'))
    print(t.get('result').decode('utf-8'))
    sock.close()
