# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-12-03 9:42
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
import json
import sqlite3
import time

from ElasticSearchImporter import ElasticSearchImporter
from utils import get_uuid, get_py


class ElasticSearchTool(object):
    def __init__(self, ip_es, port_es):
        self.__es = ElasticSearchImporter(host=ip_es, port=port_es)

    def e_sqlite2es(self):
        """
        根据mdm数据库的表记录数进行写数据到es数据库
        :return:
        """
        index_name = "mdms.entity.masterdatamanage.master_member"
        # sqlite数据库
        db_path = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
        conn = sqlite3.connect(db_path, timeout=2000)
        #         sql = """select d.id, d.code, d.de_id, d.name, d.definition, d.format, d.type, d.value, c."version ", c.rir,
        #        c.evn_rel, c.authority, c.mode_cls, c.org_sub, c.status_reg, d.create_time, d.create_id,  d.sort
        # from mdm_master a
        # left join mdm_master b on a.parent_id = b.id and a.parent_id<>0 and b.parent_id = 0
        # left join mdm_common c on b.common_id = c.id
        # left join mdm_master_item d on a.id = d.parent_id
        # where a.parent_id <> 0
        # order by a.code asc, d.code asc, d.sort asc;
        # """
        sql = """
                select distinct  d.code, d.de_id, d.name, d.definition, d.format, d.type, d.value, c."version ", c.rir,
               c.evn_rel, c.authority, c.mode_cls, c.org_sub, c.status_reg, d.create_id
        from mdm_master a
        left join mdm_master b on a.parent_id = b.id and a.parent_id<>0 and b.parent_id = 0
        left join mdm_common c on b.common_id = c.id
        left join mdm_master_item d on a.id = d.parent_id
        where a.parent_id <> 0
        order by a.code asc, d.code asc, d.sort asc;
                """
        cur = conn.cursor()
        cur.execute(sql)

        res_cur = cur.fetchall()
        res = self.__es.search_by_body(index_name=index_name, MASTER_DEF_NAME='卫生信息数据元WS363')['hits']['hits']
        count = 0
        for r in res:
            # print(f'删除第{res.index(r)}条记录...{r["_id"]}')
            self.__es.delete_data_by_id(index_name=index_name, doc_type="MASTER_MEMBER", id=r["_id"])
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
            data['MASTER_MEMBER_ID'] = get_uuid()
            data['PY'] = get_py(r[2])
            data['CREATE_TIME'] = f'{time.strftime("%Y-%m-%d", time.localtime())}' \
                                  f'T{time.strftime("%H:%M:%S", time.localtime())}Z'
            data['MEMBER']['MASTER_MEMBER_ID'] = data['MASTER_MEMBER_ID']
            data['MEMBER']['SORT'] = count
            data['MEMBER']['CREATOR_ID'] = 'zhiming'
            data['MEMBER']['NAME'] = r[2]
            data['MEMBER']['CODE'] = r[0]
            data['MEMBER']['ORG_SUB'] = r[12]
            data['MEMBER']['DEFINITION'] = r[3]
            data['MEMBER']['EVN_REL'] = r[9]
            data['MEMBER']['AUTHORITY'] = r[10]
            data['MEMBER']['VALUE'] = r[6]
            data['MEMBER']['TYPE'] = r[5]
            data['MEMBER']['FORMAT'] = r[4]
            data['MEMBER']['PY'] = get_py(r[2])
            data['MEMBER']['CREATE_TIME'] = f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}'
            data['SORT'] = count
            data['CREATOR_NAME'] = 'zhiming'
            data['MEMBER'] = json.dumps(data['MEMBER'], ensure_ascii=False)
            tmp = dict()
            tmp[data['MASTER_MEMBER_ID']] = data
            # conn.commit()
            self.__es.insert_data_list(index_name=index_name, doc_type="MASTER_MEMBER", data_dict=tmp)
            count += 1
            # print(f'写入数据:{r[3]}成功!')
            del tmp
        cur.close()
        conn.close()
        return {"error": 0, "msg": f"写入数据成功,共写入数据:{count}条,共删除记录数:{len(res)}条"}

    def e_flag_change(self, index, **kwargs):
        res = self.__es.search_by_body(index_name=index, **kwargs)['hits']
        if res['total'] == 0:
            return {"error": 1, "msg": f"没有需要修正的数据!(说明:index={index},参数:{kwargs})"}
        count = 0
        for r in res['hits']:
            if r['_source']['DELETE_FLAG'] == '1':
                r["_source"]["DELETE_FLAG"] = '0'
                # print({r['_id']: r['_source']})
                self.__es.update_data_list(index_name=index, doc_type="MASTER_DEFINITION",
                                           id_data_dict={r['_id']: r['_source']})
                count += 1

        return {"error": 0, "msg": f"修正成功!找到{res['total']}条数据,共修正{count}条数据,(说明:index={index},参数:{kwargs})"}

    def sqlite2es_e(self, index=None, doc_type=None, MASTER_DEF_ID="C79636DC4BDD488DA9CAA42712917CBB",
                    MASTER_DEF_CODE="WS363-2014", MASTER_DEF_NAME="卫生信息数据元WS363", flag_deleted=False):
        """
        根据数据库数据元数据自动同步数据到es数据库脚本
        :param index:
        :param doc_type:
        :param MASTER_DEF_ID:
        :param MASTER_DEF_CODE:
        :param MASTER_DEF_NAME:
        :param flag_deleted:
        :return:
        """
        path_db = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
        conn = sqlite3.connect(path_db, timeout=2000)
        cur = conn.cursor()
        sql_select = """
        select a.id, a.de_id, a.name, a.definition, a.type, a.format, a.value,
        b."version ", b.rir, b.evn_rel, b.mode_cls, b.authority, b.status_reg,
        b.org_sub
        from mdm_e a
        left join mdm_common b on a.common_id =b.id
        order by chapter asc, de_id asc;
        """

        cur.execute(sql_select)
        res = cur.fetchall()

        if flag_deleted:
            res_es = self.__es.search_by_body(index_name=index, MASTER_DEF_NAME=MASTER_DEF_NAME)['hits']['hits']
            for r in res_es:
                print(f"正在删除...{r['_id']}")
                self.__es.delete_data_by_id(index_name=index, doc_type=doc_type, id=r['_id'])

        es_data = {
            "MASTER_MEMBER_ID": None,
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "PY": None,
            "MEMBER": {"ORG_SUB": None, "STATUS_REG": None, "NAME": None, "STATUS": "2",
                       "PY": None, "DEFINITION": None, "DELETE_FLAG": "0",
                       "MASTER_DEF_ID": MASTER_DEF_ID, "CODE": None,
                       "EVN_REL": None, "CREATE_TIME": None, "VERSION": None,
                       "IS_ENABLE": "1", "RIR": None, "MASTER_MEMBER_ID": None, "FORMAT": None, "TYPE": None,
                       "CREATOR_ID": "10000", "SORT": None, "MODE_CLS": None, "VALUE": None, "AUTHORITY": None},
            "SORT": None,
            "STATUS": "1",
            "IS_ENABLE": "1",
            "CREATE_TIME": "2019-11-18T14:43:17.6533134+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "DELETE_FLAG": "0"
        }
        print("正在写入数据,请稍等...(请勿中断程序)")
        for content in res:
            if res.index(content) > 0:
                es_data["MEMBER"] = json.loads(es_data["MEMBER"])
            # 准备数据
            es_data["MASTER_MEMBER_ID"] = content[0]
            es_data["PY"] = get_py(content[2])
            es_data["MEMBER"]["ORG_SUB"] = content[13]
            es_data["MEMBER"]["STATUS_REG"] = content[12]
            es_data["MEMBER"]["NAME"] = content[2]
            es_data["MEMBER"]["PY"] = get_py(content[2])
            es_data["MEMBER"]["DEFINITION"] = content[3]
            es_data["MEMBER"]["EVN_REL"] = content[9]
            es_data["MEMBER"]["CODE"] = content[1]
            es_data["MEMBER"]["CREATE_TIME"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            es_data["MEMBER"]["VERSION"] = content[7]
            es_data["MEMBER"]["RIR"] = content[8]
            es_data["MEMBER"]["MASTER_MEMBER_ID"] = content[0]
            es_data["MEMBER"]["FORMAT"] = content[5]
            es_data["MEMBER"]["TYPE"] = content[4]
            es_data["MEMBER"]["MODE_CLS"] = content[10]
            es_data["MEMBER"]["SORT"] = res.index(content)
            es_data["MEMBER"]["VALUE"] = content[6]
            es_data["MEMBER"]["AUTHORITY"] = content[11]
            es_data["SORT"] = res.index(content)
            es_data[
                "CREATE_TIME"] = f'{time.strftime("%Y-%m-%d", time.localtime())}T{time.strftime("%H:%M:%S", time.localtime())}+08:00'

            es_data["MEMBER"] = json.dumps(es_data["MEMBER"], ensure_ascii=False)
            # 写入数据到es
            self.__es.insert_data_list(index_name=index, doc_type=doc_type,
                                       data_dict={es_data["MASTER_MEMBER_ID"]: es_data})
        print("数据写入完成!")
        cur.close()
        conn.close()
        return {"error": 0, "msg": f"处理成功!(备注:{len(res_es)}条数据删除,{len(res)}条数据增加)"}

    def __take_element(self, e):
        return int(json.loads(e['_source']['MEMBER'])['SORT'])

    def mdm_to_sqlite(self):
        # 从es数据库批量导入表数据到sqlite数据库
        # 1.先从定义表找到表数据
        db_path, es_define, es_menber = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db", \
                                        r'mdms.entity.masterdatamanage.master_definition', \
                                        r"mdms.entity.masterdatamanage.master_member"
        res = self.__es.search_by_body(index_name=es_define, MASTER_DIR_NAME="数据元值域")['hits']['hits']
        count = 0
        conn = sqlite3.connect(db_path, timeout=2000)
        cur = conn.cursor()
        for content in res:
            if content['_source']['DELETE_FLAG'] == '1':
                print(f"数据元值域:{content['_source']['MASTER_DEF_NAME']},置上删除标识,故在此不写入数据库!")
                continue
            print(f"数据元值域:{content['_source']['MASTER_DEF_NAME']}正在写入数据库......")
            table_name = content['_source']['MASTER_DEF_CODE']
            sql_create = f"""
             CREATE TABLE IF NOT EXISTS '""" + table_name + """' (
          code  TEXT NOT NULL PRIMARY KEY,
          name  TEXT NOT NULL,
          desc  TEXT NOT NULL,
          create_time TEXT not null)
            """
            # print(sql_create)
            # 循环写入数据
            res_men = \
                self.__es.search_by_body(index_name=es_menber, MASTER_DEF_NAME=content['_source']['MASTER_DEF_NAME'])[
                    'hits']['hits']
            # 排序
            res_men.sort(key=self.__take_element, reverse=False)
            for rm in res_men:
                # 创建表
                if int(rm['_source']["DELETE_FLAG"]) == 1:
                    continue
                cur.execute(sql_create)
                data_json = json.loads(rm['_source']['MEMBER'])
                content_insert = (data_json['CODE'], data_json['NAME'], content['_source']['MASTER_DEF_NAME'] + "," +
                                  content['_source']['MASTER_DEF_DESC'],
                                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                count += 1
                print(f"写入数据:{content_insert}到表:{content['_source']['MASTER_DEF_NAME']},{table_name}")
                try:
                    cur.execute("insert into '" + table_name + "' values(?, ?, ?, ?)", content_insert)
                except (sqlite3.IntegrityError,) as e:
                    print(f"重复主键:code({data_json['CODE']}),调过插入,继续进行插入....")
                    continue
                # break
            # 写入参照表
            sql_insert_reference = (table_name, content['_source']['MASTER_DEF_NAME'],
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            cur.execute("insert into mdm_reference(name, msg, time) values (?, ?, ?)", sql_insert_reference)
            # break
        conn.commit()
        cur.close()
        conn.close()
        # 2.根据第一步得到的表名，在成员表找到数据，在sql建表，写入数据
        return {"error": 0, "msg": f"处理成功!(备注:共完成数据{count}条数据入库)"}

    def mdm_define(self, index="mdms.entity.masterdatamanage.master_definition"):
        res = self.__es.search_by_body(index_name=index, MASTER_DIR_NAME="数据元值域")['hits']['hits']
        res.sort(key=lambda e: e["_source"]['MASTER_DEF_CODE'], reverse=False)
        for r in res:
            print(r["_source"]['MASTER_DEF_CODE'], r["_source"]['MASTER_DEF_NAME'])
        return {"error": 0, "msg": f"处理成功!(备注:共{len(res)}个表)"}

    def sqlite2es_menber(self, index=None, doc_type=None, MASTER_DEF_ID="C79636DC4BDD488DA9CAA42712917CBB",
                         MASTER_DEF_CODE="WS363-2014", MASTER_DEF_NAME="卫生信息数据元WS363", flag_deleted=False):
        """
        根据数据库指定数据元数据自动同步数据到es数据库脚本
        :param index:
        :param doc_type:
        :param MASTER_DEF_ID:
        :param MASTER_DEF_CODE:
        :param MASTER_DEF_NAME:
        :param flag_deleted:
        :return:
        """
        path_db = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
        conn = sqlite3.connect(path_db, timeout=2000)
        cur = conn.cursor()
        sql_select = """
           select id, code, name
            from "CV04.30.002";
           """

        cur.execute(sql_select)
        res = cur.fetchall()

        if flag_deleted:
            res_es = self.__es.search_by_body(index_name=index, MASTER_DEF_NAME=MASTER_DEF_NAME)['hits']['hits']
            for r in res_es:
                print(f"正在删除...{r['_id']}")
                self.__es.delete_data_by_id(index_name=index, doc_type=doc_type, id=r['_id'])

        es_data = {
            "MASTER_MEMBER_ID": None,
            "MASTER_DEF_ID": MASTER_DEF_ID,
            "MASTER_DEF_CODE": MASTER_DEF_CODE,
            "MASTER_DEF_NAME": MASTER_DEF_NAME,
            "PY": None,
            "MEMBER": {"ORG_SUB": None, "STATUS_REG": None, "NAME": None, "STATUS": "2",
                       "PY": None, "DEFINITION": None, "DELETE_FLAG": "0",
                       "MASTER_DEF_ID": MASTER_DEF_ID, "CODE": None,
                       "EVN_REL": None, "CREATE_TIME": None, "VERSION": None,
                       "IS_ENABLE": "1", "RIR": None, "MASTER_MEMBER_ID": None, "FORMAT": None, "TYPE": None,
                       "CREATOR_ID": "10000", "SORT": None, "MODE_CLS": None, "VALUE": None, "AUTHORITY": None},
            "SORT": None,
            "STATUS": "1",
            "IS_ENABLE": "1",
            "CREATE_TIME": "2019-11-18T14:43:17.6533134+08:00",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "DELETE_FLAG": "0"
        }
        print("正在写入数据,请稍等...(请勿中断程序)")
        for content in res:
            if res.index(content) > 0:
                es_data["MEMBER"] = json.loads(es_data["MEMBER"])
            # 准备数据
            es_data["MASTER_MEMBER_ID"] = content[0]
            es_data["PY"] = get_py(content[2])
            es_data["MEMBER"]["NAME"] = content[2]
            es_data["MEMBER"]["PY"] = get_py(content[2])
            es_data["MEMBER"]["CODE"] = content[1]
            es_data["MEMBER"]["CREATE_TIME"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            es_data["MEMBER"]["MASTER_MEMBER_ID"] = content[0]
            es_data["MEMBER"]["SORT"] = res.index(content)
            es_data["SORT"] = res.index(content)
            es_data[
                "CREATE_TIME"] = f'{time.strftime("%Y-%m-%d", time.localtime())}T{time.strftime("%H:%M:%S", time.localtime())}+08:00'

            es_data["MEMBER"] = json.dumps(es_data["MEMBER"], ensure_ascii=False)
            # 写入数据到es
            self.__es.insert_data_list(index_name=index, doc_type=doc_type,
                                       data_dict={es_data["MASTER_MEMBER_ID"]: es_data})
        print("数据写入完成!")
        cur.close()
        conn.close()
        return {"error": 0, "msg": f"处理成功!(备注:{len(res_es)}条数据删除,{len(res)}条数据增加)"}

    def sqlite2es_range(self, path_db=r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"):
        """
        本方法根据sqlites数据库定制化一键同步数据到es数据库
        :param path_db:
        :return:
        """
        conn = sqlite3.connect(path_db, timeout=2000)
        count_deleted = 0
        count = 0
        count_add = 0
        count_create = 0
        count_pro = 0
        count_add = 0
        cur = conn.cursor()
        sql_select_table = """
        select name, desc, msg
        from mdm_reference
        where desc is not null
        order by name asc;
        """

        # 1.得到需要写入到es的数据表名称
        names_table = cur.execute(sql_select_table).fetchall()

        print(f"程序正在批量处理,请勿强制退出......")
        # 1.1 将es值域目录下的表不在上述表中,进行置删除标识
        ranges = self.__es.search_by_body(index_name="mdms.entity.masterdatamanage.master_definition",
                                          MASTER_DIR_ID="CF0239987DA44B138127CA4AEDAE3E46")["hits"]["hits"]
        for range in ranges:
            if range['_source']['DELETE_FLAG'] == "1":
                # print(f'{range["_source"]["MASTER_DEF_NAME"]}已经是删除标识...跳过')
                continue
            flag_exist = False
            for name in names_table:
                if name[2].strip() == range['_source']['MASTER_DEF_NAME'].strip() \
                        and range['_source']['MASTER_DEF_CODE'].strip() == name[0].strip():
                    flag_exist = True
                    break
            # print(range['_source']['MASTER_DEF_NAME'].strip(), flag_exist)
            # 数据置删除标记
            if not flag_exist:
                range['_source']['DELETE_FLAG'] = "1"
                # print({range['_id']: range['_source']})
                self.__es.update_data_list(index_name="mdms.entity.masterdatamanage.master_definition",
                                           doc_type="MASTER_DEFINITION", id_data_dict={range['_id']: range['_source']})
                count_deleted += 1
            break
        for name_table in names_table:
            flag_desc = False
            flag_exist = False
            # 2.若表不在es则进行写数据到es定义表
            for range in ranges:
                if name_table[2].strip() == range['_source']['MASTER_DEF_NAME'].strip() \
                        and range['_source']['MASTER_DEF_CODE'].strip() == name_table[0].strip():
                    flag_exist = True
                    id_es = range['_id']
                    # print(range['_source'])
                    # MASTER_DEF_CODE = range["_source"]['MASTER_DEF_CODE']
                    # MASTER_DEF_ID = range["_source"]['MASTER_DEF_ID']
                    # MASTER_DEF_NAME = range["_source"]['MASTER_DEF_NAME']
                    break
            # 找到es记录后,进行删除成员表数据
            # print(name_table)
            if flag_exist:
                # 存在则删除表表,删除属性,删除记录
                # 1.删除表

                self.__es.delete_data_by_id(index_name="mdms.entity.masterdatamanage.master_definition",
                                            doc_type="MASTER_DEFINITION", id=id_es)
                # 2.删除属性
                res_pro = self.__es.search_by_body(index_name="mdms.entity.masterdatamanage.master_property",
                                                   MASTER_DEF_ID=id_es)["hits"]["hits"]
                for r in res_pro:
                    self.__es.delete_data_by_id(index_name="mdms.entity.masterdatamanage.master_property",
                                                doc_type="MASTER_PROPERTY", id=r['_id'])
                # 3.删除成员表数据
                res_menb = self.__es.search_by_body(index_name="mdms.entity.masterdatamanage.master_member",
                                                    MASTER_DEF_ID=id_es)["hits"]["hits"]
                for r in res_menb:
                    count += 1
                    self.__es.delete_data_by_id(index_name="mdms.entity.masterdatamanage.master_member",
                                                doc_type="MASTER_MEMBER", id=r['_id'])
                    # print(r)

            # 建表,建立属性
            MASTER_DEF_ID = get_uuid()
            MASTER_DEF_CODE = name_table[0]
            MASTER_DEF_NAME = name_table[2]
            es_def = {
                "IS_ENABLE": "1",
                "MASTER_DEF_DESC": name_table[1],
                "PY": get_py(MASTER_DEF_NAME),
                "IS_PUBLISH_DEF": "1",
                "MASTER_DEF_CODE": MASTER_DEF_CODE,
                "STANDARD_ID": "",
                "MASTER_DEF_ID": MASTER_DEF_ID,
                "CREATOR_ID": "1",
                "MASTER_DIR_ID": "CF0239987DA44B138127CA4AEDAE3E46",
                "DELETE_FLAG": "0",
                "STANDARD_NAME": "",
                "MASTER_DEF_NAME": MASTER_DEF_NAME,
                "SORT": names_table.index(name_table),
                "CREATOR_NAME": "zhiming",
                "MASTER_PRO_VERSION_NO": "10000",
                "CREATE_TIME": f'{time.strftime("%Y-%m-%d", time.localtime())}T{time.strftime("%H:%M:%S", time.localtime())}+08:00',
                "IS_PUBLISH_MEMBER": "0",
                "DATA_TYPE": "DATASTANDARD",
                "MASTER_DIR_NAME": "数据元值域",
                "MASTER_MEMBER_VERSION_NO": "0"
            }
            self.__es.insert_data_list(index_name="mdms.entity.masterdatamanage.master_definition",
                                       doc_type="MASTER_DEFINITION", data_dict={MASTER_DEF_ID: es_def})

            es_code = {
                "MASTER_DEF_ID": MASTER_DEF_ID,
                "MASTER_DEF_CODE": MASTER_DEF_CODE,
                "MASTER_DEF_NAME": MASTER_DEF_NAME,
                "MASTER_PRO_ID": get_uuid(),
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
            self.__es.insert_data_list(index_name="mdms.entity.masterdatamanage.master_property",
                                       doc_type="MASTER_PROPERTY", data_dict={es_code['MASTER_PRO_ID']: es_code})

            es_name = {
                "MASTER_DEF_ID": MASTER_DEF_ID,
                "MASTER_DEF_CODE": MASTER_DEF_CODE,
                "MASTER_DEF_NAME": MASTER_DEF_NAME,
                "MASTER_PRO_ID": get_uuid(),
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
            self.__es.insert_data_list(index_name="mdms.entity.masterdatamanage.master_property",
                                       doc_type="MASTER_PROPERTY", data_dict={es_name['MASTER_PRO_ID']: es_name})

            # print(f"{es_def}\n{es_code}\n{es_name}\n")
            # print(MASTER_DEF_CODE)
            count_create += 1

            # 3.根据表名查询记录
            sql_select_data = f"""
            select code, name, desc
            from "{name_table[0]}"
            order by code asc;
            """
            data = cur.execute(sql_select_data).fetchall()

            es_data = {"MASTER_MEMBER_ID": None,
                       "MASTER_DEF_ID": MASTER_DEF_ID,
                       "MASTER_DEF_CODE": MASTER_DEF_CODE,
                       "MASTER_DEF_NAME": MASTER_DEF_NAME,
                       "PY": "JSZ",
                       "MEMBER": {"DELETE_FLAG": "0", "SORT": None,
                                  "MASTER_MEMBER_ID": None, "PY": None, "STATUS": "2",
                                  "IS_ENABLE": "1", "CODE": None, "DESC": None, "CREATE_TIME": None, "NAME": None,
                                  "CREATOR_NAME": "zhiming", "MASTER_DEF_ID": MASTER_DEF_ID,
                                  "CREATOR_ID": "10000"},
                       "SORT": None,
                       "STATUS": "2",
                       "IS_ENABLE": "1",
                       "CREATE_TIME": "2019-03-22T08:50:11.7651577Z",
                       "CREATOR_ID": "10000",
                       "CREATOR_NAME": "zhiming",
                       "DELETE_FLAG": "0"}
            for d in data:
                # 循环是的有说明字段,写入数据到成员表

                if data.index(d) > 0:
                    es_data["MEMBER"] = json.loads(es_data["MEMBER"])
                # 准备数据
                es_data["MASTER_MEMBER_ID"] = get_uuid()
                es_data["PY"] = get_py(d[1])
                es_data["MEMBER"]["NAME"] = d[1]
                es_data["MEMBER"]["PY"] = get_py(d[1])
                es_data["MEMBER"]["CODE"] = d[0]
                es_data["MEMBER"]["CREATE_TIME"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                es_data["MEMBER"]["MASTER_MEMBER_ID"] = es_data["MASTER_MEMBER_ID"]
                es_data["MEMBER"]["SORT"] = data.index(d)
                es_data["MEMBER"]["DESC"] = "" if d[2].find("(") < 0 else d[2][d[2].find("(") + 1:d[2].rfind(")")]
                es_data["SORT"] = data.index(d)
                es_data[
                    "CREATE_TIME"] = f'{time.strftime("%Y-%m-%d", time.localtime())}T{time.strftime("%H:%M:%S", time.localtime())}+08:00'

                es_data["MEMBER"] = json.dumps(es_data["MEMBER"], ensure_ascii=False)
                # 写入数据到es
                self.__es.insert_data_list(index_name="mdms.entity.masterdatamanage.master_member",
                                           doc_type="MASTER_MEMBER",
                                           data_dict={es_data["MASTER_MEMBER_ID"]: es_data})
                # print(es_data)

                if d[2].find("(") > -1:
                    # print(d[2][d[2].find("(")+1:d[2].rfind(")")], d)
                    flag_desc = True
                count_add += 1
                # break

            # 写数据到属性表
            if flag_desc:
                # 写入说明字段
                desc = {"MASTER_DEF_ID": MASTER_DEF_ID,
                        "MASTER_DEF_CODE": MASTER_DEF_CODE,
                        "MASTER_DEF_NAME": MASTER_DEF_NAME,
                        "MASTER_PRO_ID": get_uuid(),
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
                self.__es.insert_data_list(index_name="mdms.entity.masterdatamanage.master_property",
                                           doc_type="MASTER_PROPERTY", data_dict={desc["MASTER_PRO_ID"]: desc})
                count_pro += 1
                # print(desc)

            # break

        cur.close()
        conn.close()
        return {"error": 0, "msg": f"处理成功!(备注:共处理{len(names_table)}个表,"
                                   f"置删除标记{count_deleted}个表,删除记录数:{count},增加记录数:{count_add},创建表:{count_create}个,创建属性表:{count_pro}个)"}


if __name__ == "__main__":
    ip, port = "127.0.0.1", 9200
    # index = "mdms.entity.masterdatamanage.master_definition"
    # MASTER_DIR_NAME = "数据元值域"
    # with Timer.timer():
    #     es = ElasticSearchTool(ip_es=ip, port_es=port)
    #     # res = es.e_sqlite2es()
    #     res = es.e_flag_change(index=index, MASTER_DIR_NAME=MASTER_DIR_NAME)
    # print(res)
    import Timer

    with Timer.Timer.timer():
        es = ElasticSearchTool(ip_es=ip, port_es=port)
        index = "mdms.entity.masterdatamanage.master_member"
        doc = "MASTER_MEMBER"
        # res = es.sqlite2es_e(index=index, doc_type=doc, flag_deleted=True)
        # res = es.mdm_define()
        # res = es.mdm_to_sqlite()
        # print(res)
        # res = ElasticSearchTool.sqlite2es_range()
        res = es.sqlite2es_range()
        print(res)
        # s = "疫苗名称代码表,药品、设备与材料"
        # print(s.find("("), s.rfind(")"), s[s.find("(")+1:s.rfind(")")])
