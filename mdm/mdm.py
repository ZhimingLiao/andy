# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-12-16 16:09
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
import os
import sys

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

# 处理excel数据导入到es数据库
import mdm_excel

from ui.main import Ui_MainWindow
from readme import readme


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    def import_data(self):
        self.btn_import.setText("正在处理...")
        self.btn_import.setEnabled(False)
        # 开始调用函数处理请求
        result = mdm_excel.main(self.le_filepath.text(), self.le_es_ip.text())
        msg = QMessageBox.information(None, "温馨提示", result['msg'], QMessageBox.Yes)

        # 处理完成之后
        self.btn_import.setText("开始导入")
        self.btn_import.setEnabled(True)

    def show_readme(self):
        # self.readme.show()
        if not hasattr(self, "readme"):
            self.readme = readme()
        self.readme.show()

    def file_path_select(self):
        """
        选择文件路径操作,把文件路径写入到编辑框
        :return:
        """
        file_choose, filetype = QFileDialog. \
            getOpenFileName(None, "选取文件", '..', "Text Files (*.xlsx);;Text Files (*.xls);;All Files (*)")
        self.le_filepath.setText(file_choose)


def main():
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
