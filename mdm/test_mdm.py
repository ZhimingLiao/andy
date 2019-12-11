# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-12-02 10:50
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
import json
import time

import utils


class MDMOptionor(object):
    def __init__(self, mes):
        self.es = mes

    def _get_e_info(self, index, **kwargs):
        res = self.es.search_by_body(index_name=index, **kwargs)["hits"]
        if not res["total"]:
            return {"error": 1, "msg": "根据参数,没有得到返回数据"}
        return res["hits"][0]["_source"]

    def create_pro(self, index, doc_type="MASTER_PROPERTY", **kwargs):
        infos = self._get_e_info(index, **kwargs)
        code = {
            "MASTER_DEF_ID": kwargs.get("MASTER_DEF_ID"),
            "MASTER_DEF_CODE": infos["MASTER_DEF_CODE"],
            "MASTER_DEF_NAME": infos["MASTER_DEF_NAME"],
            "MASTER_PRO_ID": utils.get_uuid(),
            "MASTER_PRO_CODE": "CODE",
            "MASTER_PRO_NAME": "编码",
            "MASTER_PRO_DESC": "",
            "MASTER_PRO_DATATYPE": "String",
            "MASTER_PRO_LENGTH": 100,
            "MASTER_PRO_DEFAULT_VALUE": "null",
            "MASTER_PRO_MANDATORY": 1,
            "MASTER_PRO_CONTROL_TYPE": "input",
            "META_DEF_REL_ID": "-",
            "META_DEF_REL_NAME": "-",
            "SORT": 0,
            "CREATE_TIME": f"{time.strftime('%Y-%m-%d', time.localtime())}T{time.strftime('%H:%M:%S', time.localtime())}.0Z",
            "CREATOR_ID": "1000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        name = {
            "MASTER_DEF_ID": kwargs.get("MASTER_DEF_ID"),
            "MASTER_DEF_CODE": infos["MASTER_DEF_CODE"],
            "MASTER_DEF_NAME": infos["MASTER_DEF_NAME"],
            "MASTER_PRO_ID": utils.get_uuid(),
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
            "CREATE_TIME": f"{time.strftime('%Y-%m-%d', time.localtime())}T{time.strftime('%H:%M:%S', time.localtime())}.0Z",
            "CREATOR_ID": "10000",
            "CREATOR_NAME": "zhiming",
            "IS_ENABLE": "1",
            "DELETE_FLAG": "0"
        }
        index_pro = "mdms.entity.masterdatamanage.master_property"
        deleted_need_id = self.__get_id_to_deleted(index=index_pro, **kwargs)
        if deleted_need_id:
            for id in deleted_need_id:
                self.es.delete_data_by_id(index_name=index_pro, doc_type="MASTER_PROPERTY", id=id)
        data_dict = dict()
        data_dict[code.get("MASTER_PRO_ID")] = code
        data_dict[name.get("MASTER_PRO_ID")] = name
        return self.es.insert_data_list(index_name=index_pro, doc_type=doc_type, data_dict=data_dict)

    def __get_id_to_deleted(self, index, **kwargs):
        """
        :param index: 索引名称
        :param kwargs: 匹配的关键值
        :return: 匹配的数据的id集合
        """
        res = self.es.search_by_body(index_name=index, **kwargs)['hits']
        id = set()
        if res["total"] > 0:
            for d in res["hits"]:
                id.add(d["_id"])
        return id

    def create_men(self, index, doc_type="MASTER_MEMBER", data_dict=None, flag_deleted=True, **kwargs):
        """
        :param index: 索引名称
        :param doc_type: 文件类型
        :param kwargs:
        :return:
        """
        if flag_deleted:
            infos = self._get_e_info(index, **kwargs)
            id_need_deleted = self.__get_id_to_deleted(index=index, **kwargs)
            if id_need_deleted:
                for id in id_need_deleted: self.es.delete_data_by_id(index_name=index, doc_type=doc_type, id=id)
        value = {
            "MASTER_MEMBER_ID": None,
            "MASTER_DEF_ID": kwargs.get("MASTER_DEF_ID"),
            "MASTER_DEF_CODE": infos["MASTER_DEF_CODE"],
            "MASTER_DEF_NAME": infos["MASTER_DEF_NAME"],
            "PY": None,
            "MEMBER": {"CREATOR_NAME": "zhiming", "DELETE_FLAG": "0", "MASTER_MEMBER_ID": None,
                       "PY": None, "STATUS": "1", "SORT": None, "IS_ENABLE": "1", "CODE": None, "NAME": None,
                       "CREATE_TIME": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                       "MASTER_DEF_ID": "4a1571ee-1df8-443f-be9d-a57121fef3e7", "CREATOR_ID": "10000"},
            "SORT": None,
            "STATUS": "1",
            "IS_ENABLE": "1",
            "CREATE_TIME": f"{time.strftime('%Y-%m-%d', time.localtime())}T{time.strftime('%H:%M:%S', time.localtime())}.0Z",
            "CREATOR_ID": "1",
            "CREATOR_NAME": "zhiming",
            "DELETE_FLAG": "0"
        }
        if data_dict:
            for d in data_dict:
                if data_dict.index(d) > 0:
                    value["MEMBER"] = json.loads(value["MEMBER"])
                value["MASTER_MEMBER_ID"] = utils.get_uuid()
                value["PY"] = utils.get_py(d["NAME"])
                value["SORT"] = data_dict.index(d)
                value[
                    "CREATE_TIME"] = f"{time.strftime('%Y-%m-%d', time.localtime())}T{time.strftime('%H:%M:%S', time.localtime())}.0Z"
                value["MEMBER"]["MASTER_MEMBER_ID"] = value["MASTER_MEMBER_ID"]
                value["MEMBER"]["CODE"] = d.get("CODE")
                value["MEMBER"]["NAME"] = d.get("NAME")
                value["MEMBER"]["MASTER_DEF_ID"] = kwargs.get("MASTER_DEF_ID")
                value["MEMBER"]["PY"] = utils.get_py(d["NAME"])
                value["MEMBER"]["SORT"] = data_dict.index(d)
                value["MEMBER"]["CREATE_TIME"] = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"

                value["MEMBER"] = json.dumps(value["MEMBER"], ensure_ascii=False)

                self.es.insert_data_list(index_name=index, doc_type=doc_type,
                                         data_dict={value['MASTER_MEMBER_ID']: value})
            del value
        return {"error": 0, "msg": "操作成功!"}


if __name__ == "__main__":
    es = MDMOptionor(ip="127.0.0.1", port=9200)
    # res = es.get_e_info("mdms.entity.masterdatamanage.master_definition", MASTER_DEF_ID="443C1918187040F5A353FB5E11EBC722")
    res = es.create_pro("mdms.entity.masterdatamanage.master_definition",
                        MASTER_DEF_ID="443C1918187040F5A353FB5E11EBC722")
    # res = es.get_pro(index="mdms.entity.masterdatamanage.master_definition",  MASTER_DEF_ID="443C1918187040F5A353FB5E11EBC722")
    res = es.create_men("mdms.entity.masterdatamanage.master_member", data_dict=[{"CODE": "test", "NAME": "TEST"}],
                        MASTER_DEF_ID="fcdaa67c-f0ed-4be1-a95c-fe059063f3dc")
    print(res)
