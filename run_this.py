import time
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QTreeWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication, QIcon
from PyQt5.QtCore import QRect, Qt, QTimer, pyqtSignal
import cv2
from Annotate_Console import *
from collections import defaultdict
import json, os
import datetime, time

class MyMainWinow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWinow,self).__init__(parent)
        self.setupUi(self)

        self.counter = 0
        self.m4_timer = QTimer()  # 初始化定时器
        self.m4_timer.timeout.connect(self.m4_ImagePlay)  # 创建 定时器信号槽
        self.m4_OpenVideo_Btn.clicked.connect(self.m4_OpenVideo)
        self.m4_CloseVideo_Btn.clicked.connect(self.m4_CloseVideo)
        self.m4_TakePhoto_Btn.clicked.connect(self.m4_TakePhoto)
        self.m4_SetSavePath_Btn.clicked.connect(self.m4_SetSaveDir)

    def m4_SetSaveDir(self):
        self.SavedefaultPath = QFileDialog.getExistingDirectory(self, '设置图像保存目录！', './')
        self.m4_LabelDir.setText(self.SavedefaultPath)
        self.m4_OpenVideo_Btn.setEnabled(True)
        self.m4_CloseVideo_Btn.setEnabled(True)
        self.m4_TakePhoto_Btn.setEnabled(True)


    def m4_OpenVideo(self):
        if self.m4_timer.isActive() == False:  # 定时器m4_timer没有启动
            self.m4_TakePhoto_Btn.setEnabled(True)
            self.capture = cv2.VideoCapture(1)  # 相机初始化
            self.m4_timer.start(30)  # 启动定时器m4_timer
        else:
            reply = QMessageBox.information(self, '提示', '相机已打开，无需再打开!', QMessageBox.Ok, QMessageBox.Ok)

    def m4_CloseVideo(self):
        if self.m4_timer.isActive() == True:  # 定时器m4_timer没有启动
            self.m4_timer.stop()  # 启动定时器m4_timer
            self.capture.release()
            self.m4_ShowImage.setPixmap(QtGui.QPixmap(":/pic/YY.jpg"))
            self.m4_TakePhoto_Btn.setEnabled(False)
        else:
            reply = QMessageBox.information(self, '提示', '相机已关闭，无需再关闭!', QMessageBox.Ok, QMessageBox.Ok)

    def m4_ImagePlay(self):
        ret, self.image = self.capture.read()
        frame = self.image.copy()
        self.m4_AnnImageShow(frame)
    # 标注图像显示
    def m4_AnnImageShow(self, frame):
        frame = frame.copy()
        height, width, bytesPerComponent = frame.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
        QImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.m4_ShowImage.setPixmap(pixmap)

    def m4_TakePhoto(self):
        nameTime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        cv2.imwrite(self.SavedefaultPath + '/' + str(self.counter) + '_'  + nameTime + '.png', self.image)
        self.m4_SavePath.setText(self.SavedefaultPath + '/' + str(self.counter) + '_'  + nameTime + '.png')
        self.counter += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWinow()
    myWin.show()
    sys.exit(app.exec())
