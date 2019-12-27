# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-12-12 17:27
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
# 读取excel数据,然后写入es数据库操作
import json
import os
import time

import pandas as pd

import utils
from ElasticSearchImporter import ElasticSearchImporter as es
from Timer import Timer


def read_excel(path_excel):
    # 根据xls路径, 根据列名读取里面数据
    try:
        xls = pd.read_excel(io=path_excel, sheet_name=[0], index_col=None, keep_default_na="",
                            usecols=['序号', '值', "值含义", "说明"])
    # 打印标题, .columns.values
    # print(xls[0].columns.values)
    # 打印数据
    # print(xls[0].values)
    # 打印数据样式

    # 遍历xls数据
    # for xl in xls[0].values:
    #     print(xl)
    # break
    except (ValueError, Exception) as e:
        error = 401
        msg = f"文件内容不对,请检查!(备注:{e})"
        detail = ""
    else:
        data_list = [(xl[0], xl[1], xl[2], xl[3]) for xl in xls[0].values]
        error = 0
        msg = "获取数据成功!"
        detail = data_list
    finally:
        return {"error": error, "msg": msg, "detail": detail}


def write_define(e, _id, dir_name, data_type, MASTER_DEF_NAME, index_name_define, doc_type_define):
    content = {
        "IS_ENABLE": "1",
        "MASTER_DEF_DESC": MASTER_DEF_NAME,
        "PY": utils.get_py(MASTER_DEF_NAME),
        "IS_PUBLISH_DEF": "0",
        "MASTER_DEF_CODE": utils.get_py(MASTER_DEF_NAME),
        "STANDARD_ID": "",
        "MASTER_DEF_ID": utils.get_uuid(),
        "CREATOR_ID": "10000",
        "MASTER_DIR_ID": _id,
        "DELETE_FLAG": "0",
        "STANDARD_NAME": "-",
        "MASTER_DEF_NAME": MASTER_DEF_NAME,
        "SORT": 0,
        "CREATOR_NAME": "zhiming",
        "MASTER_PRO_VERSION_NO": "1",
        "CREATE_TIME": f'{time.strftime("%Y-%m-%d", time.localtime())}T{time.strftime("%H:%M:%S", time.localtime())}+08:00',
        "IS_PUBLISH_MEMBER": "0",
        "DATA_TYPE": data_type,
        "MASTER_DIR_NAME": dir_name,
        "MASTER_MEMBER_VERSION_NO": "0"
    }
    e.insert_data_list(index_name=index_name_define, doc_type=doc_type_define,
                       data_dict={content['MASTER_DEF_ID']: content})
    return content['MASTER_DEF_ID']


def write_property(e, _id, name, index_name_property, doc_type_property):
    """
    写数据到属性表
    :param e:
    :param id:
    :param name:
    :return:
    """
    es_code = {
        "MASTER_DEF_ID": _id,
        "MASTER_DEF_CODE": utils.get_py(name),
        "MASTER_DEF_NAME": name,
        "MASTER_PRO_ID": utils.get_uuid(),
        "MASTER_PRO_CODE": "CODE",
        "MASTER_PRO_NAME": "值",
        "MASTER_PRO_DESC": " null",
        "MASTER_PRO_DATATYPE": "String",
        "MASTER_PRO_LENGTH": 100,
        "MASTER_PRO_DEFAULT_VALUE": "null",
        "MASTER_PRO_MANDATORY": 1,
        "MASTER_PRO_CONTROL_TYPE": "input",
        "META_DEF_REL_ID": "null",
        "META_DEF_REL_NAME": " null",
        "SORT": 0,
        "CREATE_TIME": f'{time.strftime("%Y-%m-%d", time.localtime())}T{time.strftime("%H:%M:%S", time.localtime())}+08:00',
        "CREATOR_ID": "10000",
        "CREATOR_NAME": "zhiming",
        "IS_ENABLE": "1",
        "DELETE_FLAG": "0"
    }
    e.insert_data_list(index_name=index_name_property, doc_type=doc_type_property,
                       data_dict={es_code['MASTER_PRO_ID']: es_code})
    es_name = {
        "MASTER_DEF_ID": _id,
        "MASTER_DEF_CODE": utils.get_py(name),
        "MASTER_DEF_NAME": name,
        "MASTER_PRO_ID": utils.get_uuid(),
        "MASTER_PRO_CODE": "NAME",
        "MASTER_PRO_NAME": "值含义",
        "MASTER_PRO_DESC": " null",
        "MASTER_PRO_DATATYPE": "String",
        "MASTER_PRO_LENGTH": 100,
        "MASTER_PRO_DEFAULT_VALUE": "null",
        "MASTER_PRO_MANDATORY": 1,
        "MASTER_PRO_CONTROL_TYPE": "input",
        "META_DEF_REL_ID": "null",
        "META_DEF_REL_NAME": " null",
        "SORT": 1,
        "CREATE_TIME": f'{time.strftime("%Y-%m-%d", time.localtime())}T{time.strftime("%H:%M:%S", time.localtime())}+08:00',
        "CREATOR_ID": "10000",
        "CREATOR_NAME": "zhiming",
        "IS_ENABLE": "1",
        "DELETE_FLAG": "0"
    }
    e.insert_data_list(index_name=index_name_property, doc_type=doc_type_property,
                       data_dict={es_name['MASTER_PRO_ID']: es_name})
    es_desc = {
        "MASTER_DEF_ID": _id,
        "MASTER_DEF_CODE": utils.get_py(name),
        "MASTER_DEF_NAME": name,
        "MASTER_PRO_ID": utils.get_uuid(),
        "MASTER_PRO_CODE": "DESC",
        "MASTER_PRO_NAME": "说明",
        "MASTER_PRO_DESC": 'null',
        "MASTER_PRO_DATATYPE": "String",
        "MASTER_PRO_LENGTH": 500,
        "MASTER_PRO_DEFAULT_VALUE": 'null',
        "MASTER_PRO_MANDATORY": 1,
        "MASTER_PRO_CONTROL_TYPE": "input",
        "META_DEF_REL_ID": 'null',
        "META_DEF_REL_NAME": 'null',
        "SORT": 2,
        "CREATE_TIME": f'{time.strftime("%Y-%m-%d", time.localtime())}T{time.strftime("%H:%M:%S", time.localtime())}+08:00',
        "CREATOR_ID": "10000",
        "CREATOR_NAME": "zhiming",
        "IS_ENABLE": "1",
        "DELETE_FLAG": "0"}
    e.insert_data_list(index_name=index_name_property, doc_type=doc_type_property,
                       data_dict={es_desc["MASTER_PRO_ID"]: es_desc})


