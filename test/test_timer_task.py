# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
#   Copyright (C) 2020 liaozhimingandy@qq.com Ltd. All Rights Reserved.
#
#   @Author      : zhiming
#   @Project     : zhiming
#   @File Name   : test_timer_task.py	
#   @Created Date: 2020-04-23 9:13
#      @Software : PyCharm
#         @e-Mail: liaozhimingandy@qq.com
#   @Description : 定时执行代码
#
# ======================================================================
import os
import sys
import threading
import time

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

curTime = time.strftime("%Y-%m-%d", time.localtime())   # 记录当前时间
execF = False
ncount=0


def execTask():
    # 具体任务执行内容
    print("任务执行!")


def timerTask():
    global execF
    global curTime
    global ncount
    if execF is False:
        execTask()  # 判断任务是否执行过，没有执行就执行
        execF=True
    else:   # 任务执行过，判断时间是否新的一天。如果是就执行任务
        desTime = time.strftime("%Y-%m-%d", time.localtime())
        if desTime > curTime:
            execF = False   # 任务执行执行置值为
            curTime = desTime
    ncount = ncount+1
    timer = threading.Timer(5, timerTask)
    timer.start()
    print(f"定时器执行{ncount}次!当前日期: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")


def main():
    timer = threading.Timer(5, timerTask)
    timer.start()


if __name__ == "__main__":
    main()
