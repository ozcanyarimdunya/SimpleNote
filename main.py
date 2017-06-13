import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu, qApp, QAction

from form import Ui_MainWindow
import resources


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__(self)
        self.setupUi(self)

        self.logo = QIcon(':logo/icons/logo.jpg')
        self.red = QIcon(':red/icons/red.png')
        self.blue = QIcon(':blue/icons/blue.png')
        self.green = QIcon(':green/icons/green.png')
        self.yellow = QIcon(':yellow/icons/yellow.png')
        self.gray = QIcon(':gray/icons/gray.png')
        self.setUpTrayIcon()

    def setUpTrayIcon(self):
        self.icon = QSystemTrayIcon()
        self.icon.setIcon(self.logo)  # :prefix/path
        self.menu = QMenu()

        actions = [(self.red, "red"), (self.blue, "blue"), (self.green, "green"), (self.yellow, "yellow")]
        self.create_actions_and_add_menu(actions, self.menu)

        self.menu.addAction(self.gray, 'quit', qApp.quit)
        self.icon.setContextMenu(self.menu)
        self.icon.show()

        for actions in self.menu.actions():
            print(actions.text(), actions.text())

    def create_actions_and_add_menu(self, actions, menu):
        for action in actions:
            name = QAction(action[0], action[1], self)
            menu.addAction(name)
            self.create_sub_menu(name)

    def create_sub_menu(self, action):
        new_menu = QMenu()
        add_new_action = QAction("+++", self)
        new_menu.addAction(add_new_action)
        action.setMenu(new_menu)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Form()
    sys.exit(app.exec_())
