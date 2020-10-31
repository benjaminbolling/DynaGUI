# -*- coding: utf-8 -*-
"""
<A Dynamic Graphical User Interface package, which gives users a method to construct temporary, permanent and/or a set of GUI:s for users in a simple and fast manner combined with diagnostics tools with advance 1D and 2D plotting methods.>
    Copyright (C) <2019-2020>  <Benjamin Edward Bolling>  <benjaminbolling@icloud.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# We create here a simple list which contains if an import of a package failed. 0 = no fail, 1 = fail
packagefailure = [0,0,0,0,0] # [ basic, tango, epics, random, finance]
# Try importing required packages. If any of these fails, DynaGUI cannot be initialized
try:
    import os, platform, sys, time, datetime, fnmatch, numexpr, math, json
    import numpy as np
    import pyqtgraph as pg
    from functools import partial
    import matplotlib.pyplot as plt
except:
    packagefailure[0] = 1
try:
    import PyQt5.QtWidgets as QtGui
    import PyQt5.QtGui as QtGui2
    from PyQt5 import QtCore
except:
    try:
        from PyQt4 import QtCore, QtGui
    except:
        packagefailure[0] = 1
if packagefailure[0] == 1:
    # At least one required package import failed, don't try importing the others and send this message to the user in the terminal
    print("Failed to import basic packages, DynaGUI cannot launch.")
    packagefailure = [1,1,1,1,1] # [ basic, tango, epics, random, finance]
elif packagefailure[0] == 0:
    # The requireded packages succeeded importing, try with the ones for the different DynaGUI control libraries
    try: # Tango
        import PyTango as PT
    except:
        print("Failed to import PyTango, Tango control library in DynaGUI is hence disabled")
        packagefailure[1] = 1
    try: # EPICS
        import epics
    except:
        print("Failed to import Epics, EPICS control library in DynaGUI is hence disabled")
        packagefailure[2] = 1
    try: # EPICS
        import requests
    except:
        print("Failed to import Requests, EPICS control library in DynaGUI is hence disabled")
        packagefailure[2] = 1
    try: # Randomizer
        import random
    except:
        print("Failed to import Random, Random control library in DynaGUI is hence disabled")
        packagefailure[3] = 1
    try: # Finance
        from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
    except:
        print("Failed to matplotlib backends package, Finance control library in DynaGUI is hence disabled")
        packagefailure[4] = 1
    try: # Finance
        from pandas.plotting import register_matplotlib_converters
        import pandas_datareader as pdr
    except: # Finance
        print("Failed to import Pandas Finance package, Finance control library in DynaGUI is hence disabled")
        packagefailure[4] = 1

class Dialog(QtGui.QWidget):
    # This is the class in which the DynaGUI window is constructed
    def __init__(self, packagefailure,parent=None):
        super(Dialog, self).__init__(parent)
        QtGui.QDialog.__init__(self)
        # Create the layout
        self.createLayout()
        # Disable control libraries that were unsuccessful during loading
        if packagefailure[0] == 1:
            self.viewdataNV.setEnabled(False)
            self.viewdataNV.setToolTip("Import of required general Python packages failed.")
        else:
            self.viewdataNV.setEnabled(False)
            self.viewdataNV.setToolTip("Not yet ready, is to be developed soon.")
        if packagefailure[1] == 1:
            self.tangoNV.setEnabled(False)
            self.tangoNV.setToolTip("Import of the PyTango Python package failed.")
            self.tangoTF.setEnabled(False)
            self.tangoTF.setToolTip("Import of the PyTango Python package failed.")
            self.tangoAlarms.setEnabled(False)
            self.tangoAlarms.setToolTip("Import of the PyTango Python package failed.")
        if packagefailure[2] == 1:
            self.epicsNV.setEnabled(False)
            self.epicsNV.setToolTip("Import of epics required Python packages (pyepics, requests, json) failed.")
            self.epicsTF.setEnabled(False)
            self.epicsTF.setToolTip("Import of epics required Python packages (pyepics, requests, json) failed.")
            self.epicsAlarms.setEnabled(False)
            self.epicsAlarms.setToolTip("Import of epics required Python packages (pyepics, requests, json) failed.")
        if packagefailure[3] == 1:
            self.randomNV.setEnabled(False)
            self.randomNV.setToolTip("Import of the random Python package failed.")
            self.randomTF.setEnabled(False)
            self.randomTF.setToolTip("Import of the random Python package failed.")
            self.randomAlarms.setEnabled(False)
            self.randomAlarms.setToolTip("Import of the random Python package failed.")
        if packagefailure[4] == 1:
            self.financeNV.setEnabled(False)
            self.financeNV.setToolTip("Import of finance required Python packages (matplotlib backends, pandas, pandas_datareader) failed.")
            self.financeAlarms.setEnabled(False)
            self.financeAlarms.setToolTip("Import of finance required Python packages (matplotlib backends, pandas, pandas_datareader) failed.")
    def createLayout(self):
        # Create the main layout
        self.setWindowTitle("DynaGUI")
        self.dialogs = list()
        self.toplayout = QtGui.QVBoxLayout(self)
        self.toplayout.addStretch()
        self.label = QtGui.QLabel("Select package to launch below.")
        self.toplayout.addWidget(self.label)
        # Create a horizontal layout box, one column for each control library
        self.subwdg = QtGui.QWidget(self)
        self.toplayout.addWidget(self.subwdg)
        self.horizlayout0 = QtGui.QHBoxLayout(self.subwdg)
        # Add one column for the historical data viewer
        self.subwdgview = QtGui.QWidget(self)
        self.horizlayout0.addWidget(self.subwdgview)
        self.vertlayoutview = QtGui.QVBoxLayout(self.subwdgview)
        # Add one column for the EPICS control library
        self.subwdgepics = QtGui.QWidget(self)
        self.horizlayout0.addWidget(self.subwdgepics)
        self.vertlayoutepics = QtGui.QVBoxLayout(self.subwdgepics)
        # Add one column for the Tango control library
        self.subwdgtango = QtGui.QWidget(self)
        self.horizlayout0.addWidget(self.subwdgtango)
        self.vertlayouttango = QtGui.QVBoxLayout(self.subwdgtango)
        # Add one column for the Finance control library
        self.subwdgfinance = QtGui.QWidget(self)
        self.horizlayout0.addWidget(self.subwdgfinance)
        self.vertlayoutfinance = QtGui.QVBoxLayout(self.subwdgfinance)
        # Add one column for the Random control library
        self.subwdgrandom = QtGui.QWidget(self)
        self.horizlayout0.addWidget(self.subwdgrandom)
        self.vertlayoutrandom = QtGui.QVBoxLayout(self.subwdgrandom)
        # Occupy the historical data viewer column
        self.viewdata = QtGui.QLabel("Data Viewer:")
        self.viewdataNV = QtGui.QPushButton("Plotting")
        self.viewdataTF = QtGui.QPushButton("Boolean Controller")
        self.viewdataAlarms = QtGui.QPushButton("Value Alarms")
        self.vertlayoutview.addWidget(self.viewdata)
        self.vertlayoutview.addWidget(self.viewdataNV)
        self.vertlayoutview.addWidget(self.viewdataTF)
        self.vertlayoutview.addWidget(self.viewdataAlarms)
        self.viewdataNV.clicked.connect(self.viewdataNVclicked)
        self.viewdataTF.setEnabled(False)
        self.viewdataTF.setToolTip("Not applicable.")
        self.viewdataAlarms.setEnabled(False)
        self.viewdataAlarms.setToolTip("Not applicable.")
        # Occupy the Epics control library column
        self.epics = QtGui.QLabel("Epics:")
        self.epicsNV = QtGui.QPushButton("Plotting")
        self.epicsTF = QtGui.QPushButton("Boolean Controller")
        self.epicsAlarms = QtGui.QPushButton("Value Alarms")
        self.vertlayoutepics.addWidget(self.epics)
        self.vertlayoutepics.addWidget(self.epicsNV)
        self.vertlayoutepics.addWidget(self.epicsTF)
        self.vertlayoutepics.addWidget(self.epicsAlarms)
        self.epicsNV.clicked.connect(self.epicsNVclicked)
        self.epicsTF.clicked.connect(self.epicsTFclicked)
        self.epicsAlarms.clicked.connect(self.epicsAlarmsclicked)
        # Occupy the Tango control library column
        self.tango = QtGui.QLabel("Tango:")
        self.tangoNV = QtGui.QPushButton("Plotting")
        self.tangoTF = QtGui.QPushButton("Boolean Controller")
        self.tangoAlarms = QtGui.QPushButton("Value Alarms")
        self.vertlayouttango.addWidget(self.tango)
        self.vertlayouttango.addWidget(self.tangoNV)
        self.vertlayouttango.addWidget(self.tangoTF)
        self.vertlayouttango.addWidget(self.tangoAlarms)
        self.tangoNV.clicked.connect(self.tangoNVclicked)
        self.tangoTF.clicked.connect(self.tangoTFclicked)
        self.tangoAlarms.clicked.connect(self.tangoAlarmsclicked)
        # Occupy the Finance control library column
        self.finance = QtGui.QLabel("Finance")
        self.financeNV = QtGui.QPushButton("Plotting")
        self.financeTF = QtGui.QPushButton("Boolean Controller")
        self.financeAlarms = QtGui.QPushButton("Value Alarms")
        self.vertlayoutfinance.addWidget(self.finance)
        self.vertlayoutfinance.addWidget(self.financeNV)
        self.vertlayoutfinance.addWidget(self.financeTF)
        self.vertlayoutfinance.addWidget(self.financeAlarms)
        self.financeNV.clicked.connect(self.financeNVclicked)
        self.financeAlarms.clicked.connect(self.financeAlarmsclicked)
        self.financeTF.setEnabled(False)
        self.financeTF.setToolTip("Not applicable.")
        # Occupy the Random control library column
        self.random = QtGui.QLabel("Random")
        self.randomNV = QtGui.QPushButton("Plotting")
        self.randomTF = QtGui.QPushButton("Boolean Controller")
        self.randomAlarms = QtGui.QPushButton("Value Alarms")
        self.vertlayoutrandom.addWidget(self.random)
        self.vertlayoutrandom.addWidget(self.randomNV)
        self.vertlayoutrandom.addWidget(self.randomTF)
        self.vertlayoutrandom.addWidget(self.randomAlarms)
        self.randomNV.clicked.connect(self.randomNVclicked)
        self.randomTF.clicked.connect(self.randomTFclicked)
        self.randomAlarms.clicked.connect(self.randomAlarmsclicked)
        # Create a text edit (and its associated widgets) allowing user to define configuration package for a control library to load
        self.subwdgconffile = QtGui.QWidget(self)
        self.toplayout.addWidget(self.subwdgconffile)
        self.horizlayout1 = QtGui.QHBoxLayout(self.subwdgconffile)
        self.conffilelbl = QtGui.QLabel("Configuration file: >>")
        self.conffilepath = QtGui.QLineEdit()
        self.conffilebtn = QtGui.QPushButton("Browse..")
        self.conffilebtn.clicked.connect(self.browseFilesClicked)
        self.horizlayout1.addWidget(self.conffilelbl)
        self.horizlayout1.addWidget(self.conffilepath)
        self.horizlayout1.addWidget(self.conffilebtn)
    def viewdataNVclicked(self):
        # Launch DynaGUI NV with historical data viewer
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_NV.py 'HistoricalData' "+fp+"&")
        self.close()
        print("View data NV clicked")
    def epicsNVclicked(self):
        # Launch DynaGUI NV with the EPICS control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_NV.py 'EPICS' "+fp+"&")
        self.close()
        print("EPICS NV clicked")
    def epicsTFclicked(self):
        # Launch DynaGUI TF with the EPICS control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_TF.py 'EPICS' "+fp+"&")
        print("EPICS TF clicked")
    def epicsAlarmsclicked(self):
        # Launch DynaGUI Alarms with the EPICS control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_Alarms.py 'EPICS' "+fp+"&")
        print("EPICS Alarms clicked")
    def tangoNVclicked(self):
        # Launch DynaGUI NV with the Tango control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_NV.py 'Tango' "+fp+"&")
        print("Tango NV clicked")
    def tangoTFclicked(self):
        # Launch DynaGUI TF with the Tango control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_TF.py 'Tango' "+fp+"&")
        print("Tango TF clicked")
    def tangoAlarmsclicked(self):
        # Launch DynaGUI Alarms with the Tango control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_Alarms.py 'Tango' "+fp+"&")
        print("Tango Alarms clicked")
    def financeNVclicked(self):
        # Launch DynaGUI NV with the Finance control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_NV.py 'Finance' "+fp+"&")
        print("Finance NV clicked")
    def financeAlarmsclicked(self):
        # Launch DynaGUI Alarms with the Finance control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_Alarms.py 'Finance' "+fp+"&")
        print("Finance Alarms clicked")
    def randomNVclicked(self):
        # Launch DynaGUI NV with the Random control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_NV.py 'Randomizer' "+fp+"&")
        print("Random NV clicked")
    def randomTFclicked(self):
        # Launch DynaGUI TF with the Random control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_TF.py 'Randomizer' "+fp+"&")
        print("Random TF clicked")
    def randomAlarmsclicked(self):
        # Launch DynaGUI Alarms with the Random control library
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        os.system("python "+dirpath+"/dynagui_files/DynaGUI_Alarms.py 'Randomizer' "+fp+"&")
        print("Random Alarms clicked")
    def browseFilesClicked(self):
        # Find a configuration file to launch a DynaGUI package with
        dirpath = os.path.abspath(os.path.dirname(__file__))
        nameoffile = QtGui.QFileDialog.getOpenFileName(self, 'Load File', dirpath+'/dynagui_files/ConfFiles')
        if len(nameoffile) > 1:
            nameoffile = str(nameoffile[0])
        self.conffilepath.setText(nameoffile)
if __name__ == '__main__':
    # The GUI is being been launched, no input arguments used
    if packagefailure[0] == 0:
        app = QtGui.QApplication(sys.argv)
        window = Dialog(packagefailure)
        window.show()
        sys.exit(app.exec_())
