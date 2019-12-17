# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-12-03 13:58
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
import os
import sqlite3
import time

from Timer import Timer
from mdm_enum import DirEnum
from utils import get_uuid


def main():
    path_db = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
    conn = sqlite3.connect(path_db, timeout=2000)
    cur = conn.cursor()
    sql = """select distinct  d.de_id, d.name, d.definition, d.format, d.type, d.value, b.common_id
from mdm_master a
left join mdm_master b on a.parent_id = b.id and a.parent_id<>0 and b.parent_id = 0
left join mdm_common c on b.common_id = c.id
left join mdm_master_item d on a.id = d.parent_id
where a.parent_id <> 0
order by d.de_id asc, d.sort asc;"""
    res = cur.execute(sql)
    content_dict = dict()
    for content in res.fetchall():
        content_dict[content[0]] = content
    for de_id, content in content_dict.items():
        content_insert = (get_uuid(), de_id, content[1], content[2], content[4], content[3], content[5],
                          content[6], '0', "zhiming", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cur.execute("insert into mdm_e values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", content_insert)
        # print(content_insert)
    conn.commit()
    cur.close()
    conn.close()
    return {"error": 0, "msg": "处理成功!"}


def insert(de_id, name, definition, _type, _format, value, common_id, chapter):
    path_db = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
    conn = sqlite3.connect(path_db, timeout=2000)
    cur = conn.cursor()
    content_insert = (get_uuid(), de_id.strip(), name.replace(" ", ""), definition.replace(" ", ""), _type.strip(),
                      _format.strip(), value.strip(), common_id.strip(), '0', "zhiming",
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), chapter)
    try:
        cur.execute("insert into mdm_e values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", content_insert)
    except (sqlite3.IntegrityError,) as e:
        msg = f"违反了唯一约束,请检查数据!(备注:{e})"
        error = 1
    else:
        conn.commit()
        error, msg = 0, "处理成功!"
    finally:
        cur.close()
        conn.close()
        return {"error": error, "msg": msg}


