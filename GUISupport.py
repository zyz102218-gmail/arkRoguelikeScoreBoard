# -*- coding: UTF-8 -*-
from PyQt5.QtCore import QUrl, pyqtSlot, QObject, pyqtSignal, QFileInfo, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QWidget

from mainwindow import Ui_MainWindow

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.setFixedSize(self.width(), self.height())
        self.IsFromPyQt = False
        