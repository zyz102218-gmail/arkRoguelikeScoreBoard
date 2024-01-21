# -*- coding: UTF-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
import GUISupport

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = GUISupport.MainWindow()
    ui.show()
    sys.exit(app.exec())