def text2sqlite():
    path_txt = r"C:\Users\andy\Desktop\test.txt"
    contents = list()
    with open(path_txt, "r", encoding="utf8") as f:
        content = f.readline()
        count = 0
        while content:
            contents.append((content, f.readline()))
            count += 1
            content = f.readline()
    sql_create = """CREATE TABLE IF NOT EXISTS  'CV04.30.002'(
          id  text NOT NULL PRIMARY KEY,
          code  TEXT NOT NULL,
          name  TEXT NOT NULL,
          desc  TEXT NOT NULL,
          create_time TEXT not null)"""

    path_db = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
    conn = sqlite3.connect(path_db, timeout=2000)
    cur = conn.cursor()
    cur.execute(sql_create)
    for con in contents:
        content_isnert = (get_uuid(),
                          con[0].replace(" ", "").replace("\n", "").upper().replace("乙", "Z").replace("O", "0").replace(
                              "o", "0"), con[1].replace("\n", "").replace(" ", "").replace("x", "X"),
                          "用放射诊断检查技术编码表,临床辅助检查", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cur.execute("insert into 'CV04.30.002'(id, code, name, desc, create_time) values (?, ?, ?, ?, ?)",
                    content_isnert)

    conn.commit()
    cur.close()
    conn.close()
    return {"error": 0, "msg": f"写入成功!(备注:{len(contents)}条数据)"}


def walkFile(file: str) -> list:
    file_list = list()
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            file_list.append(os.path.join(root, f))
        # 遍历所有的文件夹
        for d in dirs:
            file_list.append(os.path.join(root, d))

    return file_list


def sqlite2mdm_e(name_file=None) -> dict:
    """
    本函数执行,进行一键生成数据元数据并保存到md文件中
    :param name_file:
    :return:
    """
    sql_select = """
    select a.id, a.de_id, a.name, a.definition, a.type, a.format, a.value,
       b."version ", b.rir, b.evn_rel, b.mode_cls, b.authority, b.status_reg,
       b.org_sub, chapter
        from mdm_e a
        left join mdm_common b on a.common_id =b.id
        order by chapter asc, de_id asc;
    """
    path_db = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
    conn = sqlite3.connect(path_db, timeout=2000)
    cur = conn.cursor()

    res = cur.execute(sql_select).fetchall()

    # 查询有数据,则写头部信息
    if res:
        file_save(
            content=f"## 卫生信息数据元目录\n\n> [!NOTE]\n>\n>\n> 以下数据摘自 **WS 363.12-2011《卫生信息数据元目录》**, 共计**{len(res)}**条数据元\n",
            name_file=name_file)
        file_save(content="##### 以下数据为数据元公有属性\n\n| 版本 |           注册机构           | 相关环境 | 分类模式 |"
                          "      主管机构       | 注册状态 |      提交机构       |\n| :--: | :--------------------------: "
                          "| :------: | :------: | :-----------------: | :------: | :-----------------: |\n"
                          "| V1.0 | 卫生部卫生信息标准专业委员会 | 卫生信息 |  分类法  | 卫生部统计信息 中心 | 标准状态 | 卫生部统计信息 中心 |",
                  name_file=name_file)
        file_save(content=f"##### 以下数据为数据元公有属性\n| 序号 | 数据元标识符 | 数据元名称 | 定义 | 数据类型 | 表示格式 "
                          f"| 数据元允许值 | 章节 |\n| :--: | :----------: | ---------- | ---- | -------- "
                          f"| -------- | :----------: | :--: |", name_file=name_file)
    for r in res:
        content = (r[1], r[2], r[3], r[4], r[5], r[6], r[14], DirEnum[chr(r[14] + 95)].value)
        path_file = "/files/" + content[7]
        file_save(
            f'|{res.index(r) + 1}|{content[0]}|{content[1]}|{content[2]}|{content[3]}|{content[4]}|{content[5]}|<a href="{path_file.replace(" ", "")}" target="_blank">{content[6]}</a>|',
            name_file=name_file)
        # break
    cur.close()
    conn.close()
    return {"error": 0, "msg": f"处理成功!(备注:共处理{len(res)}条数据)"}


def sqlite2mdm_data_set(name_file=None) -> dict:
    """
    本函数一键从数据库,生成数据标准数据子集所有内容并保存到md文件
    :param name_file:
    :return:
    """
    path_db = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
    conn = sqlite3.connect(path_db, timeout=2000)
    cur = conn.cursor()
    sql_select = """
    select d.id, d.code, d.de_id, d.name, d.definition, d.format, d.type, d.value, c."version ", c.rir,
       c.evn_rel, c.authority, c.mode_cls, c.org_sub, c.status_reg, d.create_time, d.create_id, d.sort, a.name,b.name, a.chapter
from mdm_master a
left join mdm_master b on a.parent_id = b.id and a.parent_id<>0 and b.parent_id = 0
left join mdm_common c on b.common_id = c.id
left join mdm_master_item d on a.id = d.parent_id
where a.parent_id <> 0
order by a.code asc, d.code asc, d.sort asc;
    """
    res = cur.execute(sql_select).fetchall()

    # 若有数据,则写入标题头
    if res:
        file_save(
            content=f"## 卫生信息数据元目录\n\n> [!NOTE]\n>\n>\n> 以下数据摘自 **WS 445.1-2014《电子病历基本数据集》**, 共计**{len(res)}**条数据\n",
            name_file=name_file)
        file_save(
            content=f"| 序号 | 内部标识符 | 数据元标识符 | 数据元名称 | 定义 | 数据类型 | 表示格式 | 数据元允许值 | 版本 | 注册机构 | 相关环境 | 分类模式 | 主管机构 | 注册状态 | 提交机构 | 章节 |\n| ---- | ---------- | ------------ | ---------- | ---- | -------- | -------- | ------------ | ---- | -------- | -------- | -------- | -------- | -------- | -------- | ---- |",
            name_file=name_file)
    for r in res:
        content = (res.index(r) + 1, r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10],
                   r[11], r[12], r[13], r[14], r[18],
                   f'<a href="/files/data_set/WS 445.{str(r[20])}-2014 电子病历基本数据集 第{str(r[20])}部分：{r[19].replace("基本数据集", "")}.PDF" target="_blank">{r[20]}</a>',
                   r[20])
        file_save(
            content=f"|{content[0]}|{content[1]}|{content[2]}|{content[3]}|{content[4]}|{content[5]}|{content[6]}|{content[7]}"
                    f"|{content[8]}|{content[9]}|{content[10]}|{content[12]}|{content[11]}|{content[13]}|{content[14]}|"
                    f"{content[16]}|", name_file=name_file)
        # break

    cur.close()
    conn.close()
    return {"error": 0, "msg": f"处理成功!(备注:共处理{len(res)}条数据)"}


