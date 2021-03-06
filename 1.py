# coding=utf-8
__author__ = 'a359680405'

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

global sec
sec=0

class WorkThread(QThread):
    trigger = pyqtSignal()
    def __int__(self):
        super(WorkThread,self).__init__()

    def run(self):
        for i in range(5):
            pass
        self.trigger.emit()         #循环完毕后发出信号

def countTime():
    global  sec
    sec+=1
    lcdNumber.display(sec)          #LED显示数字+1

def work():
    timer.start(1000)               #计时器每秒计数
    workThread.start()              #计时开始
    workThread.trigger.connect(timeStop)   #当获得循环完毕的信号时，停止计数

def timeStop():
    timer.stop()
    print("运行结束用时",lcdNumber.value())
    global sec
    sec=0

app=QApplication([])
top=QWidget()
layout=QVBoxLayout(top)             #垂直布局类QVBoxLayout；
lcdNumber=QLCDNumber()              #加个显示屏
layout.addWidget(lcdNumber)
button=QPushButton("测试")
layout.addWidget(button)

timer=QTimer()
workThread=WorkThread()

button.clicked.connect(work)
timer.timeout.connect(countTime)      #每次计时结束，触发setTime

top.show()
app.exec()