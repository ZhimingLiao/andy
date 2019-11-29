# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-11-14 8:24
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
import copy
import json
import os
import socket
import sqlite3
import time

# excel文件读取操作工具包
import xlrd as xd
from utils import get_py, get_uuid

from Tools.ElasticSearchTool.ElasticSearchImporter import ElasticSearchImporter as es


class ElasticSearchTool(object):
    def __init__(self, es_host, es_port):
        self.host = es_host, es_port
        if not self.test_port_use(es_host, es_port).get("error"):
            self.es = es(host=es_host, port=es_port)
        else:
            self.es = es(host="127.0.0.1", port="9200")

    @staticmethod
    def test_port_use(test_host, test_port):
        """
        根据输入ip或者域名和端口进行判断该端口是否可用
        :param test_host: 输入ip或者域名
        :param test_port: 端口
        :return:
        """
        st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        st.settimeout(2)
        try:
            st.connect((test_host, test_port))
        except WindowsError:
            error = 1
            msg = f"ip地址:{test_host},端口:{test_port}不可用"
        else:
            error = 0
            msg = "successful"
        finally:
            st.close()
            return {"error": error, "msg": msg}

    def mdm_menber_deal(self, index_name, doc_type, file_path, tmp_path, MASTER_DEF_ID, MASTER_DEF_CODE,
                        MASTER_DEF_NAME, flag):
        """
        根据文件里面的内容进行导入到对应的es成员表里
        :param index_name:
        :param doc_type:
        :param file_path:
        :param tmp_path:
        :return:
        """
        if not os.path.exists(file_path) or not os.path.exists(tmp_path):
            return {"msg": f"文件路径:{file_path}或{tmp_path}不存在!"}
        f = xd.open_workbook(file_path).sheet_by_index(0)
        tmp_data = list()
        # 获取数据库已有记录
        data_exists = self.es.search_by_body(index_name=index_name, MASTER_DEF_NAME=MASTER_DEF_NAME)["hits"]["hits"]
        with open(tmp_path, encoding="utf8") as fp:
            tmp_file = json.load(fp)
        for row in range(1, f.nrows):
            # print(f.row(row)[1].value, f.row(row)[2].value)
            muuid = get_uuid()
            tmp_file["MASTER_MEMBER_ID"] = muuid
            tmp_file["MASTER_DEF_ID"] = MASTER_DEF_ID
            tmp_file["MASTER_DEF_CODE"] = MASTER_DEF_CODE
            tmp_file["MASTER_DEF_NAME"] = MASTER_DEF_NAME
            tmp_file["PY"] = get_py(f.row(row)[2].value)
            tmp_file["MEMBER"]["NAME"] = f.row(row)[2].value
            tmp_file["MEMBER"]["PY"] = get_py(f.row(row)[2].value)
            tmp_file["MEMBER"]["DEFINITION"] = f.row(row)[3].value
            tmp_file["MEMBER"]["CODE"] = f.row(row)[0].value
            tmp_file["MEMBER"]["MASTER_MEMBER_ID"] = muuid
            tmp_file["MEMBER"]["FORMAT"] = f.row(row)[5].value
            tmp_file["MEMBER"]["TYPE"] = f.row(row)[4].value
            tmp_file["MEMBER"]["SORT"] = row + len(data_exists)
            tmp_file["MEMBER"]["MASTER_DEF_ID"] = MASTER_DEF_ID
            tmp_file["MEMBER"]["VALUE"] = f.row(row)[6].value
            tmp_file["MEMBER"]["DE_ID"] = f.row(row)[1].value
            tmp_file["SORT"] = row
            tmp_data.append(copy.deepcopy(tmp_file))
        # print(tmp_data)
        data_dict = dict()
        print(f"除去第一行标题行,共得到{len(tmp_data)}条数据!")
        if flag:
            for deleted_data in data_exists:
                print(f"正在删除第{data_exists.index(deleted_data) + 1}条记录,"
                      f"{self.es.delete_data_by_id(index_name=index_name, doc_type='MASTER_MEMBER', id=deleted_data['_id'])}")
            data_exists = list()
        flag_exists = False
        for i in range(len(tmp_data)):
            for j in range(len(data_exists)):
                if data_exists[j]["_source"]["PY"] == tmp_data[i]["PY"]:
                    flag_exists = True
                    print(f'存在此记录,不进行插入,有疑问请查看数据库,{tmp_data[i]}')
                    break
            if not flag_exists:
                tmp_data[i] = eval(json.dumps(tmp_data[i], indent=2, ensure_ascii=False)
                                   .replace(r': {', r': """{').replace(r"},", r'}""",'))
                data_dict[tmp_data[i]["MASTER_MEMBER_ID"]] = tmp_data[i]
            flag_exists = False

        print(f"已格式化好数据,现在准备写入数据库...共有{len(data_dict)}条记录插入数据库!")
        mres = self.es.insert_data_list(index_name=index_name, doc_type=doc_type, data_dict=data_dict)
        print(mres)

    def mdm_pro_deal(self, MASTER_DEF_ID, MASTER_DEF_CODE, MASTER_DEF_NAME):
        """
        :param MASTER_DEF_ID: 定义表中子集的id
        :param MASTER_DEF_CODE: 定义表中子集编码
        :param MASTER_DEF_NAME: 定义表中子集名称
        :return:
        """
        mindex_name, mdoc_type = "mdms.entity.masterdatamanage.master_property", "MASTER_PROPERTY"
        mdata = dict()
        mtype = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "TYPE",
            "MASTER_PRO_NAME": "数据元值的数据类型",
            "MASTER_PRO_DATATYPE": "Reference",
            "MASTER_PRO_LENGTH": 2,
            "MASTER_PRO_DEFAULT_VALUE": "S1",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "select",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 4,
            "CREATE_TIME": "2019-11-14T18:03:19.4490769+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mtype.get('MASTER_PRO_ID')] = mtype
        mcode = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "CODE",
            "MASTER_PRO_NAME": "内部标识符",
            "MASTER_PRO_DESC": "",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "null",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 0,
            "CREATE_TIME": "2019-11-18T06:11:35.8189538Z",
            "CREATOR_ID": "1000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mcode.get('MASTER_PRO_ID')] = mcode
        mname = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "NAME",
            "MASTER_PRO_NAME": "名称",
            "MASTER_PRO_DESC": "",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "",
            "META_DEF_REL_NAME": "",
            "SORT": 1,
            "CREATE_TIME": "2019-11-16T09:33:18.8289694Z",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mname.get('MASTER_PRO_ID')] = mname
        mde_id = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "DE_ID",
            "MASTER_PRO_NAME": "数据元标识符(DE)",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 50,
            "MASTER_PRO_DEFAULT_VALUE": "null",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 2,
            "CREATE_TIME": "2019-11-20T10:01:40.8436859+08:00",
            "CREATOR_ID": "1",
            "CREATOR_NAME": "系统管理员",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mde_id.get('MASTER_PRO_ID')] = mde_id
        mdefinition = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "DEFINITION",
            "MASTER_PRO_NAME": "定义",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "null",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 3,
            "CREATE_TIME": "2019-11-14T18:03:19.4490769+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mdefinition.get('MASTER_PRO_ID')] = mdefinition
        mformat = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "FORMAT",
            "MASTER_PRO_NAME": "表示格式",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 20,
            "MASTER_PRO_DEFAULT_VALUE": "N2",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 5,
            "CREATE_TIME": "2019-11-14T18:03:19.4490769+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mformat.get('MASTER_PRO_ID')] = mformat
        mvalue = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "VALUE",
            "MASTER_PRO_NAME": "数据元允许值",
            "MASTER_PRO_DATATYPE": "Reference",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "-",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "select",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 6,
            "CREATE_TIME": "2019-11-14T18:03:19.4490769+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mvalue.get('MASTER_PRO_ID')] = mvalue
        mversion = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "VERSION",
            "MASTER_PRO_NAME": "版本",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 5,
            "MASTER_PRO_DEFAULT_VALUE": "V1.0",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 7,
            "CREATE_TIME": "2019-11-18T16:23:52.3721557+08:00",
            "CREATOR_ID": "1",
            "CREATOR_NAME": "系统管理员",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mversion.get('MASTER_PRO_ID')] = mversion
        morg_sub = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "ORG_SUB",
            "MASTER_PRO_NAME": "提交机构",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "中国人民解放军第四军医大学卫生信息研究院",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 8,
            "CREATE_TIME": "2019-11-18T16:35:42.5836809+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[morg_sub.get('MASTER_PRO_ID')] = morg_sub
        mevn = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "EVN_REL",
            "MASTER_PRO_NAME": "相关环境",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "卫生信息、电子病历",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 9,
            "CREATE_TIME": "2019-11-18T16:35:42.5836809+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mevn.get('MASTER_PRO_ID')] = mevn
        mclss = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "MODE_CLS",
            "MASTER_PRO_NAME": "分类模式",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "分类法",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 10,
            "CREATE_TIME": "2019-11-18T16:35:42.5836809+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mclss.get('MASTER_PRO_ID')] = mclss
        mauthority = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "AUTHORITY",
            "MASTER_PRO_NAME": "主管机构",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "卫生部统计信息中心",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 11,
            "CREATE_TIME": "2019-11-18T16:35:42.5836809+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mauthority.get('MASTER_PRO_ID')] = mauthority
        mstatus = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "STATUS_REG",
            "MASTER_PRO_NAME": "注册状态",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "标准状态",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 12,
            "CREATE_TIME": "2019-11-18T16:35:42.5836809+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mstatus.get('MASTER_PRO_ID')] = mstatus
        mrir = {
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "MASTER_PRO_ID": get_uuid(),
            "MASTER_PRO_CODE": "RIR",
            "MASTER_PRO_NAME": "注册机构",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "国家卫生标准委员会信息标准专业委员会",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 8,
            "CREATE_TIME": "2019-11-18T16:35:42.5836809+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        mdata[mrir.get('MASTER_PRO_ID')] = mrir
        # 由于创建子集过程中已经分成code,name所以不需要再次生成code和name
        res = self.es.search_by_body(index_name=mindex_name, MASTER_DEF_NAME=MASTER_DEF_NAME)["hits"]["hits"]
        if res:
            print(f"属性表存在记录,共有{len(res)}条!正在删除...")
            for mv in res:
                print(f"正在删除第{res.index(mv) + 1}条记录,"
                      f"{self.es.delete_data_by_id(index_name=mindex_name, doc_type=mdoc_type, id=mv['_id'])}")
        print(f"inserting...共写入{len(mdata)}条属性记录!")
        return self.es.insert_data_list(index_name=mindex_name, doc_type=mdoc_type, data_dict=mdata)

    def mdm(self):
        mindex_name, mdoc_type = "mdms.entity.masterdatamanage.master_member", "MASTER_MEMBER"
        mfile_path, mtmp_path = r"C:\Users\andy\Desktop\mdm_import.xlsx", r"../member.json"
        # res = es.mdm_menber_deal(index_name=mindex_name, doc_type=mdoc_type, file_path=mfile_path, tmp_path=mtmp_path,
        #                          MASTER_DEF_NAME="医疗费用记录子集",  MASTER_DEF_ID="606909500B8347E9A21A3317CD78A904",
        #                          MASTER_DEF_CODE="HDSD00.02_V1.0_4")

        MASTER_DEF_ID, MASTER_DEF_CODE, MASTER_DEF_NAME = "0DACEED8D56D4E8EACF799CB2FABD7EC", "HDSD00.06_V1.0_5", "麻醉术后访视记录子集"

        # print(f'optioning...\nstep 1....')
        # res = self.mdm_pro_deal(MASTER_DEF_ID=MASTER_DEF_ID, MASTER_DEF_CODE=MASTER_DEF_CODE,
        #                         MASTER_DEF_NAME=MASTER_DEF_NAME)
        # print(res)
        print('step 2 ......')
        res = self.mdm_menber_deal(index_name=mindex_name, doc_type=mdoc_type, file_path=mfile_path, tmp_path=mtmp_path,
                                   MASTER_DEF_ID=MASTER_DEF_ID, MASTER_DEF_CODE=MASTER_DEF_CODE,
                                   MASTER_DEF_NAME=MASTER_DEF_NAME, flag=True)
        print(res)

    def mdm_e(self, e):
        return int(e[12])

    def mdm_insert(self):
        mindex = 'mdms.entity.masterdatamanage.master_member'
        res = self.es.search_by_body(index_name=mindex, MASTER_DEF_NAME="患者基本信息子集")['hits']['hits']
        content_list = list()
        count = 0
        for tmp in res:
            data_json = json.loads(tmp['_source']['MEMBER'])
            if data_json['DELETE_FLAG'] == '1':
                continue
            count += 1
            print(data_json['DEFINITION'], data_json['NAME'], data_json['DE_ID'], data_json['CODE'],
                  data_json['TYPE'], data_json['FORMAT'], data_json['VALUE'])
            content_list.append((get_uuid(), data_json['CODE'], data_json['NAME'],
                                 '1e205e4272b743fba6180e5123a1773f', data_json['DE_ID'], data_json['DEFINITION'],
                                 data_json['TYPE'],
                                 data_json['FORMAT'], data_json['VALUE'],
                                 0, 'zhiming', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count - 1))

        import sqlite3
        db_path = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
        conn = sqlite3.connect(db_path, timeout=2000)
        cur = conn.cursor()
        content_list.sort(key=self.mdm_e, reverse=False)
        for content_insert in content_list:
            cur.execute("insert into mdm_master_item values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", content_insert)
            print(content_insert)
        print(f'完成写入数据,请查看数据库效果!一共写入数据{len(content_list)}条!')
        conn.commit()
        cur.close()
        conn.close()
        return

    def mdm_update_pro(self):
        index_name = "mdms.entity.masterdatamanage.master_property"
        # sqlite数据库
        db_path = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
        conn = sqlite3.connect(db_path, timeout=2000)
        cur = conn.cursor()
        sql = """
        select a.name, c.authority, c.evn_rel, c.rir, c.org_sub
from mdm_master a
left join mdm_master b on a.parent_id = b.id and a.parent_id<>0 and b.parent_id = 0
left join mdm_common c on b.common_id = c.id
where a.parent_id <> 0;
        """
        cur.execute(sql)
        res_cur = cur.fetchall()
        # res = self.es.search_data(index_name=index_name)
        filter_name = list([i[0] for i in res_cur])
        count = 0
        # for name in filter_name:
        for name in ('麻醉术后访视记录子集', '出院记录子集', '会诊记录子集', '阶段小结子集', '转科记录子集', '交接班记录子集',
                     '疑难病历讨论子集', '上级医师查房记录子集', '日常病程记录子集', '首次病程记录子集',
                     '中医住院病案首页子集', '住院病案首页子集'):
            res = self.es.search_by_body(index_name=index_name, MASTER_DEF_NAME=name)['hits']
            con = res_cur[filter_name.index(name)]
            print(con)
            if res['total']:
                for t in res['hits']:
                    if t['_source']['MASTER_PRO_CODE'] in ('ORG_SUB', 'AUTHORITY', 'EVN_REL'):
                        print(f'找到需要修正的数据......\n{t}\n对照数据为:{name}')
                        print(f"修改前数据:{t}")
                        if t['_source']['MASTER_PRO_CODE'] == 'ORG_SUB':
                            t['_source']['MASTER_PRO_DEFAULT_VALUE'] = con[4]
                        if t['_source']['MASTER_PRO_CODE'] == 'AUTHORITY':
                            t['_source']['MASTER_PRO_DEFAULT_VALUE'] = con[1]
                        if t['_source']['MASTER_PRO_CODE'] == 'EVN_REL':
                            t['_source']['MASTER_PRO_DEFAULT_VALUE'] = con[2]
                        print(f"修改后数据:{t}")
                        a = dict()
                        a[t['_id']] = t['_source']
                        print(a)
                        self.es.update_data_list(index_name=index_name, doc_type="MASTER_PROPERTY", id_data_dict=a)
                        del a
                        count += 1
                        print(f"完成修改第{count}条数据!")
            else:
                print(f'找到可能有问题的数据,请手工修正......\n{res}\n对照数据为:{name}')
        # conn.commit()
        cur.close()
        conn.close()
        return

    def mdm_update_men(self):
        index_name = "mdms.entity.masterdatamanage.master_member"
        # sqlite数据库
        db_path = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
        conn = sqlite3.connect(db_path, timeout=2000)
        cur = conn.cursor()
        sql = """
                select a.name, c.authority, c.evn_rel, c.rir, c.org_sub
        from mdm_master a
        left join mdm_master b on a.parent_id = b.id and a.parent_id<>0 and b.parent_id = 0
        left join mdm_common c on b.common_id = c.id
        where a.parent_id <> 0;
                """
        cur.execute(sql)
        res_cur = cur.fetchall()
        # res = self.es.search_data(index_name=index_name)
        filter_name = list([i[0] for i in res_cur])
        count = 0
        # for name in filter_name:
        for name in ('出院记录子集',):
            res = self.es.search_by_body(index_name=index_name, MASTER_DEF_NAME=name)['hits']['hits']
            con = res_cur[filter_name.index(name)]
            for r in res:
                try:
                    content_json = json.loads(r['_source']['MEMBER'])
                except (json.decoder.JSONDecodeError,) as e:
                    print(e, r)
                    print(f'此处有问题的数据,请完成后手工修改....\n{name}')
                    continue
                # print(f'修改前数据为:{content_json}')
                content_json['ORG_SUB'] = con[4]
                content_json['AUTHORITY'] = con[1]
                content_json['EVN_REL'] = con[2]
                count += 1
                r['_source']['MEMBER'] = json.dumps(content_json, ensure_ascii=False)
                # print(f"修改后数据为:{r}")
                a = dict()
                a[r['_id']] = r['_source']
                self.es.update_data_list(index_name=index_name, doc_type="MASTER_MEMBER", id_data_dict=a)
                del a
                # time.sleep(0.5)
        print(f"共完成修改{count}条数据")
        return

    def mdm_insert_e(self):
        index_name = "mdms.entity.masterdatamanage.master_member"
        # sqlite数据库
        db_path = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
        conn = sqlite3.connect(db_path, timeout=2000)
        sql = """select d.id, d.code, d.de_id, d.name, d.definition, d.format, d.type, d.value, c."version ", c.rir,
       c.evn_rel, c.authority, c.mode_cls, c.org_sub, c.status_reg, d.create_time, d.create_id,  d.sort
from mdm_master a
left join mdm_master b on a.parent_id = b.id and a.parent_id<>0 and b.parent_id = 0
left join mdm_common c on b.common_id = c.id
left join mdm_master_item d on a.id = d.parent_id
where a.parent_id <> 0
order by a.code asc, d.code asc, d.sort asc;
"""
        cur = conn.cursor()
        cur.execute(sql)

        id = ""
        res_cur = cur.fetchall()
        res = self.es.search_by_body(index_name=index_name, MASTER_DEF_NAME='卫生信息数据元WS363')['hits']['hits']
        count = 0
        for r in res:
            print(f'删除...{r["_id"]}')
            self.es.delete_data_by_id(index_name=index_name, doc_type="MASTER_MEMBER", id=r["_id"])
        for r in res_cur:
            # r = res_cur[0]
            data = {
                "MASTER_MEMBER_ID": "6DC4424C03DC4713BBB99CB1798294CF",
                "MASTER_DEF_ID": "C79636DC4BDD488DA9CAA42712917CBB",
                "MASTER_DEF_CODE": "WS363-2014",
                "MASTER_DEF_NAME": "卫生信息数据元WS363",
                "PY": "HZDHHM",
                "MEMBER": {"ORG_SUB": "中国人民解放军第四军大学卫生信息研究院", "STATUS_REG": "标准状态", "NAME": "城乡居民健康档案编号", "STATUS": "2",
                           "PY": "CXJMJKDABH", "DEFINITION": "城乡居民个人健康档案的编号", "DELETE_FLAG": "0",
                           "MASTER_DEF_ID": "C79636DC4BDD488DA9CAA42712917CBB", "CODE": "HDSD00.02.003",
                           "EVN_REL": "卫生信息、电子病历", "CREATE_TIME": "2019-11-18 14:13:43", "VERSION": "V1.0",
                           "IS_ENABLE": "1", "RIR": "国家卫生标准委员会信息标准专业委员会",
                           "MASTER_MEMBER_ID": "91AB5FC5B57A49EA87E6E00B08DC0A25", "FORMAT": "N17", "TYPE": "",
                           "CREATOR_ID": "10000", "SORT": "1111", "MODE_CLS": "分类法", "VALUE": "",
                           "DE_ID": "DE01.00.009.00",
                           "AUTHORITY": "卫生部统计信息中心"},
                "SORT": 19,
                "STATUS": "1",
                "IS_ENABLE": "1",
                "CREATE_TIME": "2019-11-18T14:43:17.6533134+08:00",
                "CREATOR_ID": "1",
                "CREATOR_NAME": "系统管理员",
                "DELETE_FLAG": "0"
            }
            data['MASTER_MEMBER_ID'] = r[0]
            data['PY'] = get_py(r[3])
            data['MEMBER']['MASTER_MEMBER_ID'] = r[0]
            data['MEMBER']['SORT'] = r[len(r) - 1]
            data['MEMBER']['CREATOR_ID'] = 'zhiming'
            data['MEMBER']['NAME'] = r[3]
            data['MEMBER']['CODE'] = r[1]
            data['MEMBER']['ORG_SUB'] = r[13]
            data['MEMBER']['DEFINITION'] = r[4]
            data['MEMBER']['EVN_REL'] = r[10]
            data['MEMBER']['AUTHORITY'] = r[11]
            data['MEMBER']['VALUE'] = r[7]
            data['MEMBER']['TYPE'] = r[6]
            data['MEMBER']['FORMAT'] = r[5]
            data['MEMBER']['PY'] = get_py(r[3])

            data['SORT'] = r[len(r) - 1]
            data['CREATOR_NAME'] = 'zhiming'
            data['MEMBER'] = json.dumps(data['MEMBER'], ensure_ascii=False)
            tmp = dict()
            tmp[r[0]] = data
            # conn.commit()
            self.es.insert_data_list(index_name=index_name, doc_type="MASTER_MEMBER", data_dict=tmp)
            count += 1
            print(f'写入数据:{r[3]}成功!')
            del tmp
        print(f'写入数据成功,共写入{count}条数据!')

        cur.close()
        conn.close()


if __name__ == "__main__":
    host, port = "127.0.0.1", 9200
    es = ElasticSearchTool(host, port)
    # res = es.es.search_by_body("mdms.entity.masterdatamanage.master_member", MASTER_DEF_NAME="患者基本信息子集")["hits"]["hits"]
    # print(len(res), res)

    # es.mdm()
    # print(get_uuid())
    # es.mdm_insert()
    # es.mdm_update_pro()
    # print(es.es.search_by_body(index_name="mdms.entity.masterdatamanage.master_property", MASTER_DEF_NAME='麻醉术前访视记录子集'))
    es.mdm_update_men()
    # es.mdm_insert_e()
    # es.mdm()
