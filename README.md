### resources
    https://pythonspot.com/en/pyqt5-window/


### mygui.py
------
    # -*- coding: utf-8 -*-

    # Form implementation generated from reading ui file '..\..\Desktop\New folder\first.ui'
    #
    # Created by: PyQt5 UI code generator 5.8.2
    #
    # WARNING! All changes made in this file will be lost!

    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QAction
    from res import resources


    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(270, 150)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(31, 20, 210, 30))
            self.pushButton = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton.setGeometry(QtCore.QRect(30, 60, 210, 30))
            self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton2.setGeometry(QtCore.QRect(30, 90, 210, 30))
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 254, 21))
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def setupTrayIcon(self):
            self.trayIcon = QSystemTrayIcon()
            self.trayIcon.setIcon(QIcon(':huawei/huawei.png'))
            self.menu = QMenu()
            self.quit = QAction("Quit")
            self.quit.setIcon(QIcon(':quit/quit.png'))
            self.menu.addAction(self.quit)
            self.trayIcon.setContextMenu(self.menu)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.label.setText(_translate("MainWindow", "Label"))
            self.pushButton.setText(_translate("MainWindow", "First"))
            self.pushButton2.setText(_translate("MainWindow", "Second"))

### main.py
------
      import sys
      from datetime import datetime
      from time import sleep

      from PyQt5.QtCore import QThread, pyqtSignal
      from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QApplication

      from info import GetInfo
      from my_gui import Ui_MainWindow
      from res import resources


      class Window(QMainWindow, Ui_MainWindow):
          def __init__(self, parent=None):
              QMainWindow.__init__(self, parent=parent)
              self.thread = ChangeNumThread()
              self.setupUi(self)
              self.setupTrayIcon()

              self.pushButton.clicked.connect(lambda: self.btns_clicked())
              self.pushButton2.clicked.connect(lambda: self.btns_clicked())

              self.trayIcon.show()
              self.trayIcon.activated.connect(lambda reason: self.icon_clicked(reason))
              self.quit.triggered.connect(lambda: self.close())

          def icon_clicked(self, reason):
              if reason == QSystemTrayIcon.Trigger:  # QSystemTrayIcon.DoubleClick
                  if self.isHidden(): self.show()
                  if not self.isActiveWindow(): self.activateWindow()

          def btns_clicked(self):
              if not self.thread.isRunning():
                  self.thread.my_signal.connect(self.updateMessage)
              self.thread.start()

              self.trayIcon.messageClicked.connect(lambda: self.activateWindow())

          def updateMessage(self, time, category, text):
              self.trayIcon.showMessage("(" + category + ")" + text, time)

          def message_clicked(self, val):
              self.label.setText(val)
              self.activateWindow()


      class ChangeNumThread(QThread):
          my_signal = pyqtSignal(str, str, str)  # must be define here

          def __init__(self):
              super().__init__()

          def run(self):
              while True:
                  try:
                      time = str(datetime.now())
                      category = "other"
                      text = ""
                      info = GetInfo()
                      if info.get_info() is not None:
                          time, category, text = info.get_info()
                      self.my_signal.emit(time, category, text)
                  except Exception as e:
                      print(e)
                  sleep(1)


      if __name__ == '__main__':
          app = QApplication(sys.argv)
          window = Window()
          sys.exit(app.exec_())
