# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import *
import sys
from Ui_main import Ui_MainWindow
import translate
import numpy as np
import baiduapi

class BigWorkThread(QThread, QMainWindow, Ui_MainWindow):
    """docstring for BigWorkThread"""

    finishSignal = pyqtSignal(list)

    def __init__(self, text1, sim_text, parent=None):
        super(BigWorkThread, self).__init__(parent)
        self.text1 = text1
        self.sim_text = sim_text

    #重写 run() 函数，在里面干大事。
    def run(self):
        result = []

        try:
            for x in translate.google_translate_text(self.text1):
                if (x):
                    result1 = []
                    sim_result = []
                    for y in self.sim_text:
                        if (y):
                            sim_result.append((translate.sim_test(x, y) * 100))
                            mean = int(np.mean(sim_result))
                    # print(f"{mean}%",end="$")
                    mean_str = str(mean) + "%"
                    result1.append(mean_str)
                    result1.append(x)
                    result.append(result1)

        except Exception as e:
            print(e)
            result.append("@#^%$&^%$*^error发生错误#@%^%*%&%*&")
        finally:
            self.finishSignal.emit(result)










class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.id = 1
        self.lines = []

    
    def add_line(self, num, str_result):
        row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row + 1)
        id = str(self.id)
        self.tableWidget.setItem(row,0,QTableWidgetItem(num))
        self.tableWidget.setItem(row,1,QTableWidgetItem(str_result))
        self.id += 1
        self.lines.append([id,num,str_result])
    
    
    @pyqtSlot()
    def on_fanyiButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # raise NotImplementedError


        self.id = 1
        self.lines = []
        self.tableWidget.setRowCount(0);
        baiduapi.appid = self.lineEdit.text()
        baiduapi.secretKey = self.lineEdit_2.text()
        text1 = self.needTranslateText.toPlainText()
        sim_text1 = self.plainTextEdit.toPlainText()
        sim_text2 = self.plainTextEdit_2.toPlainText()
        sim_text3 = self.plainTextEdit_3.toPlainText()
        sim_text4 = self.plainTextEdit_4.toPlainText()
        sim_text5 = self.plainTextEdit_5.toPlainText()
        # if(not baiduapi.appid or not baiduapi.secretKey):
        #      QMessageBox.critical(self, "未输入Key", "请输入百度翻译appid和secretKey",  QMessageBox.Yes)
        # else:
        if(not text1 or not sim_text1):
            QMessageBox.critical(self, "未输入文本", "待降重文本和重复来源1不能为空",  QMessageBox.Yes)
        else:
            self.fanyiButton.setDisabled(True)
            self.label_8.setText("正在翻译，请稍候...")
            self.tableWidget.setSortingEnabled(False)
            sim_text = []
            if(sim_text1):
                sim_text.append(sim_text1)
            if(sim_text2):
                sim_text.append(sim_text2)
            if(sim_text3):
                sim_text.append(sim_text3)
            if(sim_text4):
                sim_text.append(sim_text4)
            if(sim_text5):
                sim_text.append(sim_text5)

            # 新建对象，传入参数
            self.bwThread = BigWorkThread(text1, sim_text)
            # 连接子进程的信号和槽函数
            self.bwThread.finishSignal.connect(self.BigWorkEnd)
            # 开始执行 run() 函数里的内容
            self.bwThread.start()


    def BigWorkEnd(self, result):

        # 使用传回的返回值
        if result[0] == "@#^%$&^%$*^error发生错误#@%^%*%&%*&" and len(result)==1:
            QMessageBox.critical(self, "error", "程序发送严重错误,请重试并检查网络连接",  QMessageBox.Yes)
        else:
            for result1 in result:
                mean_str = result1[0]
                str = result1[1]
                self.add_line(mean_str, str)
            # self.tableWidget.sortItems(0,AscEndingOrder)
        # 恢复按钮
        self.tableWidget.resizeRowsToContents()

        self.tableWidget.setSortingEnabled(True)

        self.fanyiButton.setDisabled(False)
        self.label_8.setText("")







if __name__ == '__main__':

    app = QApplication(sys.argv)
    dlg = MainWindow()
    dlg.show()
    sys.exit(app.exec_())
