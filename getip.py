# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets  import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal
import pymysql
import os
import uuid
import socket
import getpass
import win32api
import win32con
import time
import image_rc
from PyQt5 import sip
import subprocess

class Ui_HomePage(QWidget):
    """ 主页"""
    def __init__(self):
        super(Ui_HomePage, self).__init__()
        self.conn=''
        self.cur=''
        self.isLogin=False
        self.sendipThread=SendIPThread()
        self.sendipThread.senip.connect(self.sendIPToServer)
        if(os.path.exists("config.py")==False):#不存在在配置文件的话就建立配置文件
            self.newConfigFile()
        self.config=self.loadCongfigFile('config.py')#加载配置文件
        self.setupUi()
        if(self.config['remberPassword']==True):#将配置文件中保存的帐户名和密码加到表单中
            self.usernameEdit.setText(self.config['username'])
            self.passwordEdit.setText(self.config['password'])
            self.remerberBox.toggle()
        if(self.config['autoLogin']==True):#默认自动登陆，系统不可修改
            self.login()
        #self.startingUpWindow()

    def setupUi(self):
        """主页上的控件"""
        """大部分是直接通过QT工具Designer生成UI，然后在其基础上修改了部分样式"""
        #主界面设置
        self.setObjectName("HomePage")
        self.resize(940, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(940, 500))
        self.setMaximumSize(QtCore.QSize(940, 500))
        self.setBaseSize(QtCore.QSize(1199, 650))
        self.setStyleSheet("color: rgb(26, 23, 17);\n""background-image: url(:/image/homeBg.png);")
        self.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        #右侧登陆界面设置
        self.loginPage = QtWidgets.QWidget(self)
        self.loginPage.setGeometry(QtCore.QRect(370, 100, 545, 270))
        self.loginPage.setMinimumSize(QtCore.QSize(545, 270))
        self.loginPage.setMaximumSize(QtCore.QSize(545, 270))
        self.loginPage.setSizeIncrement(QtCore.QSize(545, 270))
        self.loginPage.setMouseTracking(False)
        self.loginPage.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.loginPage.setStyleSheet("background-image: url(:/image/loginBg.png);\n")
        self.loginPage.setObjectName("loginPage")
        #“登陆”文字
        self.loginText = QtWidgets.QWidget(self.loginPage)
        self.loginText.setGeometry(QtCore.QRect(40, 30, 44, 18))
        self.loginText.setMinimumSize(QtCore.QSize(44, 18))
        self.loginText.setMaximumSize(QtCore.QSize(44, 18))
        self.loginText.setSizeIncrement(QtCore.QSize(44, 18))
        self.loginText.setBaseSize(QtCore.QSize(44, 18))
        self.loginText.setStyleSheet("background-image: url(:/image/loginText.png);")
        self.loginText.setObjectName("loginText")
        #“注册”文字
        self.registText = QtWidgets.QWidget(self.loginPage)
        self.registText.setGeometry(QtCore.QRect(370, 30, 45, 19))
        self.registText.setMinimumSize(QtCore.QSize(45, 19))
        self.registText.setMaximumSize(QtCore.QSize(45, 19))
        self.registText.setSizeIncrement(QtCore.QSize(45, 19))
        self.registText.setBaseSize(QtCore.QSize(44, 19))
        self.registText.setStyleSheet("image: url(:/image/registText.png);")
        self.registText.setObjectName("registText")
        #“free accout”文字
        self.freeAccoutText = QtWidgets.QWidget(self.loginPage)
        self.freeAccoutText.setGeometry(QtCore.QRect(370, 60, 88, 13))
        self.freeAccoutText.setMinimumSize(QtCore.QSize(88, 13))
        self.freeAccoutText.setMaximumSize(QtCore.QSize(88, 13))
        self.freeAccoutText.setStyleSheet("image: url(:/image/freeAccount.png);")
        self.freeAccoutText.setObjectName("freeAccoutText")
        #“本软件不提供...”文字
        self.registticText = QtWidgets.QWidget(self.loginPage)
        self.registticText.setGeometry(QtCore.QRect(370, 90, 157, 56))
        self.registticText.setMinimumSize(QtCore.QSize(157, 56))
        self.registticText.setMaximumSize(QtCore.QSize(157, 56))
        self.registticText.setSizeIncrement(QtCore.QSize(157, 56))
        self.registticText.setBaseSize(QtCore.QSize(157, 56))
        self.registticText.setStyleSheet("image: url(:/image/registPrompt.png);")
        self.registticText.setObjectName("registticText")
        #用户名输入框
        self.usernameEdit = QtWidgets.QLineEdit(self.loginPage)
        self.usernameEdit.setGeometry(QtCore.QRect(60, 90, 271, 34))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usernameEdit.sizePolicy().hasHeightForWidth())
        self.usernameEdit.setSizePolicy(sizePolicy)
        self.usernameEdit.setMinimumSize(QtCore.QSize(271, 34))
        self.usernameEdit.setMaximumSize(QtCore.QSize(271, 34))
        self.usernameEdit.setSizeIncrement(QtCore.QSize(274, 34))
        self.usernameEdit.setBaseSize(QtCore.QSize(274, 34))
        palette = QtGui.QPalette()
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.usernameEdit.setPalette(palette)
        font = QtGui.QFont()
        self.usernameEdit.setFont(font)
        self.usernameEdit.setWhatsThis("")
        #输入框样式
        self.usernameEdit.setStyleSheet("border-radius:5px;\n"
"selection-color: rgb(255, 255, 255);\n"
"width: 100%; \n"
"height: 34px; \n"
"padding: 6px 12px; \n"
"font-size: 14px; \n"
"line-height: 1.428571429; \n"
"color:#fff; \n"
"vertical-align: middle; \n"
"color: qradialgradient(spread:repeat, cx:0.5, cy:0.5, radius:0.077, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 0), stop:0.497326 rgba(255, 255, 255, 0), stop:1 rgba(255, 255, 255, 0));\n"
"border: 1px solid #cccccc; \n"
"border-radius: 4px; \n"
"BACKGROUND-COLOR: transparent;")
        self.usernameEdit.setText("")
        self.usernameEdit.setMaxLength(20)
        self.usernameEdit.setReadOnly(False)
        self.usernameEdit.setProperty("setPlaceholderText(\"username\")", "")
        self.usernameEdit.setObjectName("usernameEdit")
        #密码输入框
        self.passwordEdit = QtWidgets.QLineEdit(self.loginPage)
        self.passwordEdit.setGeometry(QtCore.QRect(60, 140, 271, 34))
        self.passwordEdit.setMinimumSize(QtCore.QSize(271, 34))
        self.passwordEdit.setMaximumSize(QtCore.QSize(271, 34))
        self.passwordEdit.setSizeIncrement(QtCore.QSize(274, 34))
        self.passwordEdit.setBaseSize(QtCore.QSize(274, 34))
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        palette = QtGui.QPalette()
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        gradient = QtGui.QRadialGradient(0.5, 0.5, 0.077, 0.5, 0.5)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 169, 255, 147))
        gradient.setColorAt(0.497326, QtGui.QColor(0, 0, 0, 147))
        gradient.setColorAt(1.0, QtGui.QColor(0, 169, 255, 147))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.passwordEdit.setPalette(palette)
        font = QtGui.QFont()
        self.passwordEdit.setFont(font)
        self.passwordEdit.setWhatsThis("")
        self.passwordEdit.setStyleSheet("border-radius:5px;\n"
"selection-color: rgb(255, 255, 255);\n"
"width: 100%; \n"
"height: 34px; \n"
"padding: 6px 12px; \n"
"font-size: 14px; \n"
"line-height: 1.428571429; \n"
"color:#fff; \n"
"vertical-align: middle; \n"
"color: qradialgradient(spread:repeat, cx:0.5, cy:0.5, radius:0.077, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 0), stop:0.497326 rgba(255, 255, 255, 0), stop:1 rgba(255, 255, 255, 0));\n"
"border: 1px solid #cccccc; \n"
"border-radius: 4px; \n"
"BACKGROUND-COLOR: transparent;")
        self.passwordEdit.setMaxLength(20)
        self.passwordEdit.setProperty("setPlaceholderText(\"username\")", "")
        self.passwordEdit.setObjectName("passwordEdit")
        #登陆按钮
        self.loginButton = QtWidgets.QPushButton(self.loginPage)
        self.loginButton.setGeometry(QtCore.QRect(240, 200, 85, 33))
        self.loginButton.setMinimumSize(QtCore.QSize(85, 33))
        self.loginButton.setMaximumSize(QtCore.QSize(85, 33))
        self.loginButton.setSizeIncrement(QtCore.QSize(85, 33))
        self.loginButton.setBaseSize(QtCore.QSize(85, 33))
        self.loginButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loginButton.clicked.connect(self.login)
        #self.loginButton.setStyleSheet("QPushButton{border-image: url(:/image/logoutButton.png);}"
                                       #"QPushButton:hover{border-image: url(:/image/logoutHoverButton.png);}")
        self.loginButton.setStyleSheet("QPushButton{border-image: url(:/image/loginButton.png);}"
                                        "QPushButton:hover{border-image: url(:/image/loginHoverButton.png);}")
        self.loginButton.setText("")
        self.loginButton.setObjectName("loginButton")
        #“remeber me”文字
        self.remerbermeText = QtWidgets.QWidget(self.loginPage)
        self.remerbermeText.setGeometry(QtCore.QRect(90, 220, 77, 13))
        self.remerbermeText.setMinimumSize(QtCore.QSize(77, 13))
        self.remerbermeText.setMaximumSize(QtCore.QSize(77, 13))
        self.remerbermeText.setSizeIncrement(QtCore.QSize(77, 13))
        self.remerbermeText.setBaseSize(QtCore.QSize(77, 13))
        self.remerbermeText.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.remerbermeText.setStyleSheet("image: url(:/image/rememberme.png);")
        self.remerbermeText.setObjectName("remerbermeText")
        self.remerberBox = QtWidgets.QCheckBox(self.loginPage)
        self.remerberBox.setGeometry(QtCore.QRect(70, 220, 13, 13))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remerberBox.sizePolicy().hasHeightForWidth())
        #“remeber me”选择框
        self.remerberBox.setSizePolicy(sizePolicy)
        self.remerberBox.setText("")
        self.remerberBox.setObjectName("remerberBox")
        self.registButton = QtWidgets.QPushButton(self.loginPage)
        self.registButton.setGeometry(QtCore.QRect(390, 160, 85, 33))
        self.registButton.setMinimumSize(QtCore.QSize(85, 33))
        self.registButton.setMaximumSize(QtCore.QSize(85, 33))
        self.registButton.setSizeIncrement(QtCore.QSize(85, 33))
        self.registButton.setBaseSize(QtCore.QSize(85, 33))
        self.registButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.registButton.setStyleSheet("QPushButton{border-image: url(:/image/registButton.png);}"
                                        "QPushButton:hover{border-image: url(:/image/registhoverButton.png);}")
        self.registButton.setText("")
        self.registButton.setObjectName("registButton")
        self.loginText.raise_()
        self.registText.raise_()
        self.freeAccoutText.raise_()
        self.registticText.raise_()
        self.passwordEdit.raise_()
        self.loginButton.raise_()
        self.remerbermeText.raise_()
        self.remerberBox.raise_()
        self.registButton.raise_()
        self.usernameEdit.raise_()
        #日志框，即系统消息
        self.logWidget = QtWidgets.QWidget(self)
        self.logWidget.setGeometry(QtCore.QRect(50, 100, 235, 268))
        self.logWidget.setMinimumSize(QtCore.QSize(235, 268))
        self.logWidget.setStyleSheet("background-image: url(:/image/logBg.png);")
        self.logWidget.setObjectName("logWidget")
        #日志输出框
        self.logEdit = QtWidgets.QTextEdit(self.logWidget)
        self.logEdit.setGeometry(QtCore.QRect(30, 50, 181, 191))
        self.logEdit.setObjectName("logEdit")
        self.logEdit.setEnabled(False)
        self.systemMessgewidget = QtWidgets.QWidget(self.logWidget)
        self.systemMessgewidget.setGeometry(QtCore.QRect(70, 20, 87, 19))
        self.systemMessgewidget.setMinimumSize(QtCore.QSize(87, 19))
        self.systemMessgewidget.setMaximumSize(QtCore.QSize(87, 19))
        self.systemMessgewidget.setSizeIncrement(QtCore.QSize(87, 19))
        self.systemMessgewidget.setBaseSize(QtCore.QSize(87, 19))
        self.systemMessgewidget.setStyleSheet("background-image: url(:/image/systemMessage.png);")
        self.systemMessgewidget.setObjectName("systemMessgewidget")
        self.homebgwidget = QtWidgets.QWidget(self)
        self.homebgwidget.setGeometry(QtCore.QRect(0, 0, 941, 501))
        self.homebgwidget.setObjectName("homebgwidget")
        self.homebgwidget.raise_()
        self.loginPage.raise_()
        self.logWidget.raise_()

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, HomePage):
        _translate = QtCore.QCoreApplication.translate
        HomePage.setWindowTitle(_translate("HomePage", "主页"))
        self.usernameEdit.setPlaceholderText(_translate("HomePage", "username"))
        self.passwordEdit.setPlaceholderText(_translate("HomePage", "password"))

    def login(self):
        """按下登陆按钮的操作"""
        cueerntTime = time.strftime("%H:%M:%S::", time.localtime(time.time()))#获取当前时间
        if(self.isLogin==False): #未登陆的操作
            if(self.connectToServer()):
                username=self.usernameEdit.text()
                password=self.passwordEdit.text()
                if(username=='' or password==''):
                    self.logEdit.append(cueerntTime + "用户名或密码不能为空")
                else:
                    sqlString="SELECT COUNT(username) FROM userinfo WHERE username='"+username+"' AND password='"+password+"'"
                    self.cur.execute(sqlString)
                    if(self.cur._rows[0][0]>0):#登陆成功
                        self.logEdit.append(cueerntTime + "登陆成功！")
                        self.isLogin=True
                        self.usernameEdit.setEnabled(False)
                        self.passwordEdit.setEnabled(False)
                        self.loginButton.setStyleSheet("QPushButton{border-image: url(:/image/logoutButton.png);}"
                                                        "QPushButton:hover{border-image: url(:/image/logoutHoverButton.png);}")
                        if(self.remerberBox.isChecked()):
                            self.config['autoLogin'] = True
                            self.config['remberPassword'] = True
                            self.config['username'] =username
                            self.config['password'] =password
                        self.updateConfigFile()
                        self.sendipThread.start()
                    else:
                        self.logEdit.append(cueerntTime + "登陆失败！请检查账户名和密码！！！")
        else:#登录后的操作
            self.isLogin = False
            self.usernameEdit.setEnabled(True)
            self.passwordEdit.setEnabled(True)
            self.logEdit.append(cueerntTime + "退出成功！！！")
            self.loginButton.setStyleSheet("QPushButton{border-image: url(:/image/loginButton.png);}"
                                           "QPushButton:hover{border-image: url(:/image/loginHoverButton.png);}")

    def connectToServer (self):
        """连接服务器数据库"""
        cueerntTime = time.strftime("%H:%M:%S::", time.localtime(time.time()))
        try:
            self.conn = pymysql.connect(host='47.106.22.99', port=3306, user='getip', password='root', db='getip',
                                        charset='utf8')
            self.cur = self.conn.cursor()
            #self.logEdit.append(cueerntTime+"服务器连接成功")
            return True
        except:
            self.logEdit.append(cueerntTime+"服务器连接失败,请稍后重试")
            return False

    def newConfigFile(self):
        """建立配置文件"""
        configFile = "config.py"
        trans_fp = open(configFile, 'w')
        config={}
        config['autoLogin']=False
        config['remberPassword']=False
        config['username']=''
        config['password']=''
        trans_fp.write(str(config))
        trans_fp.close()

    def updateConfigFile(self):
        """更新配置文件"""
        configFile = "config.py"
        trans_fp = open(configFile, 'w')
        trans_fp.write(str(self.config))
        trans_fp.close()

    def loadCongfigFile(self,filename):
        """加载配置文件"""
        str = open(filename, 'r').read()
        return eval(str)

    def sendIPToServer(self):
        cueerntTime = time.strftime("%H:%M:%S::", time.localtime(time.time()))  # 获取当前时间
        if(self.isLogin==True):
            if (self.connectToServer()):
                username = self.usernameEdit.text()
                computeMac = uuid.UUID(int=uuid.getnode()).hex[-12:]
                computeMac=":".join([computeMac[e:e+2] for e in range(0,11,2)])
                computerName = socket.gethostname()
                computerIP = socket.gethostbyname(computerName)
                conmputeUsername=getpass.getuser()
                sqlString ="SELECT COUNT(username) FROM userip WHERE username='"+username+"' AND mac='"+computeMac+"'"
                self.cur.execute(sqlString)
                if (self.cur._rows[0][0] > 0):  # 数据库表存在用户名和MAC，则更新
                    sqlString="UPDATE userip SET loginname='"+conmputeUsername+"', ip='"+computerIP+"',lastupdatetime=NOW() WHERE username='"+username+"' AND mac='"+computeMac+"'"
                    self.cur.execute(sqlString)
                    self.conn.commit()
                    print("存在")
                else:
                    sqlString="INSERT INTO userip(username,mac,loginname,ip,lastupdatetime) VALUES('"+username+"','"+computeMac+"','"+conmputeUsername+"','"+computerIP+"',NOW())"
                    self.cur.execute(sqlString)
                    self.conn.commit()
                    print("不存在，插入")
            print("登陆成功后发送IP")
        print("正在向服务器发送IP")

    def startingUpWindow(self):
        """实现开机自启"""
        name = 'oftpublic'  # 要添加的项值名称
        print()
        path = os.getcwd()+'\getip.exe'  # 要添加的exe路径
        # 注册表项名
        KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        # 异常处理
        try:
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
            win32api.RegCloseKey(key)
        except:
            print('error')
        print('开机启动成功！')

class SendIPThread(QtCore.QThread):
    senip = pyqtSignal()
    def __init__(self, parent=None):
        self.bootJudgment()
        QtCore.QThread.__init__(self, parent)

    def run(self):#每个两秒向服务器更新一次IP地址
        while(True):
            self.sleep(2)
            self.senip.emit()

    def bootJudgment(self):
        """开机判断是否连上网，没有连上则睡眠30s"""
        isLinkNetwork = subprocess.call('ping www.baidu.com', shell=True)
        while(isLinkNetwork!=0) :
            isLinkNetwork = subprocess.call('ping www.baidu.com', shell=True)#重复判断是否连接网络
            self.sleep(30)#连接不上网络就继续连接

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainMindow = Ui_HomePage()
    mainMindow.show()
    sys.exit(app.exec_())