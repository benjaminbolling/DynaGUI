# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 03:30:21 2019

@author: controlroom
"""

try:
    import PyQt5.QtWidgets as QtGui
    from PyQt5 import QtCore
except:
    from PyQt4 import QtCore, QtGui
import sys
import os

class Dialog(QtGui.QDialog):
    def __init__(self, inp):
        QtGui.QDialog.__init__(self)
        
        self.toplayout = QtGui.QVBoxLayout(self)
        
        controlsystems = ['TANGO', 'EPICS', 'Other']
        
        self.setWindowTitle("DynaGUI Launcher")
        
        self.controlsystemsBox = QtGui.QComboBox(self)
        self.controlsystemsBox.addItems(controlsystems)
        self.controlsystemsBox.currentIndexChanged.connect(self.controlsyscomboclicked)
        
        self.controlsystem = 'TANGO'
        self.controlpanel = 'AtkPanel'
        
        self.controlpanelbox = QtGui.QLineEdit(self.controlpanel)
        self.conffilepath = QtGui.QLineEdit()
        
        text_controlsystem = QtGui.QLabel('Control system:')
        text_controlpanel = QtGui.QLabel('Control Panel:')
        text_conffilepath = QtGui.QLabel('File path to configuration file:')
        
        self.toplayout.addWidget(text_controlsystem)
        self.toplayout.addWidget(self.controlsystemsBox)
        
        self.toplayout.addWidget(text_controlpanel)
        self.toplayout.addWidget(self.controlpanelbox)
        
        self.browseFiles = QtGui.QPushButton("Browse")
        self.browseFiles.clicked.connect(self.browseFilesClicked)
        
        self.toplayout.addWidget(text_conffilepath)
        Hlayout1 = QtGui.QHBoxLayout()
        self.toplayout.addLayout(Hlayout1)
        Hlayout1.addWidget(self.conffilepath)
        Hlayout1.addWidget(self.browseFiles)
        
        Hlayout2 = QtGui.QHBoxLayout()
        self.toplayout.addLayout(Hlayout2)
        
        TFbtn = QtGui.QPushButton("DynaGUI TF")
        NVbtn = QtGui.QPushButton("DynaGUI NV")
        Alarmsbtn = QtGui.QPushButton("DynaGUI Alarms")
        
        TFbtn.clicked.connect(self.TFbtnClicked)
        NVbtn.clicked.connect(self.NVbtnClicked)
        Alarmsbtn.clicked.connect(self.AlarmsbtnClicked)
        
        Hlayout2.addWidget(TFbtn)
        Hlayout2.addWidget(NVbtn)
        Hlayout2.addWidget(Alarmsbtn)
    
    def browseFilesClicked(self):
        nameoffile = QtGui.QFileDialog.getOpenFileName(self, 'Load File')
        if nameoffile:
            self.conffilepath.setText(nameoffile)
    
    def TFbtnClicked(self):
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        if self.controlsystem == 'TANGO':
            os.system("python "+dirpath+"/DynaGUI_TF_Tango.py "+fp+"&")
        else:
            QtGui.QMessageBox.information(self,'Information', 'This will be added in a future release.')
        self.close()
        
    def NVbtnClicked(self):
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        if self.controlsystem == 'TANGO':
            os.system("python "+dirpath+"/DynaGUI_NV_Tango.py "+fp+"&")
        else:
            QtGui.QMessageBox.information(self,'Information', 'This will be added in a future release.')
        self.close()
        
    def AlarmsbtnClicked(self):
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        if self.controlsystem == 'TANGO':
            os.system("python "+dirpath+"/DynaGUI_Alarms_Tango.py "+fp+"&")
        else:
            QtGui.QMessageBox.information(self,'Information', 'This will be added in a future release.')
        self.close()
        
        
    def controlsyscomboclicked(self):
        self.controlsystem = str(self.controlsystemsBox.currentText())
        
        if self.controlsystem == 'TANGO':
            self.controlpanelbox.setText('AtkPanel')
        elif self.controlsystem == 'EPICS':
            self.controlpanelbox.setText('iGp')
        elif self.controlsystem == 'Other':
            self.controlpanelbox.setText('Define the Control Panel')

if __name__ == '__main__':
    try:
        inp = sys.argv[1]
    except:
        inp = 0
    app = QtGui.QApplication(sys.argv)
    window = Dialog(inp)
    window.show()
    sys.exit(app.exec_())