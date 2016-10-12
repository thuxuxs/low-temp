# # # # import this
# # # # print 'changed something'
# # # # print 'hello'
# # # # print 'hello world'
# # # # print 1+1
# # # #
# # # # print 'from sublime text'
# # # # print 'clear'
# # # # print 'this is awesome'
# # # # print 'the gun shot effect may be shability'
# # #
# # # #!/usr/bin/env python
# # # # Copyright (c) 2008 Qtrac Ltd. All rights reserved.
# # # # This program or module is free software: you can redistribute it and/or
# # # # modify it under the terms of the GNU General Public License as published
# # # # by the Free Software Foundation, either version 2 of the License, or
# # # # version 3 of the License, or (at your option) any later version. It is
# # # # provided for educational purposes and is distributed in the hope that
# # # # it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# # # # warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# # # # the GNU General Public License for more details.
# # #
# # # from __future__ import division
# # # from __future__ import print_function
# # # from __future__ import unicode_literals
# # # from future_builtins import *
# # #
# # # import sys
# # # from math import *
# # # from PyQt5.QtCore import *
# # # from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QTextBrowser,
# # #         QVBoxLayout)
# # #
# # #
# # # class Form(QDialog):
# # #
# # #
# # #     def __init__(self, parent=None):
# # #         super(Form, self).__init__(parent)
# # #         self.browser = QTextBrowser()
# # #         self.lineedit = QLineEdit("Type an expression and press Enter")
# # #         self.lineedit.selectAll()
# # #         layout = QVBoxLayout()
# # #         layout.addWidget(self.browser)
# # #         layout.addWidget(self.lineedit)
# # #         self.setLayout(layout)
# # #         self.lineedit.setFocus()
# # #         self.lineedit.returnPressed.connect(self.updateUi)
# # #         self.setWindowTitle("Calculate")
# # #
# # #
# # #     def updateUi(self):
# # #         try:
# # #             text = unicode(self.lineedit.text())
# # #             self.browser.append("{0} = <b>{1}</b>".format(text,
# # #                                 eval(text)))
# # #         except:
# # #             self.browser.append("<font color=red>{0} is invalid!</font>"
# # #                                 .format(text))
# # #
# # #
# # # app = QApplication(sys.argv)
# # # form = Form()
# # # form.show()
# # # app.exec_()
# #
# # # coding=utf-8
# # __author__ = 'a359680405'
# #
# # from PyQt5.QtCore import *
# # from PyQt5.QtGui import *
# # from PyQt5.QtWidgets import *
# #
# # global sec
# # sec = 0
# #
# #
# # def setTime():
# #     global sec
# #     sec += 1
# #     lcdNumber.display(sec)
# #
# #
# # def work():
# #     timer.start(1000)
# #     for i in range(2000000000):
# #         pass
# #     timer.stop()
# #
# #
# # app = QApplication([])
# # top = QWidget()
# # layout = QVBoxLayout(top)
# # lcdNumber = QLCDNumber()
# # layout.addWidget(lcdNumber)
# # button = QPushButton('test')
# # layout.addWidget(button)
# #
# # timer = QTimer()
# # timer.timeout.connect(setTime)
# # button.clicked.connect(work)
# #
# # top.show()
# # app.exec_()
#
#
# #!/usr/bin/env python
#
# # embedding_in_qt5.py --- Simple Qt5 application embedding matplotlib canvases
# #
# # Copyright (C) 2005 Florent Rougon
# #               2006 Darren Dale
# #               2015 Jens H Nielsen
# #
# # This file is an example program for matplotlib. It may be used and
# # modified with no restriction; raw copies as well as modified versions
# # may be distributed without limitation.
#
# from __future__ import unicode_literals
# import sys
# import os
# import random
# import matplotlib
# # Make sure that we are using QT5
# matplotlib.use('Qt5Agg')
# from PyQt5 import QtCore, QtWidgets
#
# from numpy import arange, sin, pi
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
#
# progname = os.path.basename(sys.argv[0])
# progversion = "0.1"
#
#
# class MyMplCanvas(FigureCanvas):
#     """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
#
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         # We want the axes cleared every time plot() is called
#         self.axes.hold(False)
#
#         self.compute_initial_figure()
#
#         #
#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)
#
#         FigureCanvas.setSizePolicy(self,
#                                    QtWidgets.QSizePolicy.Expanding,
#                                    QtWidgets.QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#
#     def compute_initial_figure(self):
#         pass
#
#
# class MyStaticMplCanvas(MyMplCanvas):
#     """Simple canvas with a sine plot."""
#
#     def compute_initial_figure(self):
#         t = arange(0.0, 3.0, 0.01)
#         s = sin(2*pi*t)
#         self.axes.plot(t, s)
#
#
# class MyDynamicMplCanvas(MyMplCanvas):
#     """A canvas that updates itself every second with a new plot."""
#
#     def __init__(self, *args, **kwargs):
#         MyMplCanvas.__init__(self, *args, **kwargs)
#         timer = QtCore.QTimer(self)
#         timer.timeout.connect(self.update_figure)
#         timer.start(1000)
#
#     def compute_initial_figure(self):
#         self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
#
#     def update_figure(self):
#         # Build a list of 4 random integers between 0 and 10 (both inclusive)
#         l = [random.randint(0, 10) for i in range(4)]
#
#         self.axes.plot([0, 1, 2, 3], l, 'r')
#         self.draw()
#
#
# class ApplicationWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         QtWidgets.QMainWindow.__init__(self)
#         self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#         self.setWindowTitle("application main window")
#
#         self.file_menu = QtWidgets.QMenu('&File', self)
#         self.file_menu.addAction('&Quit', self.fileQuit,
#                                  QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
#         self.menuBar().addMenu(self.file_menu)
#
#         self.help_menu = QtWidgets.QMenu('&Help', self)
#         self.menuBar().addSeparator()
#         self.menuBar().addMenu(self.help_menu)
#
#         self.help_menu.addAction('&About', self.about)
#
#         self.main_widget = QtWidgets.QWidget(self)
#
#         l = QtWidgets.QVBoxLayout(self.main_widget)
#         sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
#         dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
#         l.addWidget(sc)
#         l.addWidget(dc)
#
#         self.main_widget.setFocus()
#         self.setCentralWidget(self.main_widget)
#
#         self.statusBar().showMessage("All hail matplotlib!", 2000)
#
#     def fileQuit(self):
#         self.close()
#
#     def closeEvent(self, ce):
#         self.fileQuit()
#
#     def about(self):
#         QtWidgets.QMessageBox.about(self, "About",
#                                     """embedding_in_qt5.py example
# Copyright 2005 Florent Rougon, 2006 Darren Dale, 2015 Jens H Nielsen
#
# This program is a simple example of a Qt5 application embedding matplotlib
# canvases.
#
# It may be used and modified with no restriction; raw copies as well as
# modified versions may be distributed without limitation.
#
# This is modified from the embedding in qt4 example to show the difference
# between qt4 and qt5"""
#                                 )
#
#
# qApp = QtWidgets.QApplication(sys.argv)
#
# aw = ApplicationWindow()
# aw.setWindowTitle("%s" % progname)
# aw.show()
# sys.exit(qApp.exec_())
# #qApp.exec_()

