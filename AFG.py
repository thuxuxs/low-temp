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
        self.create_ui()

    def create_ui(self):
        self.create_widget_plot()
        self.create_input_widget()

    def create_widget_plot(self):
        self.fig = Figure(figsize=(6, 6), dpi=80)
        self.fig.patch.set_color('w')
        self.ax = self.fig.add_axes([0, 0, 1, 1], axisbg=(0.6, 0.7, 0.8))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.show()

    def create_input_widget(self):
        self.input_widget = QWidget(self)
        self.input_widget.move(500, 0)
        self.input_widget_layout = QGridLayout(self)

        self.freq_lab = QLabel('Freq', self.input_widget)
        self.high_lab = QLabel('High', self.input_widget)
        self.low_lab = QLabel('Low', self.input_widget)
        self.off_lab = QLabel('Off', self.input_widget)

        self.freq_text = QLineEdit('60', self.input_widget)
        self.freq_text.setFixedWidth(100)
        self.high_text = QLineEdit('1', self.input_widget)
        self.high_text.setFixedWidth(100)
        self.low_text = QLineEdit('-1', self.input_widget)
        self.low_text.setFixedWidth(100)
        self.off_text = QLineEdit('0', self.input_widget)
        self.off_text.setFixedWidth(100)

        self.freq_cb = QComboBox(self.input_widget)
        self.freq_cb.addItems(['Hz', 'KHz', 'MHz'])
        self.high_cb = QComboBox(self.input_widget)
        self.high_cb.addItems(['V', 'mV'])
        self.low_cb = QComboBox(self.input_widget)
        self.low_cb.addItems(['V', 'mV'])
        self.off_cb = QComboBox(self.input_widget)
        self.off_cb.addItems(['V', 'mV'])

        self.shape_cb = QComboBox(self.input_widget)
        self.shape_cb.addItems(['RAMP', 'SIN', 'SQU'])

        self.start_btn = QPushButton('Start', self.input_widget)

        self.input_widget_layout.addWidget(self.freq_lab, 0, 0)
        self.input_widget_layout.addWidget(self.high_lab, 1, 0)
        self.input_widget_layout.addWidget(self.low_lab, 2, 0)
        self.input_widget_layout.addWidget(self.off_lab, 3, 0)
        self.input_widget_layout.addWidget(self.freq_text, 0, 1)
        self.input_widget_layout.addWidget(self.high_text, 1, 1)
        self.input_widget_layout.addWidget(self.low_text, 2, 1)
        self.input_widget_layout.addWidget(self.off_text, 3, 1)
        self.input_widget_layout.addWidget(self.freq_cb, 0, 2)
        self.input_widget_layout.addWidget(self.high_cb, 1, 2)
        self.input_widget_layout.addWidget(self.low_cb, 2, 2)
        self.input_widget_layout.addWidget(self.off_cb, 3, 2)
        self.input_widget_layout.addWidget(self.shape_cb, 4, 0, 4, 3)
        self.input_widget_layout.addWidget(self.start_btn, 10, 0, 10, 3)

        self.input_widget.setLayout(self.input_widget_layout)
        self.setStyleSheet(
            "QLabel,QLineEdit,QComboBox,QPushButton{font-size:24px;font-family:Roman times;font-weight:bold;}")

    def keyPressEvent(self,QKeyEvent):
        event_value=QKeyEvent.key()
        if event_value==Qt.Key_Q:
            sys.exit()
        if event_value in [Qt.Key_Return, Qt.Key_Enter]:
            print 'hello'

if __name__=='__main__':
    AFG_GUI=QApplication(sys.argv)
    mainwindow=AFG_MainWindow(GPIB='AFG_GPIB')
    mainwindow.show()
    sys.exit(AFG_GUI.exec_())
