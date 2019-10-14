# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-05-23 10:32
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-23 10:32'

import re
import requests as rq
import execjs
import os
import csv

a = '''  
    function a(r) {
        if (Array.isArray(r)) {
            for (var o = 0, t = Array(r.length); o < r.length; o++)
                t[o] = r[o];
            return t
        }
        return Array.from(r)
    }
    function n(r, o) {
        for (var t = 0; t < o.length - 2; t += 3) {
            var a = o.charAt(t + 2);
            a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
            a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
            r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
        }
        return r
    }
    var i = null;
    function e(r) {
        var t = r.length;
        t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))

        var u = void 0, l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
        
        u = null !== i ? i : (i = '320305.131321201' || "") || "";
        for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
            var A = r.charCodeAt(v);
            128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
            S[c++] = A >> 18 | 240,
            S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
            S[c++] = A >> 6 & 63 | 128),
            S[c++] = 63 & A | 128)
        }
        for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
            p += S[b],
            p = n(p, F);
        return p = n(p, D),
        p ^= s,
        0 > p && (p = (2147483647 & p) + 2147483648),
        p %= 1e6,
        p.toString() + "." + (p ^ m)
    }
    '''


def main():
    import time
    import random
    from SuTranslate.UserAgentInfos import UserAgentInfos
    url = "https://fanyi.baidu.com/"
    # response = rq.get(url, headers=header)
    headers = {'User-Agent': UserAgentInfos.GetUserAgent()}
    # 代理只针对访问的协议有关,访问http会随机选取http中的ip,若无,则使用真实ip地址
    proxies = {'https': None,
               'http': None, }
    # 使用同一Session进行调用接口,可以使请求头自动带上Cookies
    sess = rq.Session()
    response = sess.get(url=url, headers=headers, timeout=5, proxies=proxies)
    # 请求两次避免出现cookies过期,请求两次出现过期的概率极低,加上headers,否则请求头部不带上Cookies
    response = sess.get(url=url, headers=headers, timeout=5, proxies=proxies)
    # print(response.raw._connection.sock.getpeername()[0])
    # 使用正则表达式提取token
    token = re.findall(r"token: '(.*?)',", response.text)[0]
    b = execjs.compile(a)
    Text = '测试'
    sign = b.call('e', Text)
    data = {
        'from': 'zh',
        'to': 'en',
        'query': Text,
        'simple_means_flag': 3,
        'sign': sign,
        'token': token
    }
    url2 = 'https://fanyi.baidu.com/v2transapi'
    time.sleep(random.random())
    result = sess.post(url=url2, data=data, timeout=5, proxies=proxies)
    if result.status_code != 200:
        print(result)
        print("访问失败!")
        exit(1)
    print(result, result.status_code, result.json())
    # 使用随机睡眠减少被封
    import time
    import random
    for i in range(10000):
        result = sess.post(url=url2, data=data, proxies=proxies)
        print(i)
        if result.status_code != 200:
            print(result)
            break
        # print(result.json()['trans_result']['data'][0])
        print(result, result.status_code, result.json())
        t = random.random() * 2
        print(t)
        time.sleep(t)


def write_file_csv(file_name="", msg=""):
    if len(file_name.strip()) == 0 or not isinstance(file_name, (str,)):
        return {'error': 1, 'msg': '文件名称为非字符串或者为空'}
    if not isinstance(msg, (str, list, tuple, dict, set,)):
        return {'error': 2, 'msg': '要写入的内容不符合要求'}
    elif (isinstance(msg, (str,)) and len(msg.strip()) == 0) or (isinstance(msg, (list, set, tuple)) and len(msg) == 0):
        return {'error': 3, 'msg': '要写入的内容为空'}
    # 将指定的文本内容写到file_name.csv文件中
    file_name = file_name.replace(file_name[-4:], '-1.csv')
    try:
        with open(file_name, 'a', newline="") as f:
            w_csv = csv.writer(f)
            if isinstance(msg, (str,)):
                w_csv.writerow((msg,))
            else:
                w_csv.writerow((msg[0], msg[1]))
            f.close()
        return {'error': 0, 'msg': '文件写入成功!'}
    except IndexError:
        return {'error': 4, 'msg': '数组越界,请多传入几个数据!'}
    except PermissionError:
        return {'error': 5, 'msg': '文件写入权限被拒绝!'}


def read_file_csv(file_name=""):
    """
    从csv文件读取数据,返回列表
    :param file_name: 文件名
    :return:
    """
    if len(file_name.strip()) == 0 or not isinstance(file_name, (str,)):
        return {'error': 1, 'msg': '文件名称为非字符串或者为空'}
    data = list()
    with open(file_name, 'r') as f:
        r_csv = csv.reader(f)
        for row in r_csv:
            data.append(row)
        f.close()
    return {'error': 1, 'msg': '文件名称为非字符串或者为空', 'result': data}


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
    file = f'c:/Users/andy/Desktop/zh_CN.locale.csv'
    file2 = f'c:/Users/andy/Desktop/zh_CN.locale-1.csv'
    r1 = set(read_file_csv(file)['result'])
    r2 = set(read_file_csv(file2)['result'])
    # 得到需要翻译的集合
    # r
    print(len(r))
