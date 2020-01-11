# !/usr/bin/env python3
# -*- coding:utf-8 -*-
##############################################################################
# 杭州,志明Andy,2019-12-26 17:41		    						     		 #
# 当前计算机登录名称 :andy													 #
#          项目名称 :andy										             #
#             编译器:PyCharm										             #
#           功能作用:根据xls文件进行定制化数据,进行一键导入数据					 #
##############################################################################
import json
import time

import pandas as pd
from tqdm import tqdm

import utils
from ElasticSearchImporter import ElasticSearchImporter as es


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


def write_define(e, _id, master_def_name, data_type, dir_name, index_name_define, doc_type_define):
    content = {
        "IS_ENABLE": "1",
        "MASTER_DEF_DESC": master_def_name,
        "PY": utils.get_py(master_def_name),
        "IS_PUBLISH_DEF": "0",
        "MASTER_DEF_CODE": utils.get_py(master_def_name),
        "STANDARD_ID": "",
        "MASTER_DEF_ID": utils.get_uuid(),
        "CREATOR_ID": "10000",
        "MASTER_DIR_ID": _id,
        "DELETE_FLAG": "0",
        "STANDARD_NAME": "-",
        "MASTER_DEF_NAME": master_def_name,
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


def write_property(e, _id, name, dic_property, index_name_property, doc_type_property):
    """
    :param e:
    :param _id:
    :param name:
    :param dic_property:
    :param index_name_property:
    :param doc_type_property:
    :return:
    """
    es_common_property = {
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
    # dic_property ={"code": "值",  "name": "值含义", "desc": "说明"}
    # 人员档案
    # dic_property = {"code": "工号", "name": "姓名", "desc": "说明", "id_card": "身份证号",
    #                 "iphone": "手机号码", "tel": "电话号码", "sex": "性别", "dept_name": "所在科室",
    #                 "finance_name": "财务科室", "attendance_group": "考勤组", "type": "职工类别"}

    index = 0
    # 遍历写入属性至属性表
    for key, value in dic_property.items():
        es_common_property['MASTER_PRO_ID'] = utils.get_uuid()
        es_common_property['MASTER_PRO_CODE'] = key.upper()
        es_common_property['MASTER_PRO_NAME'] = value
        es_common_property['SORT'] = index
        es_common_property[
            'CREATE_TIME'] = f'{time.strftime("%Y-%m-%d", time.localtime())}T{time.strftime("%H:%M:%S", time.localtime())}+08:00'
        e.insert_data_list(index_name=index_name_property, doc_type=doc_type_property,
                           data_dict={es_common_property['MASTER_PRO_ID']: es_common_property})
        index += 1
    return len(dic_property)


def write_member(e, parent_id, parent_name, data, dic_property, index_name_member, doc_type_member):
    flag_change = False
    es_data = {
        "MASTER_DEF_ID": parent_id,
        "MASTER_DEF_CODE": utils.get_py(parent_name),
        "MASTER_DEF_NAME": parent_name,
        "MEMBER": {"DELETE_FLAG": "0", "STATUS": "2",
                   "IS_ENABLE": "1",
                   "CREATOR_NAME": "zhiming", "MASTER_DEF_ID": parent_id,
                   "CREATOR_ID": "10000"},
        "STATUS": "2",
        "IS_ENABLE": "1",
        "CREATE_TIME": "2019-03-22T08:50:11.7651577Z",
        "CREATOR_ID": "10000",
        "CREATOR_NAME": "zhiming",
        "DELETE_FLAG": "0"}

    for d in data:
        if data.index(d) > 0 and flag_change:
            es_data["MEMBER"] = json.loads(es_data["MEMBER"])
            # 准备数据
        es_data["MASTER_MEMBER_ID"] = utils.get_uuid()
        es_data["PY"] = utils.get_py(d.get("姓名"))

        for key, value in dic_property.items():
            es_data["MEMBER"][key.upper()] = d.get(value) if d.get(value) is not None else ""

        es_data["MEMBER"]["PY"] = es_data["PY"]
        es_data["MEMBER"]["CREATE_TIME"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        es_data["MEMBER"]["MASTER_MEMBER_ID"] = es_data["MASTER_MEMBER_ID"]
        es_data["MEMBER"]["SORT"] = data.index(d)
        es_data["SORT"] = data.index(d)
        es_data["CREATE_TIME"] = f'{time.strftime("%Y-%m-%d", time.localtime())}T' \
                                 f'{time.strftime("%H:%M:%S", time.localtime())}+08:00'

        print(f"正在写入第{data.index(d) + 1}条记录...\n{es_data}")
        es_data["MEMBER"] = json.dumps(es_data["MEMBER"], ensure_ascii=False)

        # 写入数据到es
        e.insert_data_list(index_name=index_name_member, doc_type=doc_type_member,
                           data_dict={es_data["MASTER_MEMBER_ID"]: es_data})
        flag_change = True
        # break


def read_excel_all(excel_path: str):
    xls = pd.read_excel(excel_path, keep_default_na="")
    # 获取列名
    xls_title = xls.columns.tolist()
    # 根据第1列升序排序
    xls = xls.sort_values(xls_title[0], ascending=True)
    data = list()
    # 配置进度条
    # pbar = tqdm(total=len(xls.values))
    # pbar.set_description("文件读取完成进度")
    # 使用上下文管理器进行打印进度条,防止出现多行进度条问题
    with tqdm(total=len(xls.values)) as bar:
        bar.set_description("文件读取完成进度")
        for content in xls.values:
            ctn = dict()
            for title in xls_title:
                ctn[title] = content[xls_title.index(title)]
            data.append(ctn)
            bar.update(1)
            # time.sleep(0.01)
        # break
    # 进度条使用完成后关闭
    # pbar.close()

    return xls_title, data


def main():
    path = r"C:\Users\andy\Desktop\厂商字典\人员档案.xls"
    name = "人员信息表"
    e = es(host="127.0.0.1", port=9200)
    dic_property = {"code": "工号", "name": "姓名", "id_card": "身份证号",
                    "iphone": "移动电话", "tel": "工作电话", "sex": "性别", "dept_name": "所在科室",
                    "finance_name": "财务科室", "attendance_group": "考勤组", "type": "职工类别"}

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
    index_name_member = json_data.get('index_name_member')
    doc_type_member = json_data.get('doc_type_member')

    # 读取excel数据
    title, data = read_excel_all(excel_path=path)

    # 删除已有数据
    deleted_count_pro, delete_count_men = delete_record(e, id_dir, name, index_name_define=index_name_define,
                                                        doc_type_define=doc_type_define,
                                                        index_name_property=index_name_property,
                                                        doc_type_property=doc_type_property,
                                                        index_name_menber=index_name_member,
                                                        doc_type_menber=doc_type_member)
    # 写数据到定义表
    MASTER_DEF_ID = write_define(e=e, _id=id_dir, master_def_name=name, data_type=data_type, dir_name=dir_name,
                                 index_name_define=index_name_define, doc_type_define=doc_type_define)
    print(MASTER_DEF_ID)
    # 写数据到属性表
    write_property(e, _id=MASTER_DEF_ID, name=name, dic_property=dic_property, index_name_property=index_name_property,
                   doc_type_property=doc_type_property)
    # 写数据到成员表
    write_member(e=e, parent_id=MASTER_DEF_ID, parent_name=name, data=data, dic_property=dic_property,
                 index_name_member=index_name_member, doc_type_member=doc_type_member)

    print({"error": 0, "msg": f"处理数据成功!(备注:属性表删除{deleted_count_pro}条记录,成员表删除{delete_count_men}条记录,"
                              f"增加属性{len(dic_property)}条,成员表增加{len(data)}条记录;id:{MASTER_DEF_ID})"})


if __name__ == "__main__":
    import Timer
    from pprint import pprint
    with Timer.Timer.timer():
        print("程序正在处理...")
        time.sleep(0.1)
        # main()
        path = r"C:\Users\andy\Desktop\厂商字典\人员档案.xls"
        pprint(read_excel_all(excel_path=path)[0])
