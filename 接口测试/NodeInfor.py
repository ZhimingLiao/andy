# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 中山二院  志明  2019-04-17 14:09
# 当前计算机登录名称 :andy
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-04-17 14:09'

# 导入节点处理模块
from xml.etree import ElementTree as ET


class NodeInfor(object):
    Root = None

    def __init__(self, FileName, ns):
        super().__init__()
        self.FileName = FileName
        self.ns = ns
        if NodeInfor.Root is None:
            NodeInfor.Root = ET.parse(FileName)

    # 获取节点属性的节点值
    def __GetAttrValue(self, Object, Attr):
        ReturnStr = ""
        if Object is None:
            return "警告:没有节点信息!"
        # 如果Object为集合list,则进行迭代
        if isinstance(Object, list):
            if len(Object) == 0:
                return "警告:为空的集合LIST!"
            for ob in Object:
                try:
                    if ob.attrib[Attr]:
                        # ReturnStr.join(ob.attrib[Attr])
                        ReturnStr += ob.attrib[Attr]
                except(KeyError):
                    return "警告:没有此属性值!"
                except(Exception) as e:
                    raise e
            return ReturnStr
        # 如果非集合list
        else:
            try:
                ReturnStr = (Object.attrib[Attr] if Object.attrib[Attr] else "")
            except(KeyError):
                return "警告:没有此属性值!"
            except(Exception) as e:
                raise e
            return ReturnStr

    # 字符串处理,每个节点加上命名空间ns
    def __DoStr(self, Str, ns):
        Strs = Str.split("/")
        st = ""
        for s in Strs:
            st = st + ns + s + "/"
        st = st[:-1:]
        return st

    # 解析节点信息
    def GetNodeInfo(self, Str):
        # 形如:"/controlActProcess/subject/registrationRequest/subject1
        # /healthCareProvider/statusCode/@code"
        if Str.startswith('/'):
            t = Str[1::]
        else:
            t = Str
        t1, t2 = t.split("@")
        t1 = t1[:-1:]
        return self.__GetAttrValue(self.Root.find(self.__DoStr(t1, "t1:"), self.ns), t2)


if __name__ == "__main__":
    # 命名空间处理
    ns = {"t1": "urn:hl7-org:v3"}
    n = NodeInfor("test.xml", ns)
    t1 = "/controlActProcess/subject/observationRequest/author/assignedEntity/" \
         "representedOrganization/name/item/part/@value"
    print("科室:", n.GetNodeInfo(t1))