import sys
import os
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.Qt import *
from PyQt5.QtCore import *
import functools
import numpy as np
import random as rd
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import time
import threading



def setCustomSize(x, width, height):
    sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(x.sizePolicy().hasHeightForWidth())
    x.setSizePolicy(sizePolicy)
    x.setMinimumSize(QtCore.QSize(width, height))
    x.setMaximumSize(QtCore.QSize(width, height))

''''''

class CustomMainWindow(QMainWindow):

    def __init__(self):

        super(CustomMainWindow, self).__init__()

        # Define the geometry of the main window
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("my first window")

        # Create FRAME_A
        self.FRAME_A = QFrame(self)
        self.FRAME_A.setStyleSheet("QWidget { background-color: %s }" % QColor(210,210,235,255).name())
        self.LAYOUT_A = QGridLayout()
        self.FRAME_A.setLayout(self.LAYOUT_A)
        self.setCentralWidget(self.FRAME_A)

        # Place the zoom button
        self.zoomBtn = QPushButton(text = 'zoom')
        setCustomSize(self.zoomBtn, 100, 50)
        self.zoomBtn.clicked.connect(self.zoomBtnAction)
        self.LAYOUT_A.addWidget(self.zoomBtn, *(0,0))

        # Place the matplotlib figure
        self.myFig = CustomFigCanvas()
        self.LAYOUT_A.addWidget(self.myFig, *(0,1))

        # Add the callbackfunc to ..
        myDataLoop = threading.Thread(name = 'myDataLoop', target = dataSendLoop, daemon = True, args = (self.addData_callbackFunc,))
        myDataLoop.start()

        self.show()

    ''''''


    def zoomBtnAction(self):
        print("zoom in")
        self.myFig.zoomIn(5)

    ''''''

    def addData_callbackFunc(self, value):
        # print("Add data: " + str(value))
        self.myFig.addData(value)



''' End Class '''


class CustomFigCanvas(FigureCanvas, TimedAnimation):

    def __init__(self):

        self.addedData = []
        print(matplotlib.__version__)

        # The data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        a = []
        b = []
        a.append(2.0)
        a.append(4.0)
        a.append(2.0)
        b.append(4.0)
        b.append(3.0)
        b.append(4.0)
        self.y = (self.n * 0.0) + 50

        # The window
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)


        # self.ax1 settings
        self.ax1.set_xlabel('time')
        self.ax1.set_ylabel('raw data')
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='red', linewidth=2)
        self.line1_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(0, 100)


        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        lines = [self.line1, self.line1_tail, self.line1_head]
        for l in lines:
            l.set_data([], [])

    def addData(self, value):
        self.addedData.append(value)

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom += value
        top -= value
        self.ax1.set_ylim(bottom,top)
        self.draw()


    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            print(str(self.abc))
            TimedAnimation._stop(self)
            pass

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.addedData) > 0):
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedData[0]
            del(self.addedData[0])


        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]



''' End Class '''


# You need to setup a signal slot mechanism, to
# send data to your GUI in a thread-safe way.
# Believe me, if you don't do this right, things
# go very very wrong..
class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(float)

''' End Class '''



def dataSendLoop(addData_callbackFunc):
    # Setup the signal-slot mechanism.
    mySrc = Communicate()
    mySrc.data_signal.connect(addData_callbackFunc)

    # Simulate some data
    n = np.linspace(0, 499, 500)
    y = 50 + 25*(np.sin(n / 8.3)) + 10*(np.sin(n / 7.5)) - 5*(np.sin(n / 1.5))
    i = 0

    while(True):
        if(i > 499):
            i = 0
        time.sleep(0.1)
        mySrc.data_signal.emit(y[i]) # <- Here you emit a signal!
        i += 1
    ###
###




if __name__== '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Plastique'))
    myGUI = CustomMainWindow()


    sys.exit(app.exec_())

''''''