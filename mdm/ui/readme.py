# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\andy\Desktop\readme.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_readme(object):
    def setupUi(self, readme):
        readme.setObjectName("readme")
        readme.resize(400, 300)
        readme.setMinimumSize(QtCore.QSize(400, 300))
        readme.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setBold(True)
        font.setWeight(75)
        readme.setFont(font)
        self.readme_title = QtWidgets.QLabel(readme)
        self.readme_title.setGeometry(QtCore.QRect(60, 10, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.readme_title.setFont(font)
        self.readme_title.setObjectName("readme_title")
        self.readme_msg = QtWidgets.QLabel(readme)
        self.readme_msg.setGeometry(QtCore.QRect(60, 40, 271, 131))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.readme_msg.setFont(font)
        self.readme_msg.setWordWrap(True)
        self.readme_msg.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.readme_msg.setObjectName("readme_msg")
        self.buttonBox = QtWidgets.QDialogButtonBox(readme)
        self.buttonBox.setGeometry(QtCore.QRect(210, 250, 156, 23))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.buttonBox.setFont(font)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(readme)
        # self.buttonBox.clicked()
        self.buttonBox.accepted.connect(self.hide_win)
        QtCore.QMetaObject.connectSlotsByName(readme)

    def retranslateUi(self, readme):
        _translate = QtCore.QCoreApplication.translate
        readme.setWindowTitle(_translate("readme", "关于本程序"))
        self.readme_title.setText(_translate("readme", "关于本程序"))
        self.readme_msg.setText(_translate("readme", "请根据本程序的提示进行操作;本程序仅适合根据指定excel格式,请按照说明配置对应的文件!"))
