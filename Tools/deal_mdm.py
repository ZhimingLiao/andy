# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-11-17 9:09
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm

"""
    先手工插入数据到主数据的成员表,根据数据集子集成员数据,将成员数据插回到数据元定义表
    1.根据指定的数据集名称在数据集成员中找到对应的数据元信息,放到列表中
    2.根据第一步得到的数据元数据写回到定义表中,数据目录归于数据元,固定
    3.以上数据元在属性表中每一条数据元添两条记录,分别位编码和名称
    备注,添加数据集成员时,同理需要将数据集成员数据写回到定义表中
"""
import json
import random
# 生成32位uuid
import uuid

# 汉字转拼音
from pypinyin import pinyin

# 打印日志记录
from Tools.ElasticSearchTool import Logger
from Tools.ElasticSearchTool.ElasticSearchImporter import ElasticSearchImporter


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


def deal_data_element(es_host="127.0.0.1", es_port=9200):
    """
    处理数据子集中数据元数据
    :param es_host: es ip
    :param es_port: port
    :return:
    """
    mindex_name, mdoc_tpye = "mdms.entity.masterdatamanage.master_member", "MASTER_MEMBER"
    mname = "患者基本信息子集"  # 上一级目录名称,根据名称找下一级的数据元
    mes = ElasticSearchImporter(es_host, es_port)
    # print(mes.search_size(mindex_name))
    mdata = mes.search_by_body(mindex_name, MASTER_DEF_NAME=mname).get("hits")
    mdata_newer = [json.loads(element["_source"].get("MEMBER")) for element in mdata.get("hits") if
                   json.loads(element["_source"].get("MEMBER")).get("DELETE_FLAG") == "0"]
    # print(mdata_newer)
    # 1.写回到定义表中
    insert_data_list = dict()
    for mv in mdata_newer:
        muuid = get_uuid()
        mdata = {"IS_ENABLE": "1", "MASTER_DEF_DESC": mv.get("DEFINITION"), "PY": get_py(mv.get("NAME")),
                 "LAST_MODIFY_TIME": "2019-11-22T06:19:36.9060707", "IS_PUBLISH_DEF": "1",
                 "MASTER_DEF_CODE": mv.get("CODE"), "LAST_PUBLISH_TIME": "2019-11-22T06:19:36.9060707Z",
                 "STANDARD_ID": "", "MASTER_DEF_ID": muuid,
                 "CREATOR_ID": "10000", "MASTER_DIR_ID": "455F57703B0843D7B164014B54A76F61", "LAST_MODIFIER_NAME": "",
                 "DELETE_FLAG": "0", "STANDARD_NAME": "",
                 "MASTER_DEF_NAME": mv.get("NAME"), "SORT": random.randint(30, 300), "CREATOR_NAME": "zhiming",
                 "MASTER_PRO_VERSION_NO": "0",
                 "CREATE_TIME": "2019-11-22T06:19:36.9060707Z", "IS_PUBLISH_MEMBER": "0", "LAST_MODIFIER_ID": "",
                 "DATA_TYPE": "DATASTANDARD", "MASTER_DIR_NAME": "数据元", "MASTER_MEMBER_VERSION_NO": "0"}
        insert_data_list[muuid] = mdata
    mdefine_index, mdefine_doc_type = "mdms.entity.masterdatamanage.master_definition", "MASTER_DEFINITION"
    print(f"共需要插入{len(insert_data_list)}条数据\r\n正在写入数据到索引:{mdefine_index},类型为:{mdefine_doc_type}")
    # result = mes.insert_data_list(mdefine_index, doc_type=mdefine_doc_type, data_list= insert_data_list)
    # 删除数据
    id_set_deleted = {"7033a92f1b12463db3012b98b3d85054", "d6d32a4f2d55494bacd3f2b7d950c08f"}
    result = mes.delete_data_by_id_batch(index_name=mdefine_index, doc_type=mdefine_doc_type, id_set=id_set_deleted)
    if not result.get("error"):
        print(result, f"\r\n操作了以下数据:\r\n{insert_data_list}")
    else:
        print(result)
    # print(result)"_type": "MASTER_DEFINITION",
    # 2.数据元添加属性写回到属性表中
    return None