def write_menber(e, _id, data, index_name_menber, doc_type_menber):
    flag_change = False
    es_data = {"MASTER_MEMBER_ID": None,
               "MASTER_DEF_ID": _id,
               "MASTER_DEF_CODE": utils.get_py(data[0]),
               "MASTER_DEF_NAME": data[0],
               "PY": "JSZ",
               "MEMBER": {"DELETE_FLAG": "0", "SORT": None,
                          "MASTER_MEMBER_ID": None, "PY": None, "STATUS": "2",
                          "IS_ENABLE": "1", "CODE": None, "DESC": None, "CREATE_TIME": None, "NAME": None,
                          "CREATOR_NAME": "zhiming", "MASTER_DEF_ID": _id,
                          "CREATOR_ID": "10000"},
               "SORT": None,
               "STATUS": "2",
               "IS_ENABLE": "1",
               "CREATE_TIME": "2019-03-22T08:50:11.7651577Z",
               "CREATOR_ID": "10000",
               "CREATOR_NAME": "zhiming",
               "DELETE_FLAG": "0"}
    for d in data[1]:
        if d[1] == "" and d[2] == "":
            continue
        if data[1].index(d) > 0 and flag_change:
            es_data["MEMBER"] = json.loads(es_data["MEMBER"])
            # 准备数据
        es_data["MASTER_MEMBER_ID"] = utils.get_uuid()
        es_data["PY"] = utils.get_py(d[2])
        es_data["MEMBER"]["NAME"] = d[2]
        es_data["MEMBER"]["PY"] = utils.get_py(d[2])
        es_data["MEMBER"]["CODE"] = d[1]
        es_data["MEMBER"]["CREATE_TIME"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        es_data["MEMBER"]["MASTER_MEMBER_ID"] = es_data["MASTER_MEMBER_ID"]
        es_data["MEMBER"]["SORT"] = data[1].index(d)
        es_data["MEMBER"]["DESC"] = d[3]
        es_data["SORT"] = data[1].index(d)
        es_data[
            "CREATE_TIME"] = f'{time.strftime("%Y-%m-%d", time.localtime())}T{time.strftime("%H:%M:%S", time.localtime())}+08:00'

        es_data["MEMBER"] = json.dumps(es_data["MEMBER"], ensure_ascii=False)
        # 写入数据到es
        e.insert_data_list(index_name=index_name_menber, doc_type=doc_type_menber,
                           data_dict={es_data["MASTER_MEMBER_ID"]: es_data})
        flag_change = True
        # break


def delete_record(e, _id, name, index_name_define, doc_type_define, index_name_property, doc_type_property,
                  index_name_menber, doc_type_menber):
    ranges = e.search_by_body(index_name=index_name_define, MASTER_DIR_ID=_id)["hits"]["hits"]
    flag_exist = False
    deleted_count_pro = 0
    delete_count_men = 0

    if not ranges:
        return deleted_count_pro, delete_count_men

    for r in ranges:
        if r['_source']['MASTER_DEF_NAME'] == name:
            es_deleted_id = r['_id']
            flag_exist = True
            break

    if not flag_exist:
        return deleted_count_pro, delete_count_men

    # 1.删除表记录
    e.delete_data_by_id(index_name=index_name_define, doc_type=doc_type_define, id=es_deleted_id)
    # 2.删除属性表记录
    res_pro = e.search_by_body(index_name=index_name_property, MASTER_DEF_ID=es_deleted_id)["hits"]["hits"]
    for r in res_pro:
        e.delete_data_by_id(index_name=index_name_property, doc_type=doc_type_property, id=r['_id'])
        deleted_count_pro += 1

    # 3.删除成员表数据
    res_menb = e.search_by_body(index_name=index_name_menber, MASTER_DEF_ID=es_deleted_id)["hits"]["hits"]
    for r in res_menb:
        e.delete_data_by_id(index_name=index_name_menber, doc_type=doc_type_menber, id=r['_id'])
        delete_count_men += 1

    return deleted_count_pro, delete_count_men


def deal_data(ip, port, data):
    e = es(host=ip, port=port)
    # 目录id
    # 读取参数
    config_path = "config.json"
    json_data = utils.input_json_data_from_file(config_path)
    if json_data.get("error"):
        return {"error": json_data.get("error"), "msg": json_data.get("msg")}
    id_dir = json_data.get('id_dir')
    dir_name = json_data.get("dir_name")
    data_type = json_data.get("data_type")
    index_name_define = json_data.get('index_name_define')
    doc_type_define = json_data.get('doc_type_define')
    index_name_property = json_data.get('index_name_property')
    doc_type_property = json_data.get('doc_type_property')
    index_name_menber = json_data.get('index_name_menber')
    doc_type_menber = json_data.get('doc_type_menber')

    # 删除已有数据
    deleted_count_pro, delete_count_men = delete_record(e, id_dir, data[0], index_name_define=index_name_define,
                                                        doc_type_define=doc_type_define,
                                                        index_name_property=index_name_property,
                                                        doc_type_property=doc_type_property,
                                                        index_name_menber=index_name_menber,
                                                        doc_type_menber=doc_type_menber)
    # 写数据到定义表
    MASTER_DEF_ID = write_define(e, id_dir, dir_name, data_type, data[0], index_name_define=index_name_define,
                                 doc_type_define=doc_type_define)
    # 写数据到属性表
    write_property(e, _id=MASTER_DEF_ID, name=data[0], index_name_property=index_name_property,
                   doc_type_property=doc_type_property)
    # 写数据到成员表
    write_menber(e, MASTER_DEF_ID, data, index_name_menber=index_name_menber, doc_type_menber=doc_type_menber)
    return {"error": 0, "msg": f"处理数据成功!(备注:属性表删除{deleted_count_pro}条记录,成员表删除{delete_count_men}条记录,"
                               f"增加属性3条,成员表增加{len(data[1])}条记录;id:{MASTER_DEF_ID})"}


def main(file_path, addr):
    file_path = file_path.strip()
    addr = addr.strip()
    if not all((file_path, addr,)):
        error = 401
        msg = f'参数不正确;(备注:传入的参数是<{file_path, addr}>)'
        return {'error': error, 'msg': msg}

    # 提取ip和端口
    res = utils.string_to_ip_port(addr)
    ip, port = res['detail'][0][0], int(res['detail'][1])

    # 测试IP和端口是否可用
    res = utils.test_port_use(ip, port)
    if res['error'] > 0:
        return {"error": 501, "msg": res['msg']}

    # 读取excel获取数据
    res = read_excel(file_path)
    # print(res)
    if res["error"] > 0:
        return {"error": 402, "msg": res['msg']}
    data_list = res["detail"]

    # 写数据到es数据库
    res = deal_data(ip, port, (os.path.splitext(os.path.split(file_path)[1])[0], data_list))

    return {"error": 0, "msg": res['msg']}


def read_excel_all(excel_path):
    xls = pd.read_excel(io=excel_path, keep_default_na="")
    xls_title = xls.columns.tolist()
    print(xls_title, type(xls.values()))
    for content in xls.values:
        print(content)
        break


if __name__ == "__main__":
    path_excel = r"C:\Users\andy\Desktop\厂商字典\人员档案.xls"
    with Timer.timer():
        res = read_excel_all(path_excel)
        # res = pd.read_excel(path_excel)
        # res = delete_record(es(host="127.0.0.1", port=9200), id="437403E4835C43E6B58316CF03605568",
        #                     name="妊娠终止方式代码表test")
        print(res)
