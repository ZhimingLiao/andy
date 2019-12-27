# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  zhiming  2019-11-13 16:10
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
import math

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError
from elasticsearch.helpers import bulk
from elasticsearch.helpers.errors import BulkIndexError


class ErrorHunter(object):
    @staticmethod
    def capture_connection_error(func):
        def _decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ConnectionError) as e:
                return {"error": 500, "msg": f"数据库连接出错!(备注:{e})"}

        return _decorator

    @staticmethod
    def capture_notfind_error(func):
        def _decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except NotFoundError as e:
                pass

        return _decorator


class ElasticSearchImporter(object):
    batch_search_size = 50000

    def __init__(self, host="127.0.0.1", port=9200, username=None, password=None):
        if username and password:
            self.es = Elasticsearch(hosts=host, port=port, http_auth=(username, password))
        else:
            self.es = Elasticsearch(hosts=host, port=port)

    @ErrorHunter.capture_connection_error
    def index_is_exits(self, index_name):
        """
        判断是否含有对应的索引
        :param index_name: 索引名称
        :return: true 是或false 否
        """
        return self.es.indices.exists(index_name)

    @ErrorHunter.capture_connection_error
    @ErrorHunter.capture_notfind_error
    def search_size(self, index_name):
        """
        返回根据索引和文件类型参数返回数据记录数
        :param index_name: 索引名称
        :param doc_type: 文件类型,es7以后推荐全部使用_doc
        :return: 返回整数
        """
        total = self.es.search(index=index_name, body={"query": {"match_all": {}}})
        return total.get("hits").get("total") if total.get("hits").get("total") else 0

    @ErrorHunter.capture_connection_error
    @ErrorHunter.capture_notfind_error
    def search_data(self, index_name):
        """
        通过索引值查询数据,返回迭代对象
        :param index_name: 索引名称
        :return:
        """
        if not self.index_is_exits(index_name):
            raise StopIteration
        total_page = math.ceil(self.search_size(index_name) / self.batch_search_size)
        for i in range(total_page):
            batch_result_data = self.es.search(index=index_name, from_=0,
                                               size=self.batch_search_size)
            id_data_list = [(result[u"_id"], result[u"_source"])
                            for result in batch_result_data[u"hits"][u"hits"]]
            for id_data in id_data_list:
                yield id_data

    @ErrorHunter.capture_connection_error
    @ErrorHunter.capture_notfind_error
    def search_by_body(self, index_name, **kwargs):
        """
        通过自定义参数,查询数据
        :param index_name: 索引名称
        :param kwargs: 关键词
        :return: 
        """
        body = {
            "from": 0,
            "size": self.batch_search_size,
            "query": {
                "match": kwargs
            }
        }
        res = self.es.search(index_name, body)
        return res

    @ErrorHunter.capture_connection_error
    def insert_data_list(self, index_name, doc_type="_doc", data_dict=None):
        """
        根据数据集合进行批量插入数据
        :param index_name: 所有名称
        :param doc_type: 文档类型,建议使用默认_doc,为兼容es6.0版本
        :param data_list: 数据集合使用list形式,具体参考示例
        :return:
        """
        if not self.index_is_exits(index_name):
            return {"msg": '索引不存在', "error": 1}
        actions = [
            {
                "_op_type": "index",
                "_index": index_name,
                "_type": doc_type,
                "_source": d,
                "_id": id_index
            }
            for id_index, d in data_dict.items()
        ]
        try:
            res = bulk(self.es, actions)
        except(BulkIndexError,) as e:
            # print(e)
            return {"msg": '映射失败,可能是由于索引名称和对应的字段对应不上!请重新检查', "error": 2}
        return {"msg": '插入成功!', "error": 0}

    @ErrorHunter.capture_connection_error
    @ErrorHunter.capture_notfind_error
    def update_data_list(self, index_name, doc_type="_doc", id_data_dict=None):
        """
        根据传参字典[{"_id": {__source}, ],和索引名称,进行批量更新数据
        :param index_name: 索引名称
        :param id_data_dict: 字典[{"_id": {__source}, ]
        :return:
        """
        if not id_data_dict:
            return {"msg": '无数据需要更新', "error": 3}

        actions = [
            {
                # "_op_type": "update",
                "_index": index_name,
                "_type": doc_type,
                "_source": d,
                "_id": id_index
            }
            for id_index, d in id_data_dict.items()
        ]

        try:
            res = bulk(self.es, actions)
        except(BulkIndexError,) as e:
            return {"msg": '映射失败,可能是由于索引名称和对应的字段对应不上!请重新检查', "error": 2}
        return {"msg": '更新成功!', "error": 0}

    @ErrorHunter.capture_connection_error
    @ErrorHunter.capture_notfind_error
    def delete_index(self, index_name):
        """
        根据索引名称进行删除索引信息;
        :param index_name: 索引名称
        :return:
        """
        if not self.index_is_exits(index_name=index_name):
            return {"msg": '索引信息不存在,不需要删除', "error": 4}
        res = self.es.indices.delete(index=index_name)
        return {"msg": f'索引:{index_name}删除成功!', "error": 0} \
            if res.get("acknowledged") else {"msg": '索引信息已经删除,不需要删除索引', "error": 7}

    @ErrorHunter.capture_connection_error
    def create_index(self, index_name):
        """
        根据索引名称进行删除该索引下的所有数据
        :param index_name: 索引名称
        :return:
        """
        if self.index_is_exits(index_name=index_name):
            return {"msg": f'索引{index_name}信息已经存在,不需要创建索引', "error": 5}
        res = self.es.indices.create(index=index_name, ignore=400)
        return {"msg": f'索引:{index_name}创建成功!', "error": 0} \
            if res.get("acknowledged") else {"msg": '索引信息已经存在,不需要创建索引', "error": 6}

    @ErrorHunter.capture_connection_error
    def delete_data_by_id(self, index_name, doc_type="_doc", id=None):
        if self.index_is_exits(index_name) and id:
            try:
                re = self.es.delete(index=index_name, doc_type=doc_type, id=id)
            except (NotFoundError,):
                return {"msg": '数据删除失败,可能根据id不存在或没有索引信息!', "error": 10}
            else:
                return {"msg": f'id:{id}删除成功!', "error": 0}
        else:
            return {"msg": '数据删除失败,可能根据id不存在或没有索引信息!', "error": 8}

    @ErrorHunter.capture_connection_error
    def delete_data_by_id_batch(self, index_name, doc_type="_doc", id_set=None):
        result_list = list()
        for id in id_set:
            result_list.append(self.delete_data_by_id(index_name, doc_type, id))
        return {"result": result_list, "error": 0}


