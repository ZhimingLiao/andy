# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 茅岗新村  志明  2018-12-08 9:18
# 当前计算机登录名称 :志明
# 项目名称  :
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2018-12-08 '

from queue import Queue

if __name__ == '__main__':
    cats = {
        u'影视': '.avi.mp4.rmvb.m2ts.wmv.mkv.flv.qmv.rm.mov.vob.asf.3gp.mpg.mpeg.m4v.f4v.',
        u'图像': '.jpg.bmp.jpeg.png.gif.tiff.',
        u'文档书籍': '.pdf.isz.chm.txt.epub.bc!.doc.ppt.',
        u'音乐': '.mp3.ape.wav.dts.mdf.flac.',
        u'压缩文件': '.zip.rar.7z.tar.gz.iso.dmg.pkg.',
        u'安装包': '.exe.app.msi.apk.'
    }
    for k, v in cats.items():
        print(v)

    q = Queue(maxsize=100000)
    print(q.qsize())