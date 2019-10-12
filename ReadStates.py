# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 09:01:37 2019

@author: benbol

A function that is a complement to the Stategrid. It can be run to check status of all PS:s.
"""

from PyQt4 import QtGui
import PyTango as PT
import gtk
from time import sleep

# Define the DialogBox
class DialogBox(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.changeRbtn = QtGui.QPushButton("Switch")  
        self.changeRbtn.clicked.connect(self.switchRing)
        
        self.accLbl = QtGui.QLabel("Accelerators: ALL")
        
        self.getallDevsBtn = QtGui.QPushButton("Get all PS Devices")
        self.getallDevsBtn.clicked.connect(self.getallDevs)
        
        self.getallDevsBtn = QtGui.QPushButton("Get all BPM Devices")
        self.getallDevsBtn.clicked.connect(self.getallBpms)
        
        
        self.getallStatesBtn = QtGui.QPushButton("Get all PS States")
        self.getallStatesBtn.clicked.connect(self.getallStates)
        self.getallStatesBtn.setEnabled(False)
        
        self.statusbtn1 = QtGui.QPushButton("No issues.")
        self.statusbtn1.clicked.connect(self.status1click)
        self.statusbtn1.setEnabled(False)
        
        self.level1lbl = QtGui.QLabel("Level 1: Check states")
        self.level1lbl.setStyleSheet('background-color: lime')
        
        self.level2lbl = QtGui.QLabel("Level 2: Check if RV updates")
        self.level2lbl.setStyleSheet('background-color: lime')
        
        self.readcurrbtn = QtGui.QPushButton("Read currents")
        self.readcurrbtn.clicked.connect(self.getAllCurrents)
        self.readcurrbtn.setEnabled(False)
        
        self.copyalldevsbtn = QtGui.QPushButton("Copy Devices to Clipboard")
        self.copyalldevsbtn.clicked.connect(self.copyall)
        self.copyalldevsbtn.setEnabled(False)
        
        layout = QtGui.QGridLayout()
        layout.addWidget(self.accLbl,0,0,1,1)
        layout.addWidget(self.changeRbtn,0,1,1,1)
        layout.addWidget(self.copyalldevsbtn,0,2,1,1)
        
        layout.addWidget(self.level1lbl, 1,0,1,3)
        
        layout.addWidget(self.getallDevsBtn,2,0,1,1)
        layout.addWidget(self.getallStatesBtn,2,1,1,1)
        layout.addWidget(self.statusbtn1,2,2,1,1)
        
        layout.addWidget(self.level2lbl, 3,0,1,3)
        
        layout.addWidget(self.readcurrbtn,4,0,1,1)
        
        self.setWindowTitle("Check all PS States")
        self.setLayout(layout)
        self.setGeometry(100, 100, 600, 100)
        
    def switchRing(self):
        self.getallStatesBtn.setEnabled(False)
        self.statusbtn1.setEnabled(False)
        self.readcurrbtn.setEnabled(False)
        self.copyalldevsbtn.setEnabled(False)
        if self.accLbl.text() == "Accelerator: Linac":
            self.accLbl.setText("Accelerator: R1")
        elif self.accLbl.text() == "Accelerator: R1":
            self.accLbl.setText("Accelerator: R3")
        elif self.accLbl.text() == "Accelerator: R3":
            self.accLbl.setText("Accelerators: ALL")
        elif self.accLbl.text() == "Accelerators: ALL":
            self.accLbl.setText("Accelerator: Linac")


    def getallBpms(self):
        db = PT.Database()
        devR3 = db.get_device_exported_for_class('LiberaDeviceClass')[:]
        devR3 = filter(lambda v: v.startswith('R3') and not 'TIM' in v,devR3)
        self.R3bpms = filter(lambda v: v.startswith('R3') and not 'GDX' in v,devR3)
        devR1 = db.get_device_exported_for_class('LiberaBrilliancePlus')[:]
        devR1 = filter(lambda v: v.startswith('R1'),devR1)
        self.R1bpms = filter(lambda v: v.startswith('R1') and not 'GDX' in v,devR1)

    def getallDevs(self):
        if self.accLbl.text() == "Accelerator: R3":
            selects = ['*R3-*']
        elif self.accLbl.text() == "Accelerator: Linac":
            selects = ['*I-*']
        elif self.accLbl.text() == "Accelerator: R1":
            selects = ['*R1-*']
        elif self.accLbl.text() == "Accelerators: ALL":
            selects = ['*R3-*', '*R1-*', '*I-*']
        
        
        for select in selects:
            devsysdb = PT.DeviceProxy('sys/database/2')
            danfysiklist =  devsysdb.DbGetDeviceList([select,'*Danfysik*'])
            deltalist =  devsysdb.DbGetDeviceList([select,'*Delta*'])
            itestlist =  devsysdb.DbGetDeviceList([select,'*Itest*'])
            allmagnetps = danfysiklist + deltalist + itestlist
            sel = str(str(select.split('*')[1]).split('-')[0])
            
            self.toplayout = QtGui.QVBoxLayout(self)
            
            if sel == 'R3':
                self.R3magnetPS = []
                for item in allmagnetps:
                    if item.startswith(sel):
                        self.R3magnetPS.append(item)
            elif sel == 'R1':
                self.R1magnetPS = []
                for item in allmagnetps:
                    if item.startswith(sel):
                        self.R1magnetPS.append(item)
            elif sel == 'I':
                self.ImagnetPS = []
                for item in allmagnetps:
                    if item.startswith(sel):
                        self.ImagnetPS.append(item)
        
        if self.accLbl.text() == "Accelerator: R3":
            self.allmagnetps = self.R3magnetPS
        elif self.accLbl.text() == "Accelerator: Linac":
            self.allmagnetps = self.ImagnetPS
        elif self.accLbl.text() == "Accelerator: R1":
            self.allmagnetps = self.R1magnetPS
        elif self.accLbl.text() == "Accelerators: ALL":
            self.allmagnetps = self.ImagnetPS + self.R1magnetPS + self.R3magnetPS
        
        self.getallStatesBtn.setEnabled(True)
        self.readcurrbtn.setEnabled(True)
        self.copyalldevsbtn.setEnabled(True)
        
    def getallStates(self):
        self.statusbtn1.setText('Loading...')
        
        QtGui.QApplication.processEvents()
        
        # Why on EARTH do I need to process events twice ????
        
        QtGui.QApplication.processEvents()
        
        self.getAllStates1()
        
    def getAllStates1(self):
        self.msg = 'Errors:'
        statusflag = 0
        for PS in self.allmagnetps:
            prox = [PT.DeviceProxy(str(PS))]
            for dev in prox:
                try:
                    state = str(dev.read_attribute('State').value)
                    if state != 'ON' and state != 'MOVING':
                        self.msg = str(self.msg + '\n' +str(str(PS)+' '+state))
                        statusflag = 1
                except:
                    self.msg = str(self.msg + '\n' +'Cannot connect to '+str(PS))
                    statusflag = 1
        self.statusbtn1.setText('Done! No issues found.')
        if statusflag == 1:
            self.statusbtn1.setText('Done! Press to check issues.')
            self.statusbtn1.setEnabled(True)
    
    def status1click(self):
        QtGui.QMessageBox.warning(self, 'PS issues',self.msg)
    
    def copyall(self):
        msg = ''
        for item in self.allmagnetps:
            msg = str(msg + str(item) + '\n')
        
        
        
        clipboard = gtk.clipboard_get()
        clipboard.set_text(msg)
        clipboard.store()

        #cmd = 'echo '+msg.strip()+'|clip'
        #subprocess.check_call(cmd, shell = True)
        
        
        #QtGui.QMessageBox.information(self, str(str(self.accLbl.text().split()[1])+'MAG PS'),msg)
    
    def getAllCurrents(self):
        print("reading currents")
        
        curr0 = []
        curr1 = []
        curr2 = []
        faileddevs = []
        successfuldevs = []
        
        for item in self.allmagnetps:
            try:
                for dev in [PT.DeviceProxy(str(item))]:
                    curr0.append(str(dev.read_attribute('Current').value))
                    successfuldevs.append(item)
            except:
                faileddevs.append(str(item))
        print("Read 1 complete")
        zerovalsdevs = successfuldevs
        sleep(1)
        
        for item in zerovalsdevs:
            for dev in [PT.DeviceProxy(str(item))]:
                curr1.append(str(dev.read_attribute('Current').value))
        print("Read 2 complete")
        sleep(1)
        
        for ind,val in enumerate(curr0):
            if float(curr0[ind]) - float(curr1[ind]) != 0:
                zerovalsdevs.append(successfuldevs[ind])
        
        for item in zerovalsdevs:
            for dev in [PT.DeviceProxy(str(item))]:
                curr2.append(str(dev.read_attribute('Current').value))
        print("Read 3 complete")        
        
        
        """
        zerovalsdevs = []
        for ind,val in enumerate(curr0):
            if float(curr0[ind]) - float(curr1[ind]) == 0:
                if float(curr2[ind]) - float(curr1[ind]) == 0:
                    zerovalsdevs.append(successfuldevs[ind])
        
        print(zerovalsdevs)
        
        print(curr0)
        print('- - - - -')
        print(len(curr0))
        print(len(successfuldevs))
        
        print(len(faileddevs))
        """
if __name__ == "__main__":
    app = QtGui.QApplication([])
    form = DialogBox()
    form.show()
    app.exec_()
