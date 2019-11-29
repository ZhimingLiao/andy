# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-11-15 17:55
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm

import os
import time
# 生成32位uuid
import uuid

# excel文件读取操作工具包
import xlrd as xd
# 汉字转拼音
from pypinyin import pinyin


# 生成32位uuid
def get_uuid():
    return "".join(str(uuid.uuid4()).split("-")).lower()


def get_py(char=None):
    if not char:
        return None
    data = ""
    for value in pinyin(char, style=0):
        data += value[0][0].upper()
    return data


def d():
    i, tmp = 0, None
    for d in datas:
        uid = get_uuid()
        if tmp == d.get("ws_code"):
            i += 1
        else:
            i = 1
        tmp = d.get("ws_code")
        ds = {"MASTER_MEMBER_ID": uid, "MASTER_DEF_ID": "0e1e053f-e2b2-45ed-9677-d9c8195e0751",
              "MASTER_DEF_CODE": d.get("ws_code"), "MASTER_DEF_NAME": d.get("name"), "PY": get_py(d.get("name")),
              "SORT": i, "STATUS": "6",
              "IS_ENABLE": "1", "CREATE_TIME": "2019-11-22T10:07:59.4390653Z", "CREATOR_ID": "1",
              "CREATOR_NAME": "系统管理员",
              "LAST_MODIFY_TIME": "null", "LAST_MODIFIER_ID": "null", "LAST_MODIFIER_NAME": "null", "DELETE_FLAG": "0",
              "MEMBER": {"DELETE_FLAG": "0", "SORT": "6", "MASTER_MEMBER_ID": uid,
                         "LAST_MODIFIER_NAME": "null", "LAST_MODIFY_TIME": "null", "PY": get_py(d.get("name")),
                         "STATUS": "6", "IS_ENABLE": "1",
                         "CODE": "9", "CREATE_TIME": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                         "NAME": d.get("value"), "LAST_MODIFIER_ID": "null",
                         "CREATOR_NAME": "系统管理员", "MASTER_DEF_ID": "0e1e053f-e2b2-45ed-9677-d9c8195e0751",
                         "CREATOR_ID": "1"}}
        print(ds)


if __name__ == "__main__":
    file_path = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\卫生信息数据元值域代码WS364.xls"
    # 1, 判断文件是否存在,不存在则直接跳出
    if not os.path.exists(file_path):
        print('温馨提示:\n不存在需要处理的文件:{0}'.format(file_path))
        exit(1)
    f = xd.open_workbook(file_path).sheet_by_index(0)
    datas = list()
    # 2,数据提取到列表中,f.nrows
    for row in range(1, f.nrows):
        # 获取表格第一列和第二列里面值并且格式处理
        # r1 = str(f.row(row)[0].value).strip()
        # print(row, r1)
        # data.append(r1)
        if not f.row(row)[1].value:
            print("遇到空格...")
            continue
        print("正在打印...", f.row(row)[1].value, f.row(row)[2].value, f.row(row)[3].value,
              f.row(row)[4].value, f.row(row)[5].value, f.row(row)[6].value)
        datas.append({"ws_code": f.row(row)[1].value, "name": f.row(row)[2].value, "code": f.row(row)[3].value,
                      "value": f.row(row)[4].value, "version": f.row(row)[5].value, "desc": f.row(row)[6].value})
    del row, f
    # print(datas[len(datas)-1], len(datas))
    frequency = dict()
    newer = set()
    for word in datas:
        if word.get("name") not in frequency:
            frequency[word.get("name")] = 1
        else:
            frequency[word.get("name")] += 1
        newer.add(word.get("name"))
    print(len(newer), newer)
    from test_es import EsToolor

    es = EsToolor()
    data = es.get_data().get("result")
    data = sorted(data, key=lambda val: val.get("_source").get("DATA_TYPE")[0], reverse=False)
    newer2 = set()
    for w in data:
        newer2.add(w.get("_source").get("MASTER_DEF_NAME"))
    print(len(data), newer2 - newer)
