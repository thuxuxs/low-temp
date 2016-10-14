import sys
import numpy as np
import pylab as pl
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
import time
import datetime
from scipy.optimize import leastsq

global mode
try:
    import visa
except:
    mode = 'ont_has_visa'
else:
    mode = 'has_visa'

class AFG_MainWindow(QWidget):
    def __init__(self,parent=None,GPIB=None):
        QWidget.__init__(self,parent)
        self.setWindowTitle('AFG')
        self.GPIB=GPIB
        self.resize(1000,500)
        self.btn=QPushButton('abc',self)

    def keyPressEvent(self,QKeyEvent):
        event_value=QKeyEvent.key()
        if event_value==Qt.Key_Q:
            sys.exit()

if __name__=='__main__':
    AFG_GUI=QApplication(sys.argv)
    mainwindow=AFG_MainWindow(GPIB='AFG_GPIB')
    mainwindow.show()
    sys.exit(AFG_GUI.exec_())