def test_create_index():
    print(es.create_index(index_name=test_index_name))


def test_delete_index():
    print(es.delete_index(index_name=test_index_name))


def test_insert_data_list():
    print(es.insert_data_list(test_index_name, data1))


def test_update_data_list():
    data2 = {"jGhldG4BowJxLnsrYZw2": {"MASTER_DIR_NAME": "Need to deleted"}}
    print(es.update_data_list(index_name=test_index_name, doc_type="MASTER_DIRECTORY", id_data_dict=data2))


def test_insert_data_list():
    data = {1: {"MASTER_DIR_ID": "1", "MASTER_DIR_NAME": "数据元test2", "MASTER_DIR_DESC": "数据元test2",
                "DATA_TYPE": "DATASTANDARD", "SORT": "1", "DELETE_FLAG": "0"}}
    print(es.insert_data_list(test_index_name, doc_type="MASTER_DIRECTORY", data_list=data))


def test_delete_data_by_id():
    print(es.delete_data_by_id(index_name=test_index_name, doc_type="MASTER_DIRECTORY",
                               id="8c27fdeef36a4def9b4904c7f87125f9"))


if __name__ == "__main__":
    host, port = "localhost", 9200
    es = ElasticSearchImporter(host=host, port=port)
    test_index_name = "mdms.entity.masterdatamanage.test"
    test_doc_type = "DATASTANDARD"
    # d = es.search_by_body(index_name=test_index_name, DATA_TYPE="DATASTANDARD")
    data = {"B-gsZG4B9hxG1h2IUKQ9": {"MASTER_DIR_ID": "1", "MASTER_DIR_NAME": "数据元test2", "MASTER_DIR_DESC": "数据元test2",
                                     "DATA_TYPE": "DATASTANDARD", "SORT": "1", "DELETE_FLAG": "0"}}
    data1 = [{"MASTER_DIR_ID": "1", "MASTER_DIR_NAME": "数据元test2", "MASTER_DIR_DESC": "数据元test2",
              "DATA_TYPE": "DATASTANDARD", "SORT": "1", "DELETE_FLAG": "0"}]
    # print(es.insert_data_list(test_index_name, data))
    # print(es.update_data_list(test_index_name, doc_type="MASTER_DIRECTORY", id_data_dict=data))
    # print(es.create_index(index_name=test_index_name))
    # print(es.delete_data_index(index_name=test_index_name))
    # test_create_index()
    # test_delete_index()
    # test_insert_data_list()
    # test_delete_data_by_id()
    # print(es.es.indices.get_aliases().keys())
    # test_update_data_list()
    data = {"IS_ENABLE": "1",
            "MASTER_DEF_DESC": "计划与干预",
            "PY": "YCFJKZDLBDMB",
            "LAST_MODIFY_TIME": "2019-03-22T06:19:36.9105349Z",
            "IS_PUBLISH_DEF": "1",
            "MASTER_DEF_CODE": "CV06.00.219",
            "LAST_PUBLISH_TIME": "2019-03-22T06:19:36.9105349Z",
            "STANDARD_ID": "",
            "MASTER_DEF_ID": "dca31c69-0638-418b-bd74-36a80b1a860e",
            "CREATOR_ID": "1",
            "MASTER_DIR_ID": "CF0239987DA44B138127CA4AEDAE3E46",
            "LAST_MODIFIER_NAME": "",
            "DELETE_FLAG": "0",
            "STANDARD_NAME": "",
            "MASTER_DEF_NAME": "孕产妇健康指导类别代码表",
            "SORT": 203,
            "CREATOR_NAME": "超级管理员",
            "MASTER_PRO_VERSION_NO": "1",
            "CREATE_TIME": "2019-03-22T06:19:36.9105349Z",
            "IS_PUBLISH_MEMBER": "0",
            "LAST_MODIFIER_ID": "",
            "DATA_TYPE": "DATASTANDARD",
            "MASTER_DIR_NAME": "数据元值域",
            "MASTER_MEMBER_VERSION_NO": "0"}
    es.update_data_list(index_name="mdms.entity.masterdatamanage.master_definition",
                        doc_type="MASTER_DEFINITION",
                        id_data_dict={"dca31c69-0638-418b-bd74-36a80b1a860e": data})
