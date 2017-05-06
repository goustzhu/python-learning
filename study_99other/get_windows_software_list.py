#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/3/25 9:36
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : get_windows_software_list.py
import sys, os, time, datetime

reload(sys)
sys.setdefaultencoding('utf-8')
# -*- coding: UTF8 -*-
from PyQt4 import QtCore, QtGui
import _winreg
import re, sys, os, rcc
import win32ui
import win32gui

reload(sys)
sys.setdefaultencoding("utf-8")


class ListDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ListDialog, self).__init__(parent)

        self.contentsWidget = QtGui.QListWidget()
        self.contentsWidget.setViewMode(QtGui.QListView.IconMode)
        self.contentsWidget.setIconSize(QtCore.QSize(96, 84))  # Icon 大小
        self.contentsWidget.setMovement(QtGui.QListView.Static)  # Listview不让列表拖动
        self.contentsWidget.setMaximumWidth(800)  # 最大宽度
        self.contentsWidget.setSpacing(15)  # 间距大小

        winrege = winregeditor()
        self.numreg = winrege.getreg()
        for key in self.numreg.keys():
            Atem = QtGui.QListWidgetItem(self.contentsWidget)
            try:  # ico 来自exe
                large, small = win32gui.ExtractIconEx(self.numreg[key]['exe'], 0)
                exeMenu = self.numreg[key]['exe']
                win32gui.DestroyIcon(small[0])
                self.pixmap = QtGui.QPixmap.fromWinHBITMAP(self.bitmapFromHIcon(large[0]), 2)
            except Exception, e:  # ico 来自 icon
                if self.numreg[key].has_key('icon') and os.path.isfile(self.numreg[key]['icon']):  # 判断ico文件是否存在
                    self.pixmap = QtGui.QPixmap(self.numreg[key]['icon'])
                    iconMenu = self.numreg[key]['icon']
                    split = iconMenu.split('\\')
                    exeMenu = '\\'.join(split[:-1])
                else:  # 不存在ico文件给定默认图标
                    self.pixmap = ':default.png'
                    exeMenu = ''

            Atem.setIcon(QtGui.QIcon(self.pixmap))
            Atem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            Atem.setTextAlignment(QtCore.Qt.AlignHCenter)
            Atem.setData(QtCore.Qt.UserRole, exeMenu)
            DisplayName = self.numreg[key]['DisplayName'].encode('utf-8')
            Atem.setToolTip(u"" + DisplayName)  # tip 显示
            if len(DisplayName) >= 6:
                DisplayName = DisplayName.decode('utf8')[0:6].encode('utf8') + '…'
            Atem.setText(u"" + DisplayName)

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.addWidget(self.contentsWidget)
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle(u'Pyqt 显示已安装软件列表')
        self.setWindowIcon(QtGui.QIcon(':favicon.ico'))
        self.resize(600, 300)
        self.contentsWidget.itemDoubleClicked.connect(self.DoubleClicked)  # 双击事件

    # 当窗体大小改变后重新绘制窗体   重新排列Icon效果
    def paintEvent(self, event):
        mw = self.geometry()
        width = mw.width()  # 获取窗体宽度
        self.contentsWidget.setViewMode(QtGui.QListView.IconMode)
        self.contentsWidget.setIconSize(QtCore.QSize(96, 84))  # Icon 大小
        self.contentsWidget.setMaximumWidth(width)
        self.contentsWidget.setSpacing(12)  # 间距大小

    # win32 获取exe 资源
    def bitmapFromHIcon(self, hIcon):
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), hIcon)
        hdc.DeleteDC()
        return hbmp.GetHandle()

    # 双击事件
    def DoubleClicked(self):
        item = self.contentsWidget.currentItem()  # 获取当前item   <PyQt4.QtGui.QListWidgetItem object at 0x01775E40>
        location = item.data(QtCore.Qt.UserRole)  # 获取item里面的data  <PyQt4.QtCore.QVariant object at 0x018FD9B0>
        Obj = location.toPyObject()
        if Obj and os.path.exists(Obj):  # 文件or 目录存在
            if os.path.isfile(Obj):
                import win32process
                try:
                    win32process.CreateProcess(str(Obj), '', None, None, 0, win32process.CREATE_NO_WINDOW, None, None,
                                               win32process.STARTUPINFO())
                except Exception, e:
                    print(e)
            else:
                os.startfile(str(Obj))

        else:  # 不存在的目录
            QtGui.QMessageBox.warning(self, (u'提示'), (u'无法打开不存在的目录！'), QtGui.QMessageBox.Yes)


# 注册表操作
class winregeditor:
    dicList = {}

    def orderDict(self, numkey, DisplayName, DisplayIcon):
        self.dicList[numkey] = {'DisplayName': DisplayName, 'DisplayIcon': DisplayIcon}
        exeIcon = re.compile('.*exe')
        match = exeIcon.match(DisplayIcon)
        if match:  # 匹配到exe， 可直接打开
            self.dicList[numkey]['exe'] = match.group()
        else:  # 没有exe，Icon可为ico 文件
            self.dicList[numkey]['icon'] = DisplayIcon
        return self.dicList

    def getreg(self):
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0,
                              _winreg.KEY_ALL_ACCESS)
        for i in xrange(0, _winreg.QueryInfoKey(key)[0] - 1):
            DisplayName = ''
            DisplayIcon = ''
            try:
                key_name_list = _winreg.EnumKey(key, i)
                each_key_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" + '\\' + key_name_list
                each_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, each_key_path, 0, _winreg.KEY_ALL_ACCESS)
                DisplayName, REG_SZ = _winreg.QueryValueEx(each_key, "DisplayName")
                DisplayName = DisplayName.encode('utf-8')
                try:
                    DisplayIcon, REG_SZ = _winreg.QueryValueEx(each_key, "DisplayIcon")
                    DisplayIcon = DisplayIcon.encode('utf-8')
                except WindowsError:
                    pass
                # 注册表中同时满足DisplayName 和 DisplayIcon
                if DisplayName and DisplayIcon:
                    result = self.orderDict(str(i), DisplayName, DisplayIcon)
            except WindowsError:
                pass

        return result


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = ListDialog()
    dialog.show()
    sys.exit(app.exec_())