# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-11-20 12:39
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm

import json
import os
import socket
# 生成32位uuid
import uuid

import xlrd
# 汉字转拼音
from pypinyin import pinyin


# 生成32位uuid
def get_uuid():
    """
    自动生成32位uuid,并且已经转小写
    :return: 小写uuid
    """
    return "".join(str(uuid.uuid4()).split("-")).lower()


def get_py(char=None):
    """
    根据传入中文提取中文首字母大写
    :param char: 需要提取的中文
    :return: 汉字首字母大写
    """
    if not char:
        return None
    data = ""
    for value in pinyin(char, style=0):
        data += value[0][0].upper()
    return data


def get_data(file_name):
    """
    根据文件路径提取excle里面的code和name
    :param file_name:
    :return:
    """
    result = list()
    if not os.path.exists(file_name):
        return {"error": 1, "msg": f"文件路径:{file_name},不存在!"}
    files_xls = xlrd.open_workbook(file_name)
    for name in files_xls.sheet_names():
        sheet = files_xls.sheet_by_name(name)
        for row in range(1, sheet.nrows):
            result.append({"CODE": int(sheet.row(row)[0].value) if isinstance(sheet.row(row)[0].value, (float,))
            else sheet.row(row)[0].value, "NAME": sheet.row(row)[1].value})

    return result


def string_to_ip_port(string):
    """
    从url地址中提取ip和端口号
    :param string: url地址
    :return:
    """
    import re
    # ip_port_format = ('(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.'
    #                   '(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.'
    #                   '(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.'
    #                   '(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\:'
    #                   '(\d+/)')
    # res = re.findall(ip_port_format, string.replace("localhost", "127.0.0.1"))
    # return ".".join(res[0][0:4]), int(res[0][4].replace(r"/", "").strip())
    if not string[7:8].isdigit():
        error = 401
        msg = "参数错误"
        return {"error": error, "msg": msg}
    port = string.split(':')[2].split('/')[0]  # 端口号
    mode = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    ip = mode.findall(string)
    return {"error": 0, "msg": "处理成功!", "detail": (ip, port)}


def test_port_use(ip, port):
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
        return {'error': error, 'msg': f'ip:{ip};端口号{port}连接成功' if error < 1 else f'ip:{ip};端口号:{port}未开放',
                'detail': result}


def input_json_data_from_file(path):
    """
    从文件中获取json数据
    :param path: 文件路径
    :return json_data: 返回转换为json格式后的json数据
    """
    try:
        with open(path, 'r+', encoding="utf8") as f:
            try:
                json_data = json.load(f)
            except Exception as e:
                # print('json数据格式不正确：' + str(e))
                return {"error": 401, "msg": f"配置文件config.json;json格式出错;请检查数据"}
        return json_data
    except Exception as e:
        return {"error": 402, "msg": f"当前目录下没有{path}文件"}


if __name__ == "__main__":
    # res = get_data(r"C:\Users\andy\Desktop\test.xlsx")
    # print(res)
    res = input_json_data_from_file("config.json")
    print(res)
    # pass
