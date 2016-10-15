import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *

from MDO import MDO_MainWindow
from AFG import AFG_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(1000,520)
        self.menubar=self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.create_instruments()
        self.create_menu()

    def create_instruments(self):
        self.MDO = MDO_MainWindow(self, GPIB='USB0::0x0699::0x0454::C021335::INSTR')
        self.AFG=AFG_MainWindow(self)
        self.MDO.move(0,20)
        self.AFG.move(0,20)
        self.MDO.setVisible(False)

    def create_menu(self):
        self.AFG_Menu=self.menubar.addMenu('&AFG')
        self.MDO_Menu=self.menubar.addMenu('&MDO')
        self.AFG_Action=QAction('Open AFG',self)
        self.MDO_Action=QAction('Open MDO',self)
        self.AFG_Action.setShortcut('Ctrl+1')
        self.MDO_Action.setShortcut('Ctrl+2')
        self.AFG_Menu.addAction(self.AFG_Action)
        self.MDO_Menu.addAction(self.MDO_Action)
        self.AFG_Action.triggered.connect(self.show_AFG)
        self.MDO_Action.triggered.connect(self.show_MDO)

    def show_AFG(self):
        self.AFG.setVisible(True)
        self.MDO.setVisible(False)
        self.resize(800, 520)

    def show_MDO(self):
        self.MDO.setVisible(True)
        self.AFG.setVisible(False)
        self.resize(1000, 520)

if __name__=='__main__':
    MAIN_GUI=QApplication(sys.argv)
    mainwindow=MainWindow()
    mainwindow.show()
    sys.exit(MAIN_GUI.exec_())