def sqlite2mdm_range(name_file=None, path_db: str = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db") -> dict:
    """
    一键提取标准数据值域数据生成md文件
    :return:
    """
    conn = sqlite3.connect(path_db, timeout=2000)
    cur = conn.cursor()
    sql_select_table = """
    select name, msg, chapter from mdm_reference where desc is not null
        order by name asc
    """
    table_names = cur.execute(sql_select_table).fetchall()

    # 需要写数据时,先写表头
    if table_names:
        file_save(
            content=f"## 卫生信息数据元值域代码\n\n> [!NOTE]\n>\n>\n> 以下数据摘自 ****WS 364.4-2011《卫生信息数据元值域代码》**, 共计**{len(table_names)}**个表\n",
            name_file=name_file)

    for names in table_names:
        sql_select = f"select code, name from '{names[0]}' order by code asc"
        if names[2] is None:
            print(names)
        chapter = DirEnum[chr(names[2] + 95)].value
        chapter_name = chapter[chapter.find("：") + 1:-4]
        try:
            res = cur.execute(sql_select).fetchall()
        except (sqlite3.OperationalError,) as e:
            # print(f"没有该表数据{e}")
            continue
        file_save(content=f'##### {names[1]} \n\n<a href="/files/卫生信息数据元值域代码第{names[2]}部分：{chapter_name}.pdf" '
                          f'target="_blank">详情请点击此链接</a>\n\n| 序号 | 编码 | 名称 |\n| ---- | ---- | ---- |',
                  name_file=name_file)
        for r in res:
            file_save(content=f"|{res.index(r) + 1}|{r[0]}|{r[1]}|", name_file=name_file)
            # break
        file_save(content="\n", name_file=name_file)
        # break
    cur.close()
    conn.close()
    return {"error": 0, "msg": f"处理成功!(备注:共处理{len(table_names) + 1}条数据)"}


def insert_cv(name_table: str, code, name, desc, path_db=r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db") -> dict:
    """
    根据参数建表,写入数据
    :param name_table: 表名
    :param code: 编码
    :param name: 名称
    :param desc: 描述
    :param path_db: 数据库地址
    :return: 处理结果
    """
    conn = sqlite3.connect(path_db, timeout=2000)
    cur = conn.cursor()
    sql_create = f"CREATE TABLE IF NOT EXISTS  '{name_table}'(code TEXT NOT NULL PRIMARY KEY," \
                 f"name  TEXT NOT NULL, desc  TEXT NOT NULL, create_time TEXT not null)"
    cur.execute(sql_create)
    try:
        cur.execute(f"insert into '{name_table}' values (?, ?, ?, ?)", (code.replace(" ", ""), name.replace(" ", ""),
                                                                        desc.replace(" ", ""),
                                                                        time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                      time.localtime())))
    except (sqlite3.IntegrityError,) as e:
        msg = f"违反了唯一约束,请检查数据!(备注:{e})"
        error = 1
    else:
        conn.commit()
        error, msg = 0, "处理成功!"
    finally:
        cur.close()
        conn.close()
        return {"error": error, "msg": msg}


def insert_cv_batch(name_table: str, desc, flag=False) -> dict:
    # res = insert_cv(name_table=name_table, code="01", name="左枕前 (LOA)", desc=dsec)
    path_file = r"C:\Users\andy\Desktop\demo.txt"
    content_list = list()
    with open(path_file, encoding="utf8") as f:
        content = f.readline()
        while content:
            content_list.append(content.replace("\n", ""))
            if content == "":
                continue
            content = f.readline()
    for content in content_list:
        if content == "":
            continue
        if flag:
            insert_cv(name_table=name_table,
                      code='99' if content in ("其他", "不详") else ('00' + str(content_list.index(content) + 1))[-2:],
                      name=content, desc=desc)
        else:
            insert_cv(name_table=name_table,
                      code='9' if content in ("其他", "不详") else str(content_list.index(content) + 1), name=content,
                      desc=desc)
        # print(('00'+str(content_list.index(content)+1))[-2:])
    return {"error": 0, "msg": "处理成功"}


def update_e():
    path_file = r"C:\Users\andy\Desktop\demo.txt"
    path_db = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
    content_list = list()
    with open(path_file, encoding="utf8") as f:
        content = f.readline()
        while content:
            content_list.append(content.replace("\n", ""))
            if content == "":
                continue
            content = f.readline()
    conn = sqlite3.connect(path_db, timeout=2000)
    cur = conn.cursor()
    for content in content_list:
        cnd = ('00' + str(content_list.index(content) + 1))[-2:]
        print(cnd)
        cur.execute(f"update 'CV08.50.001' set desc = '({content})疫苗名称代码表,药品、设备与材料' where code='{cnd}' or 1=2")

    conn.commit()
    cur.close()
    conn.close()
    return {"error": 0, "msg": "处理成功"}


def file_save(content: str, path_dir=None, name_file=None, encoding="utf8") -> dict:
    if content is None or content == "":
        return {"error": 1, "msg": f"没有内容需要保存!"}

    if not isinstance(content, (str,)):
        return {"error": 2, "msg": f"参数错误,你需要传入一个字符串的数据!"}

    if path_dir is None or path_dir == "":
        path_dir = os.path.join(os.getcwd(), "log")
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    if name_file is None or name_file == "":
        name_file = f'{time.strftime("%Y-%m-%d", time.localtime())}.log'

    path_file = os.path.join(path_dir, name_file)

    # 写数据到path_file
    with open(path_file, encoding=encoding, mode="a") as f:
        f.write(content)
        f.write("\n")

    return {"error": 0, "msg": f"处理成功!(备注:文件保存路径为:{path_file})"}


if __name__ == "__main__":
    with Timer.timer():
        # # main()
        # res = insert(de_id="DE09.00.102.00", name="计划生育指标标志",
        #              definition="表示本次妊娠是否有生育指标",
        #              _type="L", _format="T/F",
        #              value="",
        #              common_id="15b136a0ac974c8f8b8808b8f7eb1eb2", chapter=17)
        # res = text2sqlite()
        # 1.想要从sqlite3数据库生成数据集数据,请执行下面代码
        # res = sqlite2mdm_data_set(name_file="mdm_set.md")
        # 2.想要从sqlite3数据库生成数据元值域数据, 请执行下面代码
        # res = sqlite2mdm_range(name_file="mdm_range.md")
        # 3.想要从sqlite3数据库生成数据元数据, 请执行下面代码
        # res = sqlite2mdm_e(name_file="mdm_e.md")
        # print([f"|content[{i}]" for i in range(1,17)]
        # )
        # 建表写入数据
        # res = insert_cv_batch(name_table='CV08.10.006', desc=" 血 吸虫病诊 断(治 疗)机 构级别代码表,卫生机构", flag=False)
        # res = "  将局麻药物 注射 于神经干 的周 围 ,使该 神 经 分 布 的 区域 产 生 麻 醉作 用的方法".replace(" ", "")
        # res = update_e()
        res = (get_uuid(), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(res)
