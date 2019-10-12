# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:59:21 2019

@author: controlroom [benjamin bolling]

DynaGUI NV (Numerical Values)

"""
try:
    import PyQt5.QtWidgets as QtGui
    import PyQt5.QtGui as QtGui2
    from PyQt5 import QtCore
except:
    from PyQt4 import QtCore, QtGui

import PyTango as PT
import os
from datetime import datetime
from time import sleep
import sys
class Dialog(QtGui.QDialog):
    def __init__(self, inp):
        QtGui.QDialog.__init__(self)
        if inp == 0:
            loadflag = 0
        else:
            try:
                self.loadfile(inp,1)
                self.Nrows
                loadflag = 1
            except:
                loadflag = 0
        if loadflag == 0:
            # List of devices' server domains.
            self.devdoms = ['r3-319l/dia/tco-01/temperature',
                            'r3-319l/dia/tco-02/temperature',
                            'r3-319l/dia/tco-03/temperature',
                            'r1-101/dia/bpm-01/xmeanpossa']
            
            self.devdesc = ['R3 319 TCO 01 temperature',
                            'R3 319 TCO 02 temperature',
                            'R3 319 TCO 03 temperature',
                            'R1 101 BPM 01 x-pos']
            
            self.devlims = [36,
                            38,
                            40]
            
            self.Nrows = 20
        self.reloadflag = 0
        self.maxsize = 0
        self.timerinterval = 30 # seconds
        
        self.setWindowTitle("DynaGUI Alarms")
        
        # Construct the toplayout and make it stretchable
        self.toplayout = QtGui.QVBoxLayout(self)
        self.toplayout.addStretch()
        
        # Construct a horizontal layout box for the edit and get all attribute buttons (must be a sublayer of the toplayout)
        self.editgetallwdg = QtGui.QWidget(self)
        self.toplayout.addWidget(self.editgetallwdg)
        self.horizlayout0 = QtGui.QHBoxLayout(self.editgetallwdg)
        
        # Construct the button for setting up a dynamic list of attributes
        self.listbtn = QtGui.QPushButton("Edit DynaGUI")
        self.listbtn.clicked.connect(self.listbtnclicked)
        self.listbtn.setEnabled(True)
        self.horizlayout0.addWidget(self.listbtn)
        try:
            self.doublevalidator = QtGui.QDoubleValidator(-float('inf'),float('inf'),5)
        except:
            self.doublevalidator = QtGui2.QDoubleValidator(-float('inf'),float('inf'),5)
        
        # Now we construct the sublayout which will consist of the dynamically constructed buttons of the lists defined above (in example; list1 or list2)
        self.sublayout = QtGui.QGridLayout()
        self.toplayout.addLayout(self.sublayout)
        
        # Now we construct a groupbox for all the dynamically constructed buttons. Edit its text to whatever is appropriate. Then its added to the sublayout.# Now we construct the sublayout which will consist of the dynamically constructed buttons of the lists defined above (in example; list1 or list2)
        self.groupBox = QtGui.QGroupBox()
        self.sublayout.addWidget(self.groupBox)
        self.sublayout = QtGui.QGridLayout(self.groupBox)
        
        # Construct a simple label widget which in this example has the purpose of displaying various messages to the user (status messages)
        self.bottomlabel = QtGui.QLabel("")
        self.toplayout.addWidget(self.bottomlabel)
        
        # Construct a horizontal layout box for the load and save buttons (must be a sublayer of the toplayout)
        self.loadsavewdg = QtGui.QWidget(self)
        self.toplayout.addWidget(self.loadsavewdg)
        self.horizlayout1 = QtGui.QHBoxLayout(self.loadsavewdg)
        
        # Construct a horiztontal layout box for the Plot and Update buttons (must be a sublayer of the toplayout)
        self.plotupdwdg = QtGui.QWidget(self)
        self.toplayout.addWidget(self.plotupdwdg)
        self.horizlayout2 = QtGui.QHBoxLayout(self.plotupdwdg)
        
        # Construct the load and save buttons, connect them to their functions and add them to their horizontal container
        self.loadbtn = QtGui.QPushButton("Load")
        self.savebtn = QtGui.QPushButton("Save")
        self.loadbtn.clicked.connect(self.loadbtnclicked)
        self.loadbtn.setShortcut("Ctrl+o")
        self.loadbtn.setToolTip("Load a configuration (ctrl+o).")
        self.savebtn.clicked.connect(self.savebtnclicked)
        self.savebtn.setShortcut("Ctrl+s")
        self.savebtn.setToolTip("Save a configuration (ctrl+s).")
        self.horizlayout1.addWidget(self.loadbtn)
        self.horizlayout1.addWidget(self.savebtn)
        
        self.startstopbtn = QtGui.QPushButton("Not running. Press to activate.")
        self.startstopbtn.clicked.connect(self.startstopclicked)
        self.startstopbtn.setStyleSheet('QPushButton {background-color: maroon; color: white}')
        self.toplayout.addWidget(self.startstopbtn)
        # Run the script for generating the dynamical buttons
        self.getallDevs()
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.statuscheck)
        
    def savebtnclicked(self):
        nameoffile = QtGui.QFileDialog.getSaveFileName(self, 'Save to File')
        if not nameoffile:
            self.bottomlabel.setText("Cancelled save configuration.")
        else:
            file = open(nameoffile, 'w')
            self.toSave = str('IamaDynaGUIalarmFile' + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.devdoms) + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.devdesc) + '\n' + "##IamYourSeparator##\n" + '\n'.join(map(str, self.devlims)) + '\n' + "##IamYourSeparator##\n" + str(self.Nrows))
            file.write(self.toSave)
            file.close()
            self.bottomlabel.setText("Configuration saved to file.")
            self.bottomlabel.setToolTip("Saved configuation to file: "+nameoffile)
    
    def loadbtnclicked(self):
        nameoffile = QtGui.QFileDialog.getOpenFileName(self, 'Load File')
        if not nameoffile:
            self.bottomlabel.setText("Cancelled loading configuration.")
        else:
            self.loadfile(nameoffile,0)
            
    def loadfile(self,nameoffile,inp2):
            print(nameoffile)
            file = open(nameoffile, 'r')
            splitToLoad = file.read()
            splitToLoad = splitToLoad.split("##IamYourSeparator##")
            identifier = splitToLoad[0].split('\n')
            while("" in identifier): # Get rid of empty strings
                identifier.remove("")
            if identifier[0] == 'IamaDynaGUIalarmFile':
                try:
                    devdoms = splitToLoad[1].split("\n")
                    while("" in devdoms): # Get rid of empty strings
                        devdoms.remove("")
                    devdesc = splitToLoad[2].split("\n")
                    while("" in devdesc): # Get rid of empty strings
                        devdesc.remove("")
                    devlims = splitToLoad[3].split("\n")
                    while("" in devlims): # Get rid of empty strings
                        devlims.remove("")
                    devvlims = [float(i) for i in devlims]
                    Nrows = float(splitToLoad[4].split("\n")[1])
                    self.devdoms = devdoms
                    self.devdesc = devdesc
                    self.devlims = devvlims
                    self.Nrows = float(Nrows)
                    if inp2 == 0:
                        self.bottomlabel.setText("Loaded configuration.")
                        # Destroy the current buttons.
                        self.killdynamicbuttongroup()
                        # All buttons are gone, so lets construct the new buttons.
                        self.getallDevs()
                        # The layout should be minimal, so make it unrealistically small (x=10, y=10 [px]) and then resize to minimum.
                        self.setMaximumSize(10,10)
                        self.resize(self.sizeHint().width(), self.sizeHint().height())
                        self.bottomlabel.setToolTip("Loaded configuration from file: "+nameoffile)
                except:
                    if inp2 == 0:
                        self.bottomlabel.setText("Conf. file error: Missing separator(s).")
            else:
                if inp2 == 0:
                    self.bottomlabel.setText("Not a DynaGUI alarm file - missing identifier.")

    def killdynamicbuttongroup(self):
        # Destroy / kill all buttons currently constructed in the buttongroup.
        for i in reversed(range(self.sublayout.count())):
            item = self.sublayout.itemAt(i)
            if isinstance(item, QtGui.QWidgetItem):
                item.widget().close()

    def getallDevs(self):
        rowcount = -1
        colcount = 0
        
        # Here the construction begins for all the checkboxes, and we make them all belong to the groupbox.
        for numm, index in enumerate(self.devdesc):
            rowcount += 1
            button = QtGui.QCheckBox(index, self.groupBox)
            button.setToolTip(self.devdoms[numm])
            try:
                textbox = QtGui.QLineEdit(str(self.devlims[numm]), self.groupBox)
            except:
                textbox = QtGui.QLineEdit(str(0), self.groupBox)
            textbox.setValidator(self.doublevalidator)
            combobox = QtGui.QComboBox(self.groupBox)
            combobox.addItem("<")
            combobox.addItem(">")
            
            textbox.setEnabled(True)
            label = QtGui.QLabel("-",self.groupBox)
            self.sublayout.addWidget(button,rowcount,colcount,1,1)
            self.sublayout.addWidget(label,rowcount,colcount+1,1,1)
            self.sublayout.addWidget(combobox,rowcount,colcount+2,1,1)
            self.sublayout.addWidget(textbox,rowcount,colcount+3,1,1)
            if rowcount == self.Nrows - 1:
                rowcount = -1
                colcount += 4
        
        # Here we construct the buttongroup.
        self.buttonGroup = QtGui.QButtonGroup(self)
        
        # Here we add all buttons to the buttongroup.
        for button in self.groupBox.findChildren(QtGui.QPushButton):
            if self.buttonGroup.id(button) < 0:
                self.buttonGroup.addButton(button)
        
        # Get the statuses
        self.statuscheck()
    
    def startstopclicked(self):
        if self.timer.isActive():
            self.timer.stop()
            self.startstopbtn.setText("Not running. Press to activate.")
            self.startstopbtn.setStyleSheet('QPushButton {background-color: maroon; color: white}')
        else:
            self.statuscheck()
            self.timer.start(self.timerinterval * 1000)
            self.startstopbtn.setText("Running. Press to deactivate.")
            self.startstopbtn.setStyleSheet('QPushButton {background-color: lime; color: black}')
    
    def clock(self):
        print("tic-tac")
    
    def statuscheck(self):
        self.alarmflag = 0
        checkboxes = self.groupBox.findChildren(QtGui.QCheckBox)
        lineedits = self.groupBox.findChildren(QtGui.QLineEdit)
        labels = self.groupBox.findChildren(QtGui.QLabel)
        combos = self.groupBox.findChildren(QtGui.QComboBox)
        for ind, item in enumerate(checkboxes):
            splitt = str(item.toolTip()).split("/")
            attr = splitt[len(splitt)-1]
            proxy = str("/".join(splitt[0:len(splitt)-1]))
            prox = [PT.DeviceProxy(str(proxy))]
            lorm = str(combos[ind].currentText())
            
            for bd in prox:
                val = bd.read_attribute(attr).value
            labels[ind].setText(str(val))
            if item.isChecked():
                if lorm == "<":
                    if val > float(lineedits[ind].text()):
                        string = str(str(str(str(splitt[0]).split("-")[1]) + " " + str(splitt[len(splitt)-2]) + " in " + str(attr) + " alarm"))
                        self.bottomlabel.setText(string)
                        item.setStyleSheet("background-color: red")
                        if self.alarmflag == 0:
                            os.system('spd-say "' + string + '"')
                            self.alarmflag = 1
                    else:
                        item.setStyleSheet("background-color: lime")
                        
                elif lorm == ">":
                    if val < float(lineedits[ind].text()):
                        string = str(str(str(str(splitt[0]).split("-")[1]) + " " + str(splitt[len(splitt)-2]) + " in " + str(attr) + " alarm"))
                        self.bottomlabel.setText(string)
                        item.setStyleSheet("background-color: red")
                        if self.alarmflag == 0:
                            os.system('spd-say "' + string + '"')
                            self.alarmflag = 1
                    else:
                        item.setStyleSheet("background-color: lime")
            
    def listbtnclicked(self):
        listGui = listbtnGUI(self)
        listGui.setModal(True)
        listGui.exec_()
        
        if self.reloadflag == 1:
            self.maxsize = 0
            self.killdynamicbuttongroup()
            self.getallDevs()
            
            # The layout should be minimal, so make it unrealistically small (x=10, y=10 [px]) and then resize to minimum.
            self.reloadflag = 0
    
    def closeEvent(self, event):
        self.timer.stop()

class listbtnGUI(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(listbtnGUI, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Edit DynaGUI Alarms")
        listgui = QtGui.QFormLayout(self)
        
        devslbl = QtGui.QLabel("List of devices' server domains:")
        self.textboxDevs = QtGui.QPlainTextEdit('\n'.join(parent.devdoms))
        
        desclbl = QtGui.QLabel("List of devices' descriptions:")
        self.textboxDesc = QtGui.QPlainTextEdit('\n'.join(parent.devdesc))
        
        rowslbl = QtGui.QLabel("Max. number of rows:")
        self.textboxRows = QtGui.QSpinBox()
        self.textboxRows.setValue(parent.Nrows)
        
        tmrlbl = QtGui.QLabel("Alarms timer [s]")
        self.textboxTmr = QtGui.QSpinBox()
        self.textboxTmr.setValue(parent.timerinterval)
        
        okbtn = QtGui.QPushButton('Ok')
        nobtn = QtGui.QPushButton('Cancel')
        
        
        listgui.addRow(devslbl,desclbl)
        listgui.addRow(self.textboxDevs,self.textboxDesc)
        
        listgui.addRow(rowslbl,self.textboxRows)
        
        listgui.addRow(tmrlbl,self.textboxTmr)
        
        listgui.addRow(okbtn, nobtn)
        okbtn.clicked.connect(self.confirmfunc)
        nobtn.clicked.connect(self.cancelfunc)
        
        
        self.resize(self.sizeHint().width(), self.sizeHint().height())
        
    def confirmfunc(self):
        textDevs = str(self.textboxDevs.toPlainText())
        textDescs = str(self.textboxDesc.toPlainText())
        self.newlistDevs = textDevs.split()
        self.newlistDescs = textDescs.split('\n')
        
        
        # Check if all devices have domain, description and limits defined:
        if abs(len(self.newlistDevs)-len(self.newlistDescs)) == 0:
            self.parent.timerinterval = self.textboxTmr.value()
            if self.parent.devdoms != self.newlistDevs or self.parent.devdesc != self.newlistDescs:
                self.parent.devdoms = self.newlistDevs
                self.parent.devdesc = self.newlistDescs
                self.parent.reloadflag = 1
            
            if self.parent.Nrows != self.textboxRows.value():
                self.parent.Nrows = self.textboxRows.value()
                self.parent.reloadflag = 1
            self.close()
        else:
            os.system('spd-say "NO"')
            QtGui.QMessageBox.warning(self,"Error","Number of domains and descriptions must be the same.")
        
    
    def cancelfunc(self):
        self.close()

if __name__ == '__main__':
    try:
        inp = sys.argv[1]
    except:
        inp = 0
    app = QtGui.QApplication(sys.argv)
    window = Dialog(inp)
    window.show()
    sys.exit(app.exec_())
