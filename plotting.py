#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 16:01:52 2019

@author: Sarah
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 10:20:29 2019

@author: Sarah
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication, QPushButton, QDesktopWidget,
                            QLabel, QFileDialog, QWidget, QGridLayout, QMenu, QSizePolicy, QMessageBox, QWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt

import json
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import math
import numpy as np
import csv

CURRENT_VERSION = 0.1

class Example(QMainWindow):
    '''def LoadJson(datafilename):
        with open(datafilename, 'r') as datajson:
            data = json.load(datajson)
    
        return data   '''

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Multiple Axis GUI')

        self.center()

        self.setWindowIcon(QIcon('Icon.png'))

        #inits
        self.openDirectoryDialog = ""
        self.data = np.empty(shape=(1,2), dtype=np.float)
        ##self.idata = np.empty(shape=(1,2), dtype=np.float)

        #Exit on menubar
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit applicatiion')
        exitAct.triggered.connect(qApp.quit)

        #Open on menubar
        openAct = QAction('&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open Directory')
        openAct.triggered.connect(self.openFile)

        #menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(openAct)

        #Central
        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget)

        #Grid
        grid = QGridLayout(centralwidget)
        self.setLayout(grid)

        #Plot
        plotCan = PlotCanvas(self, width=5, height=4)
        grid.addWidget(plotCan , 0,1)

        #button
        btn = QPushButton("Load Data", centralwidget)
        btn.resize(btn.sizeHint())
        grid.addWidget(btn, 0,0)
        btn.clicked.connect(lambda: plotCan.plot(self.data, self.idata, self.palpha))
       # btn.clicked.connect(plotCan .plot(self.data))

        #savebutton
        btn2 = QPushButton("save as .png", centralwidget)
        btn.resize(btn.sizeHint())
        grid.addWidget(btn2, 1,0)
        btn2.clicked.connect(plotCan.savepng)
        
        
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openFile(self):        
        self.datafiles = QFileDialog.getOpenFileNames(self, "Get Dir Path")[0]
        #list of list
        for file in self.datafiles:
            if str(file).endswith('E.CSV'):
                with open(file, 'r') as datacsv:
                    reader=csv.reader(datacsv, delimiter = ',')
                    self.data = [row for row in reader]
                ifilename = str(file).split('.')[0]+('I.CSV')
                with open(ifilename, 'r') as datacsv:
                    reader=csv.reader(datacsv, delimiter = ',')
                    self.idata = [row for row in reader]
                    print(self.idata)
                    
            colorindex= {}
            colorindex['_LINVLIN_']=1
            colorindex['_LOGVLIN_']=1
            colorindex['_LOGVLOG_']=2
            colorindex['_LINVLOG_']=1        
            alphamin = 0.1
    
            for key in colorindex:
                if key in str(file):
                    self.palpha = alphamin+(1-alphamin)*0.5**colorindex[key]
      

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig = Figure()
        self.pltCanvas = FigureCanvas(self.fig)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data='', idata='', palpha=''): 
        print('idata \n' + str(idata))
        self.sfig1 = self.figure.subplots()
        self.sfig2 = self.sfig1.twinx()
        self.sfig1.set_xlabel('Freq (Hz)')
        self.sfig1.set_ylabel(chr(949)+chr(8242), color = 'b')
        self.sfig1.set_xscale('log')
        self.sfig1.tick_params(axis='y', labelcolor='b')
        self.sfig2.set_ylabel('tan '+chr(948), color = 'g', rotation=-90, labelpad=10)
        self.sfig2.tick_params(axis='y', labelcolor='g')
        self.sfig1.set_xlim(1E7,1E9)
        self.sfig1.set_ylim(2.2,2.4)
        self.sfig2.set_ylim(-0.001,0.005)
        self.sfig1.set_title('PyQt Matplotlib Example')

        
        freqlist = [float(line[0]) for line in data[3:]]
        elist = [float(line[1]) for line in data[3:]]
        print('e')
        print(elist)
        eilist = [float(line[1]) for line in idata[3:]]
        print('ei')
        print(eilist)
        tandlist = [math.tan(eilist[n]/elist[n]) for n in range(0,len(elist))]
        
        self.sfig1.plot(freqlist, elist, color = 'b', alpha = palpha)
        self.sfig2.plot(freqlist, tandlist, color = 'g', alpha = palpha)
        
        self.draw()
        
        
    def savepng(self):
        file_name = input('Enter a filename: ') or 'Figure'+ 'Summary' +'tand.png'
        self.figure.savefig(file_name, dpi=600)
        print('done')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Example()
    sys.exit(app.exec_())