def create_data(id, name, desc, code, data_code, v_data, v, sort, format):
    py_code = get_py(name)
    mdata = {
        "MASTER_MEMBER_ID": id,
        "MASTER_DEF_ID": "E51D74F6D748447282EA534E0C61D076",
        "MASTER_DEF_CODE": "HDSD00.02_V1.0_1",
        "MASTER_DEF_NAME": "患者基本信息子集",
        "PY": py_code,
        "MEMBER": {"MASTER_MEMBER_ID": id,
                   "DATA_ELEMENT_VALUE_DATATYPE_id": "B047628CB5454F4F8EA0B8789B77E963", "LAST_MODIFIER_ID": "1",
                   "DATA_ELEMENT_VALUE_DATATYPE": v_data, "DEFINITION": desc, "SORT": sort,
                   "MASTER_DEF_ID": "E51D74F6D748447282EA534E0C61D076", "CREATOR_ID": "1000",
                   "DATA_ELEMENT_VALUE_DATATYPE_code": v_data, "DATA_ELEMENT": name, "CREATOR_NAME": "zhiming",
                   "VALUE_RANGE": v, "STATUS": "2", "LAST_MODIFY_TIME": "2019-11-16 17:08:53", "NAME": name,
                   "CODE": code, "DELETE_FLAG": "0", "IS_ENABLE": "1", "CREATE_TIME": "2019-11-14 18:08:39",
                   "PY": py_code, "PRESENTATION_FORMAT": format, "DATA_ELEMENT_code": data_code,
                   "DATA_ELEMENT_id": "B5D0639687F04E1EA513344A167FBC82", "LAST_MODIFIER_NAME": "系统管理员"},
        "SORT": 1,
        "STATUS": "2",
        "IS_ENABLE": "1",
        "CREATE_TIME": "2018-11-14T18:08:39.1046642+08:00",
        "CREATOR_ID": "10000",
        "CREATOR_NAME": "zhiming",
        "DELETE_FLAG": "0",
        "LAST_MODIFIER_NAME": "系统管理员",
        "LAST_MODIFY_TIME": "2019-11-16T17:08:53.8974009+08:00",
        "LAST_MODIFIER_ID": "1"}
    import json
    return json.dumps(mdata, ensure_ascii=False)


def deal_data_mdm(data_element_code):
    """
    标准数据成员表,由于界面上无法维护数据元的数据,只能通过后台进行维护,故写了此方法,在界面上点击检查,找到对应id
    1.浏览器点击检查,找到_id
    2.通过get方式找到原数据GET /mdms.entity.masterdatamanage.master_member/MASTER_MEMBER/{此处为第一步的id},
        复制_soruce节点下面数据到文件data.json中
    3.调用本方法,同时传入标准的数据元节点信息,本返回会自动生成data_result.json处理后的结果
    4.复制data_result.json中文件到远程es,调用PUT /mdms.entity.masterdatamanage.master_member/MASTER_MEMBER/{此处为第一步的id}
    后面紧跟着{复制的数据}
    备注MEMBER后面记得使用三个双引号,具体参考第一步返回值
    :param data_element_code:需要修正的数据元标准编码
    :return:返回修改后的内容
    """
    mf = open(r"data.json", encoding="utf8")
    mcontent = json.load(mf)
    mf.close()
    logger.info(mcontent)
    mcontent["MEMBER"]["DATA_ELEMENT"] = mcontent["MEMBER"]["NAME"]
    mcontent["MEMBER"]["DATA_ELEMENT_code"] = data_element_code
    mcontent["MEMBER"]["CREATOR_NAME"] = "zhiming"
    mcontent["CREATOR_NAME"] = "zhiming"
    mcontent["CREATOR_ID"] = "10000"
    with open(r"data_result.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(mcontent, indent=2, ensure_ascii=False))
    return mcontent


def mdm_create_data(CODE, DE_ID, NAME, DEFINITION, TYPE, FORMAT, VALUE, VERSION="V1.0",
                    RIR="国家卫生标准委员会信息标准专业委员会", EVN_REL="卫生信息、电子病历",
                    MODE_CLS="分类法", AUTHORITY="卫生部统计信息中心", STATUS_REG="标准状态",
                    ORG_SUB="中国人民解放军第四军大学卫生信息研究院"):
    mf = open(r"data.json", encoding="utf8")
    mcontent = json.load(mf)
    mf.close()
    muuid = get_uuid()
    # 获取传入的参数
    kwargs = locals()
    logger.info(f"入参:{kwargs}\r\n")
    mcontent["MASTER_MEMBER_ID"] = muuid
    mcontent["MEMBER"]["MASTER_MEMBER_ID"] = muuid
    mcontent["MEMBER"]["CODE"] = CODE
    mcontent["MEMBER"]["DE_ID"] = DE_ID
    mcontent["MEMBER"]["NAME"] = NAME
    mcontent["MEMBER"]["DEFINITION"] = DEFINITION
    mcontent["MEMBER"]["TYPE"] = TYPE
    mcontent["MEMBER"]["FORMAT"] = FORMAT
    mcontent["MEMBER"]["VALUE"] = VALUE
    mcontent["MEMBER"]["VERSION"] = VERSION
    mcontent["MEMBER"]["RIR"] = RIR
    mcontent["MEMBER"]["EVN_REL"] = EVN_REL
    mcontent["MEMBER"]["MODE_CLS"] = MODE_CLS
    mcontent["MEMBER"]["AUTHORITY"] = AUTHORITY
    mcontent["MEMBER"]["STATUS_REG"] = STATUS_REG
    mcontent["MEMBER"]["ORG_SUB"] = ORG_SUB
    mcontent["MEMBER"]["EVN_REL"] = EVN_REL
    mcontent["MEMBER"]["PY"] = get_py(NAME)
    mcontent["MEMBER"]["CREATOR_NAME"] = "zhiming"
    mcontent["CREATOR_NAME"] = "zhiming"
    mcontent["CREATOR_ID"] = "10000"
    mcontent["PY"] = get_py(NAME)

    with open(r"data_result.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(mcontent, indent=2, ensure_ascii=False))
    return mcontent


def mdm_create_data2(VERSION="V1.0", RIR="国家卫生标准委员会信息标准专业委员会", EVN_REL="卫生信息、电子病历",
                     MODE_CLS="分类法", AUTHORITY="卫生部统计信息中心", STATUS_REG="标准状态",
                     ORG_SUB="中国人民解放军第四军大学卫生信息研究院"):
    mf = open(r"data.json", encoding="utf8")
    mcontent = json.load(mf)
    mf.close()

    # 获取传入的参数
    kwargs = locals()
    logger.info(f"入参:{kwargs}\r\n")
    mcontent["MEMBER"]["DE_ID"] = mcontent["MEMBER"]["DATA_ELEMENT_code"]
    mcontent["MEMBER"]["TYPE"] = mcontent["MEMBER"]["DATA_ELEMENT_VALUE_DATATYPE_code"]
    mcontent["MEMBER"]["FORMAT"] = mcontent["MEMBER"]["PRESENTATION_FORMAT"]
    mcontent["MEMBER"]["VALUE"] = mcontent["MEMBER"]["VALUE_RANGE"]
    mcontent["MEMBER"]["VERSION"] = VERSION
    mcontent["MEMBER"]["RIR"] = RIR
    mcontent["MEMBER"]["EVN_REL"] = EVN_REL
    mcontent["MEMBER"]["MODE_CLS"] = MODE_CLS
    mcontent["MEMBER"]["AUTHORITY"] = AUTHORITY
    mcontent["MEMBER"]["STATUS_REG"] = STATUS_REG
    mcontent["MEMBER"]["ORG_SUB"] = ORG_SUB
    mcontent["MEMBER"]["EVN_REL"] = EVN_REL
    mcontent["MEMBER"]["PY"] = get_py(mcontent["MEMBER"]["NAME"])
    mcontent["MEMBER"]["CREATOR_NAME"] = "zhiming"
    mcontent["CREATOR_NAME"] = "zhiming"
    mcontent["CREATOR_ID"] = "10000"
    mcontent["PY"] = get_py(mcontent["MEMBER"]["NAME"])

    with open(r"data_result.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(mcontent, indent=2, ensure_ascii=False))
    return mcontent


def mdm_deal_data():
    """
    置删除标识为1
    :return:
    """
    mes = ElasticSearchImporter()
    mindex_name = "mdms.entity.masterdatamanage.master_definition"
    res = mes.search_by_body(index_name=mindex_name, MASTER_DIR_NAME="数据元值域")["hits"]["hits"]
    data = dict()
    for val in res:
        if not int(val['_source']['DELETE_FLAG']):
            print(f"正在修改第{res.index(val) + 1}条数据,内容为:{val['_source']['DELETE_FLAG']},修改为:1")
            val['_source']['DELETE_FLAG'] = "1"
            data[val["_id"]] = val['_source']
    mes.update_data_list(index_name=mindex_name, doc_type="MASTER_DEFINITION", id_data_dict=data)
    print("es数据库已修改完毕!请查看数据库效果!")


def mdm_deal_element():
    # 将数据子集中的成员补充到数据元成员中
    mindex_name = "mdms.entity.masterdatamanage.master_member"
    mes = ElasticSearchImporter()
    res = mes.search_by_body(index_name=mindex_name, MASTER_DEF_NAME="患者基本信息子集")["hits"]["hits"]
    print(f"共找到{len(res)}条记录,内容为:\n{res}")
    import copy
    res_bak = copy.deepcopy(res)
    for val in res:
        if int(val['_source']["DELETE_FLAG"]):
            res_bak.remove(val)
    print(f"处理后数据还剩{len(res_bak)},已经剔除删除标识为1的数据")


def mdm_deal_to():
    mf = open(r"data_from.json", encoding="utf8")
    mcontent_from = json.load(mf)
    mf = open(r"data_to.json", encoding="utf8")
    mcontent_to = json.load(mf)
    mf.close()
    muuid = get_uuid()
    mcontent_to["MASTER_MEMBER_ID"] = str(muuid)
    mcontent_to["PY"] = get_py(mcontent_from["MEMBER"]["NAME"])
    mcontent_to["MEMBER"]["NAME"] = mcontent_from["MEMBER"]["NAME"]
    mcontent_to["MEMBER"]["DEFINITION"] = mcontent_from["MEMBER"]["DEFINITION"]
    mcontent_to["MEMBER"]["CODE"] = mcontent_from["MEMBER"]["CODE"]
    mcontent_to["MEMBER"]["FORMAT"] = mcontent_from["MEMBER"]["FORMAT"]
    mcontent_to["MEMBER"]["PY"] = get_py(mcontent_from["MEMBER"]["NAME"])
    mcontent_to["MEMBER"]["NAME"] = mcontent_from["MEMBER"]["NAME"]
    mcontent_to["MEMBER"]["RIR"] = mcontent_from["MEMBER"]["RIR"]
    mcontent_to["MEMBER"]["MASTER_MEMBER_ID"] = muuid
    mcontent_to["MEMBER"]["CREATOR_NAME"] = "zhiming"
    mcontent_to["MEMBER"]["DE_ID"] = mcontent_from["MEMBER"]["DE_ID"]
    mcontent_to["MEMBER"]["TYPE"] = mcontent_from["MEMBER"]["TYPE"]

    with open(r"data_result.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(mcontent_to, indent=2, ensure_ascii=False))

    with open(r"data_result.json", encoding="utf8") as f:
        mdata = f.read()
    d = mdata.replace('"MEMBER": {', '"MEMBER": """{').replace('},', '}""",')
    print("重新格式化数据...")
    with open(r"data_result.json", 'w', encoding="utf8") as f:
        f.write(d)
    print("数据生成完毕,请查看data_result.json文件!")


def mdm_deal_data_biatch():
    mindex_name = "mdms.entity.masterdatamanage.master_member"
    mes = ElasticSearchImporter()
    res = mes.search_by_body(index_name=mindex_name, MASTER_DEF_NAME="患者基本信息子集")["hits"]["hits"]
    print(f"共找到{len(res)}条记录,内容为:\n{res}")
    import copy
    res_bak = copy.deepcopy(res)
    for val in res:
        if int(val['_source']["DELETE_FLAG"]):
            res_bak.remove(val)
    print(f"处理后数据还剩{len(res_bak)},已经剔除删除标识为1的数据")
    # 数据元中数据
    res_ele = mes.search_by_body(index_name=mindex_name, MASTER_DEF_NAME="卫生信息数据元WS363")["hits"]["hits"]
    print(f"共找到{len(res)}条记录,内容为:\n{res_ele}")
    import copy
    res_ele_bak = copy.deepcopy(res_ele)
    for val in res_ele:
        if int(val['_source']["DELETE_FLAG"]):
            res_ele_bak.remove(val)
    print(f"处理后数据还剩{len(res_ele_bak)},已经剔除删除标识为1的数据")
    # print(type(res_ele_bak[0]["_source"]["MEMBER"]))
    print("正在重新格式化数据...")
    for i in range(len(res_ele_bak)):
        res_ele_bak[i]["_source"]["MEMBER"] = json.loads(res_ele_bak[i]["_source"]["MEMBER"])
    datalist = dict()
    for i in range(len(res_ele_bak) - 1, len(res_ele_bak)):
        mf = open(r"data_to.json", encoding="utf8")
        mcontent_to = json.load(mf)
        for j in range(len(res_bak)):
            if res_ele_bak[i]["_source"]["MEMBER"]["CODE"] == "": pass


if __name__ == "__main__":
    logger = Logger.Logger("info", use_console=True)
    # deal_data_element()
    # res = create_data("D1EA2D69C5654A89A5074B4AF5091BC7", "身份证件类别代码", "患者身份证所属类别在特定编码体系中的代码",
    #             "HDSD00.02.26", "DE02.01.030.00", v_data="S3", v="WS364-2011表1CV02.01.101身份证件类别代码",
    #             sort="2", format="N2")
    # res = deal_data_mdm(data_element_code="DE06.00.218.00")
    # res = mdm_create_data(CODE="HDSD00.02.027", DE_ID="DE02.01.039.00", NAME="医疗保险类别代码",
    #                       DEFINITION="患者本人在公安户籍管理部门正式登记注册的姓氏和名称", TYPE="S1", FORMAT="A..50", VALUE="-")
    # res = mdm_create_data2()
    # logger.info(res)
    # mdm_deal_data()
    # mdm_deal_element()
    # mdm_deal_data_biatch()
    # mdm_deal_to()
    res = mdm_create_data(CODE="HDSD00.02.040", DE_ID="DE01.00.010.00", NAME="门(急)诊号",
                          DEFINITION="按照某一特定编码规则赋予门(急)诊就诊对象的顺序号", TYPE="S1", FORMAT="A..18", VALUE="-")
