# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-04-16 14:27
# 当前计算机登录名称 :andy
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-04-16 14:27'
from xml.etree import ElementTree as ET


# 获取节点属性值
def GetAttrValue(Object, Attr):
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
                    ReturnStr += ob.attrib[Attr] + "\n"
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


# 获取节点的值
def GetValue(Object):
    return Object.text if Object.text else ""


# 字符串处理,每个节点加上命名空间ns
def DoStr(Str, ns):
    Strs = Str.split("/")
    st = ""
    for s in Strs:
        st = st + ns + s + "/"
    st = st[:-1:]
    return st


# 解析节点信息
def GetNodeInfo(Str, n, ns):
    # 形如:"/controlActProcess/subject/registrationRequest/subject1
    # /healthCareProvider/statusCode/@code"
    if Str.startswith('/'):
        t = Str[1::]
    else:
        t = Str
    t1, t2 = t.split("@")
    t1 = t1[:-1:]
    return GetAttrValue(Root.findall(DoStr(t1, n), ns), t2)


if __name__ == '__main__':
    # 命名空间处理
    ns = {"t1": "urn:hl7-org:v3"}
    # 从文档中载入需要解析节点
    Root = ET.parse('test.xml')
    t1 = "/controlActProcess/queryByParameter/queryByParameterPayload/actId/value/item/@extension"
    print(GetNodeInfo(t1, "t1:", ns))

    # Str = "MSH|^~\&|HIS||EAI||20190419171000||ADT^A01|100404304227|P|2.4|||AL|AL|CHN|GBK"
    # print(Str.split("|"), len(Str.split("|")))
