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
import visa

from scipy.optimize import leastsq


class MDO_MainWindow(QWidget):
    def __init__(self, parent=None, GPIB=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('MDO')
        self.GPIB = GPIB
        self.resize(1000, 500)
        self.create_ui()

    def get_init_state(self):
        self.inst = visa.ResourceManager().open_resource(self.GPIB)
        self.ch_state = [0, 0, 0, 0]
        for ch in range(4):
            self.ch_state[ch] = int(str(self.inst.ask('select:ch' + str(ch + 1) + '?')).split(' ')[1])
        self.ch_color = ['y', 'b', 'r', 'g']

    def create_ui(self):
        self.create_widget_plot()
        self.create_widget_control()
        self.create_fit_result()
        self.create_fit_plot()

    def create_widget_plot(self):
        self.widget_plot = QWidget(self)
        self.vbox_plot = QVBoxLayout()
        self.hbox_plot = QHBoxLayout()

        self.fig_plot = plt.figure(figsize=(9, 6), dpi=65)
        self.fig_plot.patch.set_color('w')
        self.ax_plot = self.fig_plot.add_axes([0, 0, 1, 1], axisbg=(0.6, 0.7, 0.8))
        # self.ax_plot.hold(False)
        self.fit_line, = self.ax_plot.plot([], [])

        self.canvas_plot = FigureCanvas(self.fig_plot)
        self.canvas_plot.setParent(self.widget_plot)
        self.canvas_plot.show()
        self.mpl_toolbar = NavigationToolbar(self.canvas_plot, self.widget_plot)
        self.mpl_toolbar.setStyleSheet("border:none;background-color:#efefef")

        self.ch1_label = QLabel('CH1')
        self.ch2_label = QLabel('CH2')
        self.ch3_label = QLabel('CH3')
        self.ch4_label = QLabel('CH4')
        self.ch_label_group = [self.ch1_label, self.ch2_label, self.ch3_label, self.ch4_label]
        for i in self.ch_label_group:
            i.setStyleSheet("color:rgb(100,100,100,250);font-size:15px;font-weight:bold;border:2px solid red;")

        self.hbox_plot.addWidget(self.ch1_label)
        self.hbox_plot.addStretch(1)
        self.hbox_plot.addWidget(self.ch2_label)
        self.hbox_plot.addStretch(1)
        self.hbox_plot.addWidget(self.ch3_label)
        self.hbox_plot.addStretch(1)
        self.hbox_plot.addWidget(self.ch4_label)
        self.vbox_plot.addWidget(self.canvas_plot)
        self.vbox_plot.addWidget(self.mpl_toolbar)
        self.vbox_plot.addLayout(self.hbox_plot)
        self.widget_plot.setLayout(self.vbox_plot)

    def create_widget_control(self):
        self.widget_control = QWidget(self)
        self.widget_control.resize(200, 180)
        self.widget_control.move(640, 10)
        # self.widget_control.setStyleSheet("background-color:white")
        self.ch1_cb = QCheckBox(self.widget_control)
        self.ch2_cb = QCheckBox(self.widget_control)
        self.ch3_cb = QCheckBox(self.widget_control)
        self.ch4_cb = QCheckBox(self.widget_control)
        self.ch_cb_grounp = [self.ch1_cb, self.ch2_cb, self.ch3_cb, self.ch4_cb]
        for i in range(4):
            self.ch_cb_grounp[i].move(10 + i * 25, 5)

        self.run_stop = QPushButton('STOP', self.widget_control)
        self.run_stop.move(10, 60)
        self.run_stop.resize(50, 24)
        self.fit_mdo = QPushButton('FIT', self.widget_control)
        self.fit_mdo.move(80, 60)
        self.fit_mdo.resize(50, 24)
        self.save = QPushButton('SAVE', self.widget_control)
        self.save.move(80, 116)
        self.save.resize(50, 24)
        self.h_plus = QPushButton('+', self.widget_control)
        self.h_minus = QPushButton('-', self.widget_control)
        self.h_plus.move(10, 120)
        self.h_plus.resize(20, 20)
        self.h_minus.move(40, 120)
        self.h_minus.resize(20, 20)
        self.v_plus = QPushButton('+', self.widget_control)
        self.v_minus = QPushButton('-', self.widget_control)
        self.v_plus.resize(20, 20)
        self.v_minus.resize(20, 20)
        self.v_plus.move(140, 60)
        self.v_minus.move(140, 90)
        self.h_slider = QSlider(self.widget_control)
        self.v_slider = QSlider(self.widget_control)
        self.h_slider.setOrientation(Qt.Horizontal)
        self.h_slider.move(10, 150)
        self.v_slider.move(170, 60)
        self.h_slider.resize(120, 20)
        self.v_slider.resize(20, 110)
        self.ch_which = QComboBox(self.widget_control)
        self.ch_which.move(140, 30)
        self.ch_which.resize(50, 24)

    def create_fit_result(self):
        self.fit_result_te = QTextEdit(self)
        self.fit_result_te.setText('Q:7e8')
        self.fit_result_te.move(850, 10)
        self.fit_result_te.resize(115, 180)

    def create_fit_plot(self):
        self.fig_fit = plt.figure(figsize=(5, 4), dpi=65)
        self.fig_fit.patch.set_color('w')
        self.ax_fit = self.fig_fit.add_axes([0, 0, 1, 1], axisbg=(0.6, 0.7, 0.8))

        self.ax_fit.plot(pl.linspace(0, 6, 100), pl.sin(pl.linspace(0, 6, 100)))

        self.canvas_fit = FigureCanvas(self.fig_fit)
        self.canvas_fit.setParent(self)
        self.canvas_fit.move(640, 200)
        self.canvas_fit.show()

        self.file_type = QComboBox(self)
        self.file_type.addItem('1')
        self.file_type.addItem('2')
        self.file_type.addItem('3')
        self.file_type.resize(30, 24)
        self.file_type.move(640, 465)
        self.file_fit_file = QPushButton('file', self)
        self.file_fit_file.move(675, 465)
        self.file_fit_file.resize(40, 24)
        self.file_fit_file.clicked.connect(self.select_file_plot)
        self.fit_type1 = QPushButton('Lorentz-1', self)
        self.fit_type1.move(720, 465)
        self.fit_type1.clicked.connect(self.lorentz_1_btn)
        self.fit_type2 = QPushButton('Lorentz-2', self)
        self.fit_type2.move(800, 465)
        self.fit_type2.clicked.connect(self.lorentz_2_btn)
        self.fit_type3 = QPushButton('Lorentz-3', self)
        self.fit_type3.move(880, 465)

    def read_data_from_file(self, file_name, type=1):
        '''
        type 1: for data saved from floor 3;
        type 2: for data saved from floor 2;
        type 3: unknown type, input manually
        '''

        data = pl.genfromtxt(file_name, delimiter=',')
        # print 'the total size of input data are:',len(data),'X',len(data[0])
        if type == 1:
            data = data[20:, :]
        elif type == 2:
            data = data[:, -3:-1]
        else:
            begin_row = input('begin row:')
            begin_column = input('begin column:')
            end_row = raw_input('end row:')
            end_column = raw_input('end column:')
            if end_row == 'end':
                end_row = len(data)
            else:
                end_row = int(end_row)
            if end_column == 'end':
                end_column = len(data[0])
            else:
                end_column = int(end_column)
            data = data[begin_row:end_row, begin_column:end_column]
        return data

    def lorentz_2(self, x, p):
        w0, k0, kex, g, a, = p
        return abs(1 + kex / (-1j * (x - w0) - (k0 + kex) / 2 + g ** 2 / (-1j * (x - w0) - (k0 + kex) / 2))) ** 2 * a

    def lorentz_1(self, x, p):
        w0, k0, kex, a = p
        return ((x - w0) ** 2 + (k0 - kex) ** 2) / ((x - w0) ** 2 + (k0 + kex) ** 2) * a

    def residuals_lorentz_1(self, p, y, x):
        return y - self.lorentz_1(x, p)

    def residuals_lorentz_2(self, p, y, x):
        return y - self.lorentz_2(x, p)

    def to_freq(self, time_domain):
        # time[0]=0
        lamb = 1434
        v = 1.3
        v_scan = 0.0456
        f = 5
        n = 1.37
        c = 3e8
        return 2 * pl.pi * c / (lamb + time_domain * 2 * v_scan * v * f) / n * 1e2

    def handle_x(self, data_x, middle):
        return self.to_freq(data_x - data_x[0]) - self.to_freq(data_x[middle] - data_x[0])

    def lorentz_fit(self, data_x, data_y, type):
        self.lorentz_type = [self.lorentz_1, self.lorentz_2]
        self.residuals_lorentz_type = [self.residuals_lorentz_1, self.residuals_lorentz_2]
        self.para_init = [[0.03, 0.01, 0.01, 0.9], [0.03, 0.01, 0.01, 0.01, 0.9]]
        plsq = leastsq(self.residuals_lorentz_type[type], self.para_init[type],
                       args=(data_y, self.handle_x(data_x, int(len(data_x) / 2))))
        return plsq[0]

    def plot_fit_result(self, type):
        self.ax_fit.clear()
        self.fit_data_begin = self.ax_plot.get_xlim()[0]
        self.fit_data_end = self.ax_plot.get_xlim()[1]
        self.index = []

        for i in range(len(self.x)):
            if self.x[i] > self.fit_data_begin:
                self.index.append(i)
                break

        for i in range(len(self.x)):
            if self.x[i] > self.fit_data_end:
                self.index.append(i)
                break
        if len(self.index) < 2:
            self.index = [0, len(self.x) - 1]
        para = self.lorentz_fit(self.x[self.index[0]:self.index[1]], self.y[self.index[0]:self.index[1]], type)
        self.x_freq = self.handle_x(self.x[self.index[0]:self.index[1]], int((self.index[1] - self.index[0]) / 2))
        self.ax_fit.plot(self.x_freq, self.y[self.index[0]:self.index[1]] / para[-1], '.')
        self.fit_x = pl.linspace(self.x_freq[0], self.x_freq[-1], 1000)
        self.fit_y = self.lorentz_type[type](self.fit_x, para)
        self.ax_fit.plot(self.fit_x, self.fit_y / para[-1], linewidth=3)
        self.canvas_fit.draw()
        print para

    def select_file_plot(self):
        self.selected_file = QFileDialog.getOpenFileName(self, 'Select Data', '.')[0]
        if self.selected_file != '':
            self.data = self.read_data_from_file(self.selected_file, type=int(self.file_type.currentText()))
            self.x = self.data[:, 0]
            self.y = self.data[:, 1]
            self.ax_plot.clear()
            self.ax_plot.plot(self.x, self.y)
            self.ax_plot.set_xlim(min(self.x), max(self.x))
            self.ax_plot.set_ylim(min(self.y), max(self.y))
            self.canvas_plot.draw()

    def lorentz_1_btn(self):

        self.plot_fit_result(0)

    def lorentz_2_btn(self):
        self.plot_fit_result(1)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(200, 200)
        self.main_frame = QWidget()
        hbox = QHBoxLayout()
        self.mdo1 = MDO_MainWindow(self.main_frame)
        self.mdo2 = MDO_MainWindow(self.main_frame)
        hbox.addWidget(self.mdo1)
        hbox.addWidget(self.mdo2)
        self.main_frame.setLayout(hbox)
        self.setCentralWidget(self.main_frame)


MDO_GUI = QApplication(sys.argv)
mainwindow = MDO_MainWindow()
mainwindow.show()

sys.exit(MDO_GUI.exec_())
