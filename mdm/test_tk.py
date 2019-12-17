# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-11-29 14:27
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
import socket
import threading
import time
import tkinter as tk
import tkinter.messagebox
from datetime import datetime
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk

import utils
from Tools.ElasticSearchTool.ElasticSearchImporter import ElasticSearchImporter as es
from mdm.test_mdm import MDMOptionor


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)


# 打开文件对话框
def open_file(content):
    global ask_file_name
    ask_file_name = askopenfilename()
    if not ask_file_name:
        return
    print_log(f"\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())};您刚才选择了文件路径:{ask_file_name}")
    if len(ask_file_name) > 20: file_name = ask_file_name[0:5] + "..." + ask_file_name[-13:]
    content.set(file_name)


# 得到当前时间上午下午判断
def get_time_name():
    hour = datetime.now().hour
    if hour in (0, 1, 2):
        return "凌晨"
    elif hour in (3, 4, 5):
        return "黎明"
    elif hour in (6, 7):
        return "早晨"
    elif hour in (8, 9, 10, 11):
        return "上午"
    elif hour in (12, 13):
        return "中午"
    elif hour in (14, 15, 16, 17):
        return "下午"
    elif hour in (18, 19, 20, 21, 22):
        return "晚上"
    else:
        return "夜间"


def test_port_use(ip, port):
    '''
       检测指定的IP的端口是否开启监听
       :param ip: 测试ip地址
       :param port: 连接的端口号
       :return: 处理结果
       '''
    # 使用TCP连接方式
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        st.settimeout(2)
        st.connect((ip, port))
        # print("%s的IP的端口%d已连接!" % (ip, port))
    except WindowsError:
        result = False
        error = 1
    except Exception as e:
        result = False
        error = 2
    else:
        result = True
        error = 0
    finally:
        st.close()
        return {'error': error, 'msg': f'ip:{ip};端口号{port}连接成功' if error < 1 else f'ip:{ip};端口号:{port}未开放',
                'result': result}


def test_es(es_addr):
    threading.Thread(target=test_es_thread, args=(es_addr,)).start()
    print_log(f"\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())};您刚才操作了测试数据连接,连接地址是:{es_addr}")


def string_to_ip_port(string):
    import re
    ip_port_format = ('(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.'
                      '(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.'
                      '(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.'
                      '(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\:'
                      '(\d+/)')
    res = re.findall(ip_port_format, string.replace("localhost", "127.0.0.1"))
    return ".".join(res[0][0:4]), int(res[0][4].replace(r"/", "").strip())


def test_es_thread(es_addr):
    import re
    error = 0
    ip_port_format = ('(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.'
                      '(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.'
                      '(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.'
                      '(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\:'
                      '(\d+/)')
    if not re.search(ip_port_format, es_addr.replace("localhost", "127.0.0.1")):
        tkinter.messagebox.showinfo("温馨提示", "es地址不正确!")
        error = 1
        return {"error": error, "msg": "连接失败!"}
    res = re.findall(ip_port_format, es_addr.replace("localhost", "127.0.0.1"))
    ip, port = ".".join(res[0][0:4]), int(res[0][4].replace(r"/", "").strip())
    res = test_port_use(ip, port)
    if res['error'] > 0:
        tkinter.messagebox.showwarning("温馨提示", f"连接数据地址为:{es_addr}失败!请检查本机是否可以ping通对应的数据库!")
        error = 2
        return {"error": error, "msg": "连接失败!"}
    e = es(ip, port)
    res = e.search_size(index_name="mdms.entity.masterdatamanage.master_definition")
    tkinter.messagebox.showinfo("成功提示", f"恭喜您连接ES数据库:{es_addr}成功!,在定义表共找到{res}条记录!")
    return {"error": error, "msg": "连接成功!"}
    # res = test_port_use(ip, port)
    # print(res)


def print_log(msg):
    tx.config(state=tk.NORMAL)
    tx.insert(tk.END, msg)
    tx.config(state=tk.DISABLED)


def mdm_import(index, uuid):
    t = test_es_thread(index)
    if t.get("error") > 0:
        print_log(msg=f"\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())};您点击了导入\还原操作!(备注:{t})")
        return {"error": 0, "msg": "因es数据库连接失败,导致无法继续执行下面代码!"}

    index, uuid, file_name = index.strip(), uuid.strip(), file_path["text"].strip()
    index_define = r"mdms.entity.masterdatamanage.master_definition"
    index_pro = r"mdms.entity.masterdatamanage.master_property"
    index_men = r"mdms.entity.masterdatamanage.master_member"
    print_log(msg=f"\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())};您点击了导入\还原操作!")
    if not index or not uuid:
        tkinter.messagebox.showinfo("温馨提示", f"索引名称:{index}, uuid:{uuid};请检查...")
        return

    ip, port = string_to_ip_port(string=index.strip())
    e = es(ip, port)
    res = e.search_by_body(index_name=index_define, MASTER_DEF_ID=uuid)['hits']
    if not res['total']:
        tkinter.messagebox.showinfo("温馨提示", f"根据uuid:{uuid}在定义表{index_define}没有找到数据;请检查...")
        return
    ok = tkinter.messagebox.askokcancel('提示',
                                        f'根据您输入的id:{uuid},找到{res["total"]}条记录\n名称是:{res["hits"][0]["_source"]["MASTER_DEF_NAME"]}'
                                        f'\n是否继续下一步操作(1.在属性表建立属性;2.成员表写入数据)')
    if not ok:
        print_log(msg=f"\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())};您取消了导入\还原操作!")
        return
    data_xls = utils.get_data(ask_file_name)
    ses = MDMOptionor(mes=e)
    ses.create_pro(index=index_pro, MASTER_DEF_ID=uuid)
    res = ses.create_men(index=index_men, data_dict=data_xls, MASTER_DEF_ID=uuid, flag_deleted=v.get())
    return res


