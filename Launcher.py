# -*- coding: utf-8 -*-
"""
<A Dynamic Graphical User Interface package, which gives users a method to construct temporary, permanent and/or a set of GUI:s for users in a simple and fast manner combined with diagnostics tools (with advance 1D and 2D plotting methods).>
    Copyright (C) <2019>  <Benjamin Edward Bolling>

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

try:
    import PyQt5.QtWidgets as QtGui
    from PyQt5 import QtCore
except:
    from PyQt4 import QtCore, QtGui
import sys
import os

class Dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
        self.toplayout = QtGui.QVBoxLayout(self)
        
        controlsystems = ['TANGO', 'EPICS', 'Randomizer', 'Other']
        
        self.setWindowTitle("DynaGUI Launcher")
        
        self.controlsystemsBox = QtGui.QComboBox(self)
        self.controlsystemsBox.addItems(controlsystems)
        self.controlsystemsBox.currentIndexChanged.connect(self.controlsyscomboclicked)
        
        self.controlsystem = 'TANGO'
        
        self.conffilepath = QtGui.QLineEdit()
        
        text_controlsystem = QtGui.QLabel('Control system:')
        text_conffilepath = QtGui.QLabel('File path to configuration file:')
        
        self.toplayout.addWidget(text_controlsystem)
        self.toplayout.addWidget(self.controlsystemsBox)
        
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
        nameoffile = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '/mxn/groups/operators/controlroom/python_programs/qtw_DynaGUI/ConfFiles')
        if nameoffile:
            self.conffilepath.setText(nameoffile)
    
    def TFbtnClicked(self):
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        if self.controlsystem == 'TANGO':
            os.system("python "+dirpath+"/DynaGUI_TF.py 'Tango' "+fp+"&")
        elif self.controlsystem == 'Randomizer':
            os.system("python "+dirpath+"/DynaGUI_TF.py 'Randomizer' "+fp+"&")
        else:
            QtGui.QMessageBox.information(self,'Information', 'This will be added in a future release.')
        self.close()
        
    def NVbtnClicked(self):
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        if self.controlsystem == 'TANGO':
            os.system("python "+dirpath+"/DynaGUI_NV.py 'Tango' "+fp+"&")
        elif self.controlsystem == 'Randomizer':
            os.system("python "+dirpath+"/DynaGUI_NV.py 'Randomizer' "+fp+"&")
        else:
            QtGui.QMessageBox.information(self,'Information', 'This will be added in a future release.')
        self.close()
        
    def AlarmsbtnClicked(self):
        dirpath = os.path.abspath(os.path.dirname(__file__))
        fp = str(self.conffilepath.text())
        if self.controlsystem == 'TANGO':
            os.system("python "+dirpath+"/DynaGUI_Alarms.py 'Tango' "+fp+"&")
        elif self.controlsystem == 'Randomizer':
            os.system("python "+dirpath+"/DynaGUI_Alarms.py 'Randomizer' "+fp+"&")
        else:
            QtGui.QMessageBox.information(self,'Information', 'This will be added in a future release.')
        self.close()
        
        
    def controlsyscomboclicked(self):
        self.controlsystem = str(self.controlsystemsBox.currentText())

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Dialog()
    window.show()
    sys.exit(app.exec_())