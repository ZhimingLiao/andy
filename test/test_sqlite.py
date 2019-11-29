# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-11-27 15:11
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
import os
import sqlite3
import time

import xlrd

from Tools.ElasticSearchTool.utils import get_uuid


def mdm_master():
    db_path = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
    conn = sqlite3.connect(db_path, timeout=2000)
    cur = conn.cursor()
    sql = "select id, name from mdm_master;"
    result_list = cur.execute(sql).fetchall()
    file_path = r'C:\Users\andy\Desktop\test.xlsx'
    file = xlrd.open_workbook(file_path).sheet_by_index(0)
    for index in range(0, file.nrows):
        # print(file.row(index)[0].value, file.row(index)[1].value, file.row(index)[2].value)
        patient_id = None
        for tmp in result_list:
            if tmp[1] == file.row(index)[2].value:
                patient_id = tmp[0]
                break
        content_insert = (get_uuid(), file.row(index)[0].value, file.row(index)[1].value,
                          patient_id, 0, 'zhiming', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cur.execute('insert into mdm_master values (?, ?, ?, ?, ?, ?, ?)', content_insert)
    print("数据写入完成,正在提交事务......")
    conn.commit()
    cur.close()
    conn.close()


def mdm_item():
    file_p = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm_ws"
    file_list = walkFile(file_p)
    # 1.获取数据库记录list
    db_path = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
    conn = sqlite3.connect(db_path, timeout=2000)
    cur = conn.cursor()
    sql = "select id, name from mdm_master where parent_id <> 0;"
    result_list = cur.execute(sql).fetchall()
    count = 0
    for file_path in file_list:
        # print(file_path)
        file = xlrd.open_workbook(file_path)
        for index_sheet in file.sheet_names():
            print(f'正在为{index_sheet}表格中的数据......')
            sheet = file.sheet_by_name(index_sheet)
            for row in range(1, sheet.nrows):
                # print(ssheet.row(row)[0].value, sheet.row(row)[1].value, sheet.row(row)[2].value,
                #       sheet.row(row)[3].value, sheet.row(row)[4].value, sheet.row(row)[5].value,
                #       sheet.row(row)[6].value)
                patient_id = None
                for tmp in result_list:
                    if tmp[1] == index_sheet.split(r'-')[1][:-7]:
                        patient_id = tmp[0]
                        break
                if not patient_id:
                    print(f'根据{index_sheet},截取后为:{index_sheet.split(r"-")[1][:-7]},未找到对应得目前,请手动检查!')
                    return
                content_insert = (
                get_uuid(), sheet.row(row)[0].value, sheet.row(row)[2].value, patient_id, sheet.row(row)[1].value,
                sheet.row(row)[3].value, sheet.row(row)[4].value, sheet.row(row)[5].value, sheet.row(row)[6].value,
                0, 'zhiming', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), row - 1)
                cur.execute("insert into mdm_master_item values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            content_insert)
                count += 1
                print(f"写入了数据第{count}条数据")

    print(f'完成写入数据,请查看数据库效果!一共写入数据{count}条!')
    conn.commit()
    cur.close()
    conn.close()


def mdm_insert():
    db_path = r"C:\Users\andy\OneDrive\文档\恺恩泰\mdm\mdm.db"
    conn = sqlite3.connect(db_path, timeout=2000)
    cur = conn.cursor()
    content_insert = (get_uuid(), 'V1.0', '国家卫生标准委员会信息标准专业委员会', '电子病历',
                      '分类法', '卫生部统计信息中心', '标准状态', '中国人民解放军总医院)',
                      0, 'zhiming', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cur.execute('insert into mdm_common values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', content_insert)
    print(f'成功插入数据到数据库!\n{content_insert}')
    conn.commit()
    cur.close()
    conn.close()


# 遍历文件夹
def walkFile(file):
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


if __name__ == "__main__":
    # mdm_insert()
    mdm_item()
    # pass