def main():
    # 第1步，实例化object，建立窗口window
    window = tk.Tk()

    # 第2步，给窗口的可视化起名字
    window.title('主数据同步助手(' + get_time_name() + "好!)")

    # 第3步，设定窗口的大小(长 * 宽)
    center_window(window, 600, 400)
    # window.maxsize(800, 600)
    # window.minsize(300, 240)
    window.resizable(0, 0)
    # window.update()

    ask_file_name = None
    # 第4步，在图形界面上设定标签
    lab = tk.Label(window, text='你好！这是主数据字典同步工具!', bg='green', font=('微软雅黑', 12), width=30, height=2)

    # 第5步，放置标签
    lab.grid(row=0, columnspan=2)  # Label内容content区域放置位置，自动调节尺寸
    frame = tk.Frame(window, height=200, width=400)
    frame.grid(row=1, column=0)
    frame1 = tk.Frame(window, height=200, width=200)
    frame1.grid(row=1, column=1)
    frame2 = tk.Frame(window, height=300, width=600)
    frame2.grid(row=2, column=0, columnspan=2)

    # 添加控件
    tk.Label(frame, font=('微软雅黑', 12), text="ip地址:").grid(row=0, column=0, padx=10, pady=3, sticky=tk.E)  # 靠右
    es_addr = tk.StringVar(window, value="http://localhost:9200/")
    e = tk.Entry(frame, font=('微软雅黑', 12), width=26, textvariable=es_addr)
    e.grid(row=0, column=1, columnspan=3, pady=3)

    # 添加需要关联的数据id
    tk.Label(frame, font=('微软雅黑', 12), text="索引名或id:").grid(row=1, column=0, padx=10, pady=0, sticky=tk.E)
    es_id = tk.StringVar(window, value="32位的uuid或者索引名称")
    e_id = tk.Entry(frame, font=('微软雅黑', 12), width=26, textvariable=es_id)
    e_id.grid(row=1, column=1, columnspan=3, pady=3)

    # 文件框选项
    content = tk.StringVar(window, "点击左边按钮进行选择文件路径")
    tk.Button(frame, font=('微软雅黑', 12), text="选择文件路径:", command=lambda: open_file(content), bg="white") \
        .grid(row=2, column=0, pady=0, padx=10)
    global file_path
    file_path = tk.Label(frame, font=('微软雅黑', 10), textvariable=content, justify=tk.LEFT, width=25)
    file_path.grid(row=2, column=1, padx=10, pady=0, sticky=tk.E)
    file_path.config(text=content)
    global ck
    global v
    v = tk.IntVar()
    v.set(1)
    ck = tk.Checkbutton(frame, text="先删除后导入(默认不删除)", variable=v, font=('微软雅黑', 12))
    ck.select()
    ck.grid(row=3, column=0, pady=2, padx=2, columnspan=2)
    tk.Label(frame, font=('微软雅黑', 10), text="使用流程:\n1.得到定义表新增生成的uuid\n2.生成属性表数据以及根据导入文件导入数据到成员表",
             justify=tk.LEFT).grid(row=4, column=0, sticky=tk.E + tk.W, columnspan=3)

    # 右边进行确定操作
    img = Image.open(r"C:\Users\andy\OneDrive\文档\docs\docs\浙江省肿瘤医院\docs\imgs\logo.png")
    img2 = img.resize((200, 80))
    photo = ImageTk.PhotoImage(img2)
    tk.Label(frame1, image=photo, width=200, height=80) \
        .grid(row=0, columnspan=2, sticky=tk.E + tk.W)
    tk.Button(frame1, font=('微软雅黑', 12), text="测试es数据库连接", bg="white", command=lambda: test_es(es_addr.get())) \
        .grid(row=1, sticky=tk.E + tk.W)
    tk.Button(frame1, font=('微软雅黑', 12), text=r"导入\还原", bg="white",
              command=lambda: mdm_import(es_addr.get(), es_id.get())) \
        .grid(row=2, sticky=tk.E + tk.W)
    tk.Button(frame1, font=('微软雅黑', 12), text=r"导出\备份", bg="white") \
        .grid(row=3, sticky=tk.E + tk.W)

    # 日志输入区域
    global tx
    tx = scrolledtext.ScrolledText(frame2, font=('微软雅黑', 10), height=8, width=72, wrap=tk.WORD)
    tx.grid(row=0, columnspan=3)
    tx.insert("end", "此处为日志输出区域...")
    tx.config(state=tk.DISABLED)
    # 固定frame容器大小
    frame.grid_propagate(0)
    frame1.grid_propagate(0)
    frame2.grid_propagate(0)

    # 第6步，主窗口循环显示
    window.mainloop()


if __name__ == "__main__":
    main()