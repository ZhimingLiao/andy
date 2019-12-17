# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 杭州  志明  2019-12-16 18:38
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm

# 使用抽象方法,在子类实现其余方法

from PyQt5.QtWidgets import QApplication, QMainWindow

from ui.readme import Ui_readme


class readme(QMainWindow, Ui_readme):
    def __init__(self, parent=None):
        super(readme, self).__init__(parent)
        self.setupUi(self)

    def hide_win(self):
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    myWin = readme()
    myWin.show()
    sys.exit(app.exec_())
