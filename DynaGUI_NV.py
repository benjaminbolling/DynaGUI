# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:59:21 2019

@author: controlroom [benjamin bolling]

DynaGUI NV (Numerical Values)

"""
try:
    import PyQt5.QtWidgets as QtGui
    from PyQt5 import QtCore
except:
    from PyQt4 import QtCore, QtGui

import PyTango as PT
import os
from taurus.qt.qtgui.plot import TaurusTrend
import numpy as np
import pyqtgraph as pg
import sys
import matplotlib.pyplot as plt
class Dialog(QtGui.QDialog):
    def __init__(self, inp):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("DynaGUI NV")
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
            # All device attributes needed (basically which can be TRUE or False)
            self.listofbpmattributes = ['PowerSupplyReadValue',
                                   'xpossa',
                                   'MainFieldComponent',
                                   'Current',
                                   'Voltage',
                                   'Resistance',
                                   'PowerSupplySetPoint',
                                   'State',
                                   'Attribute1',
                                   'Attribute2',
                                   'Attribute3',
                                   'OutputOn']
            
            # Some list of devices. List consists of some random stuff
            self.devlist = ['R3-302/MAG/CRQF-01',
                     'R1-105/MAG/CRCOX-03',
                     'R1-106/MAG/CRCOX-03',
                     'R1-107/MAG/CRCOX-03',
                     'r3-303/mag/crsxd-01',
                     'r3-303/mag/crsxfo-01',
                     'r3-304/mag/crsxd-01',
                     'r3-304/mag/crsxfo-01',
                     'r3-305/mag/crsxd-01',
                     'r3-305/mag/crsxfo-01',
                     'r3-a110711cab08/mag/pspi-01',
                     'r3-a110711cab08/mag/pspi-02',
                     'r3-a110711cab08/mag/pspi-03',
                     'r3-a110711cab08/mag/pspi-04',
                     'r3-a110711cab08/mag/pspi-05',
                     'r3-a110711cab08/mag/pspi-06',
                     'r3-a110711cab08/mag/pspi-07',
                     'r1-101/dia/bpm-01',
                     'r1-103/dia/bpm-01',
                     'r1-103/dia/bpm-02',
                     'r1-104/dia/bpm-01',
                     'r1-104/dia/bpm-02',
                     'r1-105/dia/bpm-01',
                     'r1-105/dia/bpm-02',
                     'r1-106/dia/bpm-01',
                     'r1-107/dia/bpm-01',
                     'r1-107/dia/bpm-02',
                     'r1-108/dia/bpm-01',
                     'r1-108/dia/bpm-02',
                     'r1-109/dia/bpm-01']
            self.Nrows = 15
        self.reloadflag = 0
        self.maxsize = 0
        self.toSpecminutes = 15
        self.toSpecupdateFrequency = 2
        self.showallhideflag = False
        
        # Construct the toplayout and make it stretchable
        self.toplayout = QtGui.QVBoxLayout(self)
        self.toplayout.addStretch()
        
        # Construct the combobox for the list of attributes
        self.listofbpmattributeslistbox = QtGui.QComboBox(self)
        self.listofbpmattributeslistbox.addItems(self.listofbpmattributes)
        self.listofbpmattributeslistbox.currentIndexChanged.connect(self.statuscheck)
        self.toplayout.addWidget(self.listofbpmattributeslistbox)
        
        # Construct a horizontal layout box for the edit and get all attribute buttons (must be a sublayer of the toplayout)
        self.editgetallwdg = QtGui.QWidget(self)
        self.toplayout.addWidget(self.editgetallwdg)
        self.horizlayout0 = QtGui.QHBoxLayout(self.editgetallwdg)
        
        # Construct the button for setting up a dynamic list of attributes
        self.listbtn = QtGui.QPushButton("Edit DynaGUI")
        self.listbtn.clicked.connect(self.listbtnclicked)
        self.listbtn.setEnabled(True)
        self.horizlayout0.addWidget(self.listbtn)
        
        # Construct the button for getting all attributes of all devices
        self.getAllAttsBtn = QtGui.QPushButton("Get all attributes")
        self.getAllAttsBtn.clicked.connect(self.getAllAttsClicked)
        self.getAllAttsBtn.setEnabled(True)
        self.horizlayout0.addWidget(self.getAllAttsBtn)
        
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
        
        # Now we create a button to update the status selected in the combobox for all the dynamically constructed buttons
        self.updatebutton = QtGui.QPushButton("Update statuses")
        self.updatebutton.clicked.connect(self.statuscheck)
        self.horizlayout2.addWidget(self.updatebutton)
        
        # Now we create a button to plot the selected attribute for the available devices for which this is a valid attribute
        self.plot1Dbutton = QtGui.QPushButton("1D Plot")
        self.plot1Dbutton.clicked.connect(self.plotinTaurus)
        self.horizlayout2.addWidget(self.plot1Dbutton)
        
        # Now we create a button to plot the selected attribute for the available devices for which this is a valid attribute
        self.plot2Dbutton = QtGui.QPushButton("2D Plot")
        self.plot2Dbutton.clicked.connect(self.plotin2D)
        self.horizlayout2.addWidget(self.plot2Dbutton)
        
        # Now we create a button to plot the selected attribute for the available devices for which this is a valid attribute
        self.plotall2Dbutton = QtGui.QPushButton("2D Plot all")
        self.plotall2Dbutton.clicked.connect(self.plotallin2D)
        self.horizlayout2.addWidget(self.plotall2Dbutton)
        
        # Run the script for generating the dynamical buttons
        self.getallDevs()
        
    def savebtnclicked(self):
        nameoffile = QtGui.QFileDialog.getSaveFileName(self, 'Save to File')
        if not nameoffile:
            self.bottomlabel.setText("Cancelled save configuration.")
        else:
            file = open(nameoffile, 'w')
            self.toSave = str('IamaDynaGUIfile' + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.devlist) + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.listofbpmattributes) + '\n' + "##IamYourSeparator##\n" + str(self.Nrows))
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
            file = open(nameoffile, 'r')
            splitToLoad = file.read()
            splitToLoad = splitToLoad.split("##IamYourSeparator##")
            identifier = splitToLoad[0].split('\n')
            while("" in identifier): # Get rid of empty strings
                identifier.remove("")
            if identifier[0] == 'IamaDynaGUIfile':
                print("Identified as a DynaGUI file.")
                try:
                    devlist = splitToLoad[1].split("\n")
                    while("" in devlist): # Get rid of empty strings
                        devlist.remove("")
                    listofbpmattributes = splitToLoad[2].split("\n")
                    while("" in listofbpmattributes): # Get rid of empty strings
                        listofbpmattributes.remove("")
                    Nrows = splitToLoad[3].split("\n")[1]
                    self.devlist = devlist
                    self.listofbpmattributes = listofbpmattributes
                    self.Nrows = float(Nrows)
                    # Destroy the current buttons.
                    if inp2 == 0:
                        self.listofbpmattributeslistbox.clear()
                        self.listofbpmattributeslistbox.addItems(self.listofbpmattributes)
                        self.bottomlabel.setText("Loaded configuration.")
                        self.killdynamicbuttongroup()
                        self.resize(10,10)
                        # All buttons are gone, so lets construct the new buttons.
                        self.getallDevs()
                        # The layout should be minimal, so make it unrealistically small (x=10, y=10 [px]) and then resize to minimum.
                        self.setMaximumSize(10,10)
                        #self.resize(self.sizeHint().width(), self.sizeHint().height())
                        self.bottomlabel.setToolTip("Loaded configuration from file: "+nameoffile)
                except:
                    if inp2 == 0:
                        self.bottomlabel.setText("Conf. file error: Missing separator(s).")
            else:
                if inp2 == 0:
                    self.bottomlabel.setText("Not a DynaGUI file - missing identifier.")
            

    def killdynamicbuttongroup(self):
        # Destroy / kill all buttons currently constructed in the buttongroup.
        self.bottomlabel.setText(str("Loading " + str(self.listofbpmattributeslistbox.currentText()) + " statuses..."))
        for i in reversed(range(self.sublayout.count())):
            item = self.sublayout.itemAt(i)
            if isinstance(item, QtGui.QWidgetItem):
                item.widget().close()
        for n in self.buttonGroup.buttons():
            self.buttonGroup.removeButton(n)
        self.sublayout.removeWidget(self.groupBox)
        self.groupBox = QtGui.QGroupBox()
        self.sublayout.addWidget(self.groupBox)
        self.sublayout = QtGui.QGridLayout(self.groupBox)
        
    def getallDevs(self):
        # Construct all necessary buttons
        rowcount = -1
        colcount = 0
        
        # Here the construction begins for all the pushbuttons, and we make them all belong to the groupbox.
        for index in self.devlist:
            rowcount += 1
            button = QtGui.QPushButton(index, self.groupBox)
            textbox = QtGui.QLineEdit("-", self.groupBox)
            textbox.setEnabled(False)
            self.sublayout.addWidget(button,rowcount,colcount,1,1)
            self.sublayout.addWidget(textbox,rowcount,colcount+1,1,1)
            self.groupBox.setStyleSheet("text-align:center")
            if rowcount == self.Nrows - 1:
                rowcount = -1
                colcount += 2
        
        # Here we construct the buttongroup.
        self.buttonGroup = QtGui.QButtonGroup(self)
        self.buttonGroup.buttonClicked.connect(self.handleButtonClicked)
        
        # Here we add all buttons to the buttongroup.
        for button in self.groupBox.findChildren(QtGui.QPushButton):
            if self.buttonGroup.id(button) < 0:
                self.buttonGroup.addButton(button)
                
        # Get the statuses
        self.statuscheck()
        
    def statuscheck(self):
        bval = -1
        self.maxsize = 0
        TaurusList = []
        for item in self.buttonGroup.buttons():
            bval += 1
            try:
                proxy = item.text()
                prox = [PT.DeviceProxy(str(proxy))]
                try:
                    for bd in prox:
                        val = bd.read_attribute(str(self.listofbpmattributeslistbox.currentText())).value
                        item.setStyleSheet('background-color: lime')
                        lineedits = self.groupBox.findChildren(QtGui.QLineEdit)
                        lineedits[bval].setText(str(val))
                        font = lineedits[bval].font()
                        ffont = QtGui.QFont(font)
                        thissize = QtGui.QFontMetrics(ffont).boundingRect(lineedits[bval].text()).width()
                        if thissize > self.maxsize:
                            self.maxsize = thissize
                        TaurusList.append(str(proxy))
                except:
                    item.setStyleSheet('background-color: fuchsia')
                    lval = -1
                    for lineedit in self.groupBox.findChildren(QtGui.QLineEdit):
                        lval += 1
                        if lval == bval:
                            lineedit.setText("-")
            except:
                item.setStyleSheet('QPushButton {background-color: maroon; color: white}')
        self.TaurusList = TaurusList
        
        for lineedit in self.groupBox.findChildren(QtGui.QLineEdit):
            try:
                lineedit.setFixedWidth(self.maxsize+25)
            except:
                lineedit.setFixedWidth(50)
        self.bottomlabel.setText(str(str(self.listofbpmattributeslistbox.currentText()) + " statuses loaded."))
        self.setMaximumSize(10,10)
        self.resize(self.sizeHint().width(), self.sizeHint().height())
    
    def getAllAttsClicked(self):
        dev_ids = []
        valid_devs = []
        valid_attr_names = []
        
        for dev in self.devlist:
            dev_id = dev.split("/")
            dev_id = dev_id[len(dev_id)-1]
            if dev_id not in [str(x) for x in dev_ids]:
                dev_ids.append(dev_id)
                valid_devs.append(dev)
        
        for dev in valid_devs:
            try:
                for devi in [PT.DeviceProxy(dev)]:
                    atts = devi.attribute_list_query()[:]
                    for att in atts:
                        if att.name not in [str(x) for x in valid_attr_names]:
                            valid_attr_names.append(att.name)
            except:
                None
        
        self.listofbpmattributes = valid_attr_names
        self.listofbpmattributeslistbox.clear()
        self.listofbpmattributeslistbox.addItems(self.listofbpmattributes)
        self.setMaximumSize(10,10)
        self.resize(self.sizeHint().width(), self.sizeHint().height())
    
    def plotallin2D(self):
        TaurusList = []
        for attr in self.listofbpmattributes:
            for devs in self.devlist:
                try:
                    prox = [PT.DeviceProxy(str(devs))]
                    for bd in prox:
                        bd.read_attribute(str(attr)).value
                    TaurusList.append(str(devs)+"/"+attr)
                except:
                    pass
        
        if len(TaurusList) < 1:
            self.bottomlabel.setText("No devices found with attribute "+attr+".")
        else:
            print(TaurusList)
            self.toSpecTaurusList = TaurusList
            self.okflag = 0
            prep2D = prep2DGUI(self)
            prep2D.exec_()
            if self.okflag == 1:
                self.specflag = 1
                spectro = Spectrogram(self)
                spectro.show()
                
    def plotin2D(self):
        TaurusList = []
        DevsNames = []
        attr = str(self.listofbpmattributeslistbox.currentText())
        for devs in self.TaurusList:
            TaurusList.append(str(devs)+"/"+attr)
            DevsNames.append(str(devs))
        
        if len(TaurusList) < 1:
            self.bottomlabel.setText("No devices found with attribute "+attr+".")
        else:
            self.toSpecTaurusList = TaurusList
            self.okflag = 0
            prep2D = prep2DGUI(self)
            prep2D.exec_()
            if self.okflag == 1:        
                self.specflag = 0
                spectro = Spectrogram(self)
                spectro.show()
        
    def plotinTaurus(self):
        TaurusList = []
        DevsNames = []
        attr = str(self.listofbpmattributeslistbox.currentText())
        for devs in self.TaurusList:
            TaurusList.append(str(devs)+"/"+attr)
            DevsNames.append(str(devs))
        self.toSpecTaurusList = TaurusList
        self.toSpecDevList = DevsNames
        if len(TaurusList) < 1:
            self.bottomlabel.setText("No devices found with attribute "+attr+".")
        else:
            lt = LaunchTaurus(self)
            lt.setModal(False)
            lt.show()
    
    def handleButtonClicked(self,button):
        for item in self.buttonGroup.buttons():
            if button is item:
                if item.palette().button().color().name() == "#800000":
                    self.bottomlabel.setText("Cannot establish contact with this device.")
                else:
                    proxy = item.text()
                    self.bottomlabel.setText("Launching AtkPanel for "+str(proxy)+".")
                    os.system("atkpanel "+str(proxy) +"  &")
            
    def listbtnclicked(self):
        listGui = listbtnGUI(self)
        listGui.setModal(True)
        listGui.exec_()
        self.listofbpmattributeslistbox.clear()
        self.listofbpmattributeslistbox.addItems(self.listofbpmattributes)
        if self.reloadflag == 1:
            devlist = []
            for n in self.devlist:
                if n not in devlist:
                    devlist.append(n)
            self.devlist = devlist
            self.maxsize = 0
            self.killdynamicbuttongroup()
            self.getallDevs()
            # The layout should be minimal, so make it unrealistically small (x=10, y=10 [px]) and then resize to minimum.
            self.setMaximumSize(10,10)
            self.resize(self.sizeHint().width(), self.sizeHint().height())
            self.reloadflag = 0

class LaunchTaurus(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(LaunchTaurus, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        attr = str(parent.listofbpmattributeslistbox.currentText())
        TaurusList = parent.toSpecTaurusList
        DevsNames = parent.toSpecDevList
        
            
        newTTrend = NewTaurusTrend(TaurusList, DevsNames)
        layout.addWidget(newTTrend)
        self.setLayout(layout)
        self.setWindowTitle("Plotting: "+attr)
        self.resize(parent.size())

class NewTaurusTrend(TaurusTrend):
    def __init__(self,input1,input2):
        TaurusTrend.__init__(self)
        self.setXIsTime(True)
        self.setModel(input1)
        for ind, inp in enumerate(input1):
            inputtxt = inp.lower()
            if inputtxt in self.trendSets:
                self.trendSets[inputtxt].setTitleText(str(input2[ind].lower()))

class listbtnGUI(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(listbtnGUI, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Edit DynaGUI NV")
        listgui = QtGui.QFormLayout(self)
        
        devslbl = QtGui.QLabel("List of devices:")
        self.textboxDevs = QtGui.QPlainTextEdit('\n'.join(parent.devlist))
        
        attrlbl = QtGui.QLabel("List of device attributes:")
        self.textboxAttr = QtGui.QPlainTextEdit('\n'.join(parent.listofbpmattributes))
        
        rowslbl = QtGui.QLabel("Max. number of rows:")
        self.textboxRows = QtGui.QSpinBox()
        self.textboxRows.setValue(parent.Nrows)
        
        okbtn = QtGui.QPushButton('Ok')
        nobtn = QtGui.QPushButton('Cancel')
        listgui.addRow(devslbl)
        listgui.addRow(self.textboxDevs)
        listgui.addRow(attrlbl)
        listgui.addRow(self.textboxAttr)
        listgui.addRow(rowslbl,self.textboxRows)        
        listgui.addRow(okbtn, nobtn)
        okbtn.clicked.connect(self.confirmfunc)
        nobtn.clicked.connect(self.cancelfunc)
        
    def confirmfunc(self):
        textDevs = str(self.textboxDevs.toPlainText())
        self.newlistDevs = textDevs.split()

        if self.parent.devlist != self.newlistDevs:
            self.parent.devlist = self.newlistDevs
            self.parent.reloadflag = 1
        
        textAtts = str(self.textboxAttr.toPlainText())
        self.newlistAtts = textAtts.split()
        self.parent.listofbpmattributes = self.newlistAtts
        
        if self.parent.Nrows != self.textboxRows.value():
            self.parent.Nrows = self.textboxRows.value()
            self.parent.reloadflag = 1
            
        self.close()
    
    def cancelfunc(self):
        self.close()

class Surfogram(QtGui.QDialog): # Maybe do 3D plotting in future?
    def __init__(self, parent = Dialog):
        super(Surfogram, self).__init__(parent)
        pg.opengl.GLSurfacePlotItem

class prep2DGUI(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(prep2DGUI, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Setup 2D spectrogram plotting")
        listgui = QtGui.QFormLayout(self)
        
        
        freqlbl = QtGui.QLabel("Plotting frequency: [Hz]")
        self.textboxF = QtGui.QSpinBox()
        self.textboxF.setValue(parent.toSpecupdateFrequency)
        
        minulbl = QtGui.QLabel("# of minutes in spectrogram: [min]")
        self.textboxM = QtGui.QSpinBox()
        self.textboxM.setValue(parent.toSpecminutes)
        
        okbtn = QtGui.QPushButton('Ok')
        nobtn = QtGui.QPushButton('Cancel')
        listgui.addRow(freqlbl,self.textboxF)   
        listgui.addRow(minulbl,self.textboxM)
        listgui.addRow(okbtn, nobtn)
        okbtn.clicked.connect(self.confirmfunc)
        nobtn.clicked.connect(self.cancelfunc)
        
    def confirmfunc(self):
        self.parent.toSpecminutes = self.textboxM.value()
        self.parent.toSpecupdateFrequency = self.textboxF.value()
        self.parent.okflag = 1
        self.close()
    
    def cancelfunc(self):
        self.parent.okflag = 0
        self.close()
   
class Spectrogram(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(Spectrogram, self).__init__(parent)
        self.parent = parent
        
        self.sensorNames = parent.toSpecTaurusList
        self.minutes = parent.toSpecminutes
        self.updateFrequency = parent.toSpecupdateFrequency
        
        self.w = pg.PlotWidget()
        
        self.hist = pg.HistogramLUTWidget()
        self.img = pg.ImageItem()
        self.hist.setImageItem(self.img)
        
        hBox1 = QtGui.QGridLayout()
        hBox1.addWidget(self.w,0,0,1,4)
        
        self.pausebtn = QtGui.QPushButton("Pause")
        self.pausebtn.clicked.connect(self.pauseclicked)
        hBox1.addWidget(self.pausebtn,1,0,1,1)
        
        plotposbtn = QtGui.QPushButton("Plot Trace")
        plotposbtn.clicked.connect(self.plotTrace)
        hBox1.addWidget(plotposbtn,1,1,1,1)
        
        self.plotvsstoredbtn = QtGui.QPushButton("Plotting real values")
        self.plotvsstoredbtn.clicked.connect(self.plotvsstored)
        hBox1.addWidget(self.plotvsstoredbtn,1,2,1,1)
    
        self.storeposbtn = QtGui.QPushButton("Store current positions")
        self.storeposbtn.clicked.connect(self.updateRefImage)
        hBox1.addWidget(self.storeposbtn,1,3,1,1)
        
        self.editcmbtn = QtGui.QPushButton("Edit CM")
        self.editcmbtn.clicked.connect(self.editcm)
        self.editcmbtn.setToolTip("CM: Colormap colors.\nCM1: Background color. \nCM2: Middle-level color. \nCM3: High-level color.")
        hBox1.addWidget(self.editcmbtn,1,4,1,1)
        
        self.setLayout(hBox1)

        self.w.addItem(self.img)
        hBox1.addWidget(self.hist,0,4,1,1)
        
        if parent.specflag == 0:
            title = self.sensorNames[0].split('/')
            self.title = str(title[len(title)-1])
        else:
            self.title = 'Plotting all'
        
        self.setWindowTitle(self.title)
        
        self.w.setLabel('left',"Device #")
        self.w.setLabel('bottom',"time [min]")
        self.tSize = self.minutes*60*self.updateFrequency
        self.DevsSize = len(self.sensorNames)
        self.plotarr = np.zeros((self.tSize,self.DevsSize))
        x = []
        for minute in range(-self.minutes, self.minutes/10, 2):
            if minute == 0:
                x.append('Now')
            else:
                x.append(format('%s min') % minute)
        xt = [i for i in range(0, self.updateFrequency*(self.minutes+1)*60, self.updateFrequency*2*60)]
        ticks = [list(zip(xt, x))]
        wXAxis = self.w.getAxis('bottom')
        wXAxis.setTicks(ticks)
        pos = np.array([0., 1., 1.])
        
        self.cm1 = [0,0,0,255]
        self.cm2 = [0,255,0,255]
        self.cm3 = [255,0,0,255]
        
        color = np.array([self.cm1,self.cm2,self.cm3],dtype=np.ubyte)
        cmap = pg.ColorMap(pos,color)
        lut = cmap.getLookupTable(0.0,1.0,256)
        self.img.setLookupTable(lut)
        
        self.isoV = pg.InfiniteLine(angle=90, movable=True, pen='y')
        self.w.addItem(self.isoV, ignoreBounds=False)
        self.isoV.setZValue(1000)
        self.isoV.setPos(self.tSize)
        self.isoV.sigPositionChangeFinished.connect(self.moveLine)
        
        self.update()
        
        m1 = self.plotarr.min()
        m2 = self.plotarr.max()
        diff = 1.1
        if m1 > 0:
            m1 = m1 / diff
        else:
            m1 = m1 * diff
        if m2 > 0:
            m2 = m2 * diff
        else:
            m2 = m2 / diff
        
        self.hist.setLevels(m1,m2)
        self.img.setLevels([0,255],[0,255])
        self.img.setLookupTable(lut)
        self.t = QtCore.QTimer()
        self.t.timeout.connect(self.update)
        self.t.start(1000/self.updateFrequency)
    
    def editcm(self):
        items = ("CM1","CM2","CM3")
        item,ok = QtGui.QInputDialog.getItem(self,"Edit CM:s","Select CM #:",items,0,False)
        print(self.cm1)
        if ok and item:
            if item == "CM1":
                self.cm1 = self.getcm(self.cm1,'CM1')
            elif item == "CM2":
                self.cm2 = self.getcm(self.cm2,'CM2')
            elif item == "CM3":
                self.cm3 = self.getcm(self.cm3,'CM3')
        print(self.cm1)
        color = np.array([self.cm1,self.cm2,self.cm3],dtype=np.ubyte)
        pos = np.array([0., 1., 1.])
        cmap = pg.ColorMap(pos,color)
        lut = cmap.getLookupTable(0.0,1.0,256)
        self.img.setLookupTable(lut)
    
    def getcm(self,cmin,cmt):
        cmtxt = []
        for n in cmin:
            cmtxt.append(str(n))
        cmtxt = ','.join(cmtxt)
        text,ok = QtGui.QInputDialog.getText(self,"Edit CM","Define "+cmt+" in alpha-RGB format [int, int, int, int]:",text=cmtxt)
        if ok and text:
            text = text.split(',')
            cm = []
            for n in text:
                cm.append(int(n))
            return cm
        else:
            return cmin
        
    def plotvsstored(self):
        if str(self.plotvsstoredbtn.text()) == 'Plotting vs stored':
            self.plotvsstoredbtn.setText('Plotting real values')
        elif str(self.plotvsstoredbtn.text()) == 'Plotting real values':
            self.plotvsstoredbtn.setText('Plotting vs stored')
        
    def updateRefImage(self):
        self.refarr = self.plotarr[self.tSize-1,:]

    def plotTrace(self): # From JonPet
        fig = plt.figure()
        i = round(float(self.isoV.value()))
        if i == self.tSize:
            i = self.tSize - 1
        if str(self.plotvsstoredbtn.text()) == 'Plotting vs stored':
            arr = (self.plotarr[i,:]) - self.refarr
            title = " (real - stored values)"
            #np.abs( np.abs(self.plotarr) - np.abs(self.refarr))
        elif str(self.plotvsstoredbtn.text()) == 'Plotting real values':
            arr = (self.plotarr[i,:])
            title = " (real values)"
        plt.plot(arr, picker=5)
        plt.title(str(self.title+title))
        fig.canvas.mpl_connect('pick_event', self.onpick)
        plt.show()
        
    def onpick(self, event): # From JonPet
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        
        ind = event.ind
        if len(ind) > 1:
            ind = ind[np.argmax(abs(ydata[ind]))]
        if self.parent.specflag == 0:
            sensname = self.sensorNames[ind].split('/')
            sensname = '  '.join([sensname[0], sensname[2]])
        else:
            sensname = self.sensorNames[ind]
        plt.text(xdata[ind], ydata[ind], sensname, rotation =45, rotation_mode = 'anchor')
        event.canvas.draw()
        
    def moveLine(self): # From JonPet
        """Move the vertical line only to integers"""
        val = round(float(self.isoV.value()))
        if val < 0: 
            self.isoV.setPos(0.0)
        elif val > self.tSize:
            self.isoV.setPos(self.tSize)
            
    def pauseclicked(self):
        if self.pausebtn.text() == 'Pause':
            self.pausebtn.setText("Run")
            self.t.stop()
        elif self.pausebtn.text() == 'Run':
            self.pausebtn.setText("Pause")
            self.t.start()
        
    def update(self):
        self.plotarr = np.roll(self.plotarr, -1, 0)
        y = []
        for ind, inp in enumerate(self.sensorNames):
            attr = inp.split('/')
            attr = str(attr[len(attr)-1])
            prox = [PT.DeviceProxy(str("/".join(inp.split('/')[:-1])))]
            for bd in prox:
                val = bd.read_attribute(attr).value
            y.append(str(val))
            y.append("test "+str(ind))
        self.plotarr[-1:] = y
        if str(self.plotvsstoredbtn.text()) == 'Plotting vs stored':
            try:
                self.img.setImage(np.abs( np.abs(self.plotarr) - np.abs(self.refarr)), autoLevels=False)
            except:
                self.updateRefImage()
                self.img.setImage(np.abs( np.abs(self.plotarr) - np.abs(self.refarr)), autoLevels=False)
        elif str(self.plotvsstoredbtn.text()) == 'Plotting real values':
            self.img.setImage(np.abs(self.plotarr), autoLevels=False)
            
    def closeEvent(self, event):
        self.t.stop()
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
