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
    import PyQt5.QtGui as QtGui2
    from PyQt5 import QtCore
except:
    from PyQt4 import QtCore, QtGui
import os, platform
from datetime import datetime
from functools import partial
from time import sleep
import sys
class Dialog(QtGui.QDialog):
    # This is the class in which the DynaGUI window is constructed
    def __init__(self, inp, ctrl_library):
        # Intialization of start-up parameters and Qt
        QtGui.QDialog.__init__(self)
        self.ctrl_library = ctrl_library
        self.setWindowTitle("DynaGUI Alarms")
        # Input 0 means load with standard pre-defined configurations (no file to load to during start-up)
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
            # List of some sample channels, some samples to load here if no start-up file was defined above
            if self.ctrl_library == "Tango":
                self.devdoms = ['section1/discipline1/device1/temp',
                                'section1/discipline1/device2/press',
                                'section3/discipline1/device1/temp',
                                'section3/discipline2/device1/temp']
                self.devdesc = ['S1 P1 R1 temperature',
                                'S1 P1 R2 pressure',
                                'S3 P1 R1 temperature',
                                'S3 P2 R1 temperature']
                self.devlims = [30,
                                700,
                                22,
                                53]
            elif self.ctrl_library == "EPICS":
                self.devdoms = ['s1:p1-r1:temp',
                                's1:p1-r2:press',
                                's3:p1-r1:temp',
                                's3:p2-r1:temp']
                self.devdesc = ['S1 P1 R1 temperature',
                                'S1 P1 R1 pressure',
                                'S3 P1 R1 temperature',
                                'S3 P2 R1 temperature']
                self.devlims = [30,
                                700,
                                22,
                                53]
            elif self.ctrl_library == "Finance":
                self.devdoms = ['AAPL',
                                'TSLA',
                                'FB',
                                'BAX',
                                'AVGO',
                                'UBER']
                self.devdesc = ['Apple Inc.',
                                'Tesla Inc.',
                                'Facebook INC',
                                'Baxter International Inc.',
                                'Broadcom Inc.',
                                'UBER Technologies Inc.']
                self.devlims = [10,
                                11,
                                12,
                                13,
                                14]
            elif self.ctrl_library == "Randomizer":
                self.devdoms = ['Random Attribute 1',
                                'Random Attribute 2',
                                'Random Attribute 3',
                                'Random Attribute 4',
                                'Random Attribute 5']
                self.devdesc = ['Random Attribute 1 description',
                                'Random Attribute 2 description',
                                'Random Attribute 3 description',
                                'Random Attribute 4 description',
                                'Random Attribute 5 description']
                self.devlims = [10000,
                                1,
                                10,
                                100,
                                1000]
            self.Nrows = 20
        # Reloadflag is used for stating if there are pre-existing control buttons; 1 == rmv them, 0 == nothing to remove which is only during start-up
        self.reloadflag = 0
        self.timerinterval = 30 # seconds
        # Create the layout
        self.createLayout()
        # Run the script for generating the dynamical buttons with the channels defined
        self.getallDevs()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.statuscheck)
    def createLayout(self):
        # Create the layout
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
            self.doublevalidator = QtGui2.QDoubleValidator(-float('inf'),float('inf'),5)
        except:
            self.doublevalidator = QtGui.QDoubleValidator(-float('inf'),float('inf'),5)
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
        self.selectallbtn = QtGui.QPushButton("Select All")
        self.unselectallbtn = QtGui.QPushButton("Unselect All")
        self.loadbtn.clicked.connect(self.loadbtnclicked)
        self.loadbtn.setShortcut("Ctrl+o")
        self.loadbtn.setToolTip("Load a configuration (ctrl+o).")
        self.savebtn.clicked.connect(self.savebtnclicked)
        self.savebtn.setShortcut("Ctrl+s")
        self.savebtn.setToolTip("Save a configuration (ctrl+s).")
        self.selectallbtn.clicked.connect(self.selectallbtnclicked)
        self.unselectallbtn.clicked.connect(self.unselectallbtnclicked)
        self.horizlayout1.addWidget(self.loadbtn)
        self.horizlayout1.addWidget(self.savebtn)
        self.horizlayout1.addWidget(self.selectallbtn)
        self.horizlayout1.addWidget(self.unselectallbtn)
        # Construct the start/stop button for comparing channel values with limits defined
        self.startstopbtn = QtGui.QPushButton("Not running. Press to activate.")
        self.startstopbtn.setStyleSheet('QPushButton {background-color: maroon; color: white}')
        self.startstopbtn.clicked.connect(self.startstopclicked)
        self.toplayout.addWidget(self.startstopbtn)
    def selectallbtnclicked(self):
        # Set all alarms to be checked
        for item in self.groupBox.findChildren(QtGui.QCheckBox):
            item.setChecked(True)
    def unselectallbtnclicked(self):
        # Set all alarms to be unchecked
        for item in self.groupBox.findChildren(QtGui.QCheckBox):
            item.setChecked(False)
    def savebtnclicked(self):
        # Save the DynaGUI configuration
        nameoffile = QtGui.QFileDialog.getSaveFileName(self, 'Save to File', "", "DynaGUI Alarms file (*.dg3)")[0]
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
        # The button was clicked to load a file
        nameoffile = QtGui.QFileDialog.getOpenFileName(self, 'Load File', "", "DynaGUI Alarms file (*.dg3)")[0]
        if not nameoffile:
            self.bottomlabel.setText("Cancelled loading configuration.")
        else:
            self.loadfile(nameoffile,0)
    def loadfile(self,nameoffile,inp2):
        # Load a previously saved configuration
        file = open(nameoffile, 'r')
        splitToLoad = file.read()
        splitToLoad = splitToLoad.split("##IamYourSeparator##")
        identifier = splitToLoad[0].split('\n')
        while("" in identifier): # Get rid of empty strings
            identifier.remove("")
        if identifier[0] == 'IamaDynaGUIalarmFile':
            try:
                if inp2 == 0:
                    # Destroy the current buttons
                    self.killdynamicbuttongroup()
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
                # All buttons are gone, so let's construct the new buttons.
                self.getallDevs()
                # The layout should be minimal, so make it unrealistically small (x=10, y=10 [px]) and then resize to minimum.
                self.resize(10,10)
                self.resize(self.sizeHint().width(), self.sizeHint().height())
                self.bottomlabel.setToolTip("Loaded configuration from file: "+nameoffile)
            except:
                if inp2 == 0:
                    self.bottomlabel.setText("Conf. file error: Missing separator(s).")
        else:
            if inp2 == 0:
                self.bottomlabel.setText("Not a DynaGUI alarm file - missing identifier.")
    def killdynamicbuttongroup(self):
        # Destroy / kill all buttons currently constructed in the buttongroup
        for i in reversed(range(self.sublayout.count())):
            item = self.sublayout.itemAt(i)
            if isinstance(item, QtGui.QWidgetItem):
                item.widget().close()
        for item in self.groupBox.findChildren(QtGui.QLineEdit):
            self.sublayout.removeWidget(item)
            item.deleteLater()
        for item in self.groupBox.findChildren(QtGui.QCheckBox):
            self.sublayout.removeWidget(item)
            item.deleteLater()
        for item in self.groupBox.findChildren(QtGui.QLabel):
            self.sublayout.removeWidget(item)
            item.deleteLater()
    def getallDevs(self):
        # Construct the buttongroup with the widgets for all the channels defined
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
                self.devlims.append(0)
            textbox.setValidator(self.doublevalidator)
            combobox = QtGui.QComboBox(self.groupBox)
            combobox.addItem(">")
            combobox.addItem("<")
            textbox.setEnabled(True)
            textbox.textChanged.connect(partial(self.lineeditedited,textbox))
            label = QtGui.QLabel("-",self.groupBox)
            self.sublayout.addWidget(button,rowcount,colcount,1,1)
            self.sublayout.addWidget(label,rowcount,colcount+1,1,1)
            self.sublayout.addWidget(combobox,rowcount,colcount+2,1,1)
            self.sublayout.addWidget(textbox,rowcount,colcount+3,1,1)
            if rowcount == self.Nrows - 1:
                # Reached maximum number of rows; start a new column and set row to 0
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
    def lineeditedited(self,lineedit):
        # Limit of an alarm has been changed
        n = -1
        # Loop through the lineedit widgets
        for item in self.groupBox.findChildren(QtGui.QLineEdit):
            n += 1
            if lineedit is item:
                # lineedit edited found, update this channel's limit
                self.devlims[n] = item.text()
    def startstopclicked(self):
        # The button to start or stop checking channel values vs limits clicked
        if self.timer.isActive():
            # It is running so stop all
            self.timer.stop()
            self.startstopbtn.setText("Not running. Press to activate.")
            self.startstopbtn.setStyleSheet('QPushButton {background-color: maroon; color: white}')
        else:
            # It is not running so start checking values
            self.alarmflag = 0
            self.statuscheck()
            self.timer.start(self.timerinterval * 1000)
            self.startstopbtn.setText("Running. Press to deactivate.")
            if platform.system() == "Linux":
                self.startstopbtn.setStyleSheet('QPushButton {background-color: lime; color: white}')
            elif platform.system() == "Darwin":
                self.startstopbtn.setStyleSheet('QPushButton {background-color: green; color: white}')
            else:
                self.startstopbtn.setStyleSheet('QPushButton {background-color: lime; color: white}')
    def statuscheck(self):
        # Check the states of all channels vs limits
        checkboxes = self.groupBox.findChildren(QtGui.QCheckBox)
        lineedits = self.groupBox.findChildren(QtGui.QLineEdit)
        labels = self.groupBox.findChildren(QtGui.QLabel)
        combos = self.groupBox.findChildren(QtGui.QComboBox)
        alarmstring = 0
        # Loop through all channels and retrieve their values
        for ind, item in enumerate(checkboxes):
            if self.ctrl_library == "Tango":
                splitt = str(item.toolTip()).split("/")
                attr = splitt[len(splitt)-1]
                proxy = str("/".join(splitt[0:len(splitt)-1]))
            elif self.ctrl_library == "Finance" or self.ctrl_library == "Randomizer" or self.ctrl_library == "EPICS":
                proxy = item.toolTip()
            if self.ctrl_library == "Tango":
                prox = [PT.DeviceProxy(str(proxy))]
                for bd in prox:
                    val = bd.read_attribute(attr).value
            elif self.ctrl_library == "EPICS":
                val = epics.PV(devs, auto_monitor=True).value
            elif self.ctrl_library == "Randomizer":
                val = random.random()
            elif self.ctrl_library == "Finance":
                try:
                    try:
                        val = float(pdr.get_quote_yahoo(proxy)['price'].values.tolist()[0])
                    except:
                        val = float(pdr.get_quote_yahoo(proxy)['preMarketPrice'].values.tolist()[0])
                except:
                    print("failed to retreive data for "+proxy)
                    val = 0
            # Update the value shown for the channel
            labels[ind].setText(str(val))
            if item.isChecked():
                # Limit is to be checked since this channel's checkbox is checked
                # Check if value should be less than or more than the limit
                # If condition is untrue, paint background red and speak that it is in alarm - otherwise make background green
                lorm = str(combos[ind].currentText())
                if lorm == "<":
                    if val > float(lineedits[ind].text()):
                        if alarmstring == 0:
                            alarmstring = str(item.text())
                        else:
                            alarmstring = str(alarmstring + " [[slnc 200]] and [[slnc 200]] " + str(item.text()))
                        self.paintRed(item)
                    else:
                        self.paintGreen(item)
                elif lorm == ">":
                    if val < float(lineedits[ind].text()):
                        if alarmstring == 0:
                            alarmstring = str(item.text())
                        else:
                            alarmstring = str(alarmstring + " [[slnc 200]] and [[slnc 200]] " + str(item.text()))
                        self.paintRed(item)
                    else:
                        self.paintGreen(item)
            else:
                item.setStyleSheet('background-color: grey')
        if alarmstring == 0:
            # There is no active alarms so send message all clear to the log (bottomlabel)
            self.bottomlabel.setText("All clear.")
            self.alarmflag = 0
        else:
            # There is an active alarm so send this message to the log (bottomlabel)
            if self.alarmflag == 0:
                if platform.system() == "Linux":
                    os.system('spd-say "' + str("".join(alarmstring.split("[[slnc 200]]"))) + '[[slnc 200]] in alarm."')
                elif platform.system() == "Darwin":
                    os.system("say -v 'karen' "+ alarmstring + '[[slnc 200]] in alarm.')
                elif platform.system() == "Windows":
                    print("Windows - no voice speaker set up yet")
                self.alarmflag = 1
            self.bottomlabel.setText(str(datetime.now().strftime("%Y-%b-%d_%H%M%S")) + ", " + str("".join(alarmstring.split("[[slnc 200]]")))+" in alarm.")
    def paintGreen(self,item):
        # Paint the background colour green or lime depending on OS
        if platform.system() == "Linux":
            item.setStyleSheet("background-color: lime")
        elif platform.system() == "Darwin":
            item.setStyleSheet("background-color: green")
        else:
            item.setStyleSheet('background-color: lime')
    def paintRed(self,item):
        # Paint the background colour red
        item.setStyleSheet("background-color: red")
    def listbtnclicked(self):
        # Launch the edit DynaGUI window
        listGui = listbtnGUI(self)
        listGui.setModal(True)
        listGui.exec_()
        if self.reloadflag == 1:
            # Remove all channel limit rows
            self.killdynamicbuttongroup()
            # Construct all channel limit rows
            self.getallDevs()
            # The layout should be minimal, so make it unrealistically small (x=10, y=10 [px]) and then resize to minimum.
            self.reloadflag = 0
    def closeEvent(self, event):
        # This stops the timer event
        self.timer.stop()

class listbtnGUI(QtGui.QDialog):
    # This is the class in which the Edit DynaGUI window is constructed
    def __init__(self, parent = Dialog):
        # Initialize the parameters needed for this window
        super(listbtnGUI, self).__init__(parent)
        self.parent = parent
        # Only the widgets which require the parent parameters are constructed here
        self.textboxDevs = QtGui.QPlainTextEdit('\n'.join(parent.devdoms))
        self.textboxDesc = QtGui.QPlainTextEdit('\n'.join(parent.devdesc))
        self.textboxRows = QtGui.QSpinBox()
        self.textboxRows.setValue(parent.Nrows)
        self.textboxTmr = QtGui.QSpinBox()
        self.textboxTmr.setValue(parent.timerinterval)
        # Create the window layout
        self.createLayout()
    def createLayout(self):
        # Create the window layout
        self.setWindowTitle("Edit DynaGUI Alarms")
        listgui = QtGui.QFormLayout(self)
        devslbl = QtGui.QLabel("List of devices' server domains:")
        desclbl = QtGui.QLabel("List of devices' descriptions:")
        rowslbl = QtGui.QLabel("Max. number of rows:")
        tmrlbl = QtGui.QLabel("Alarms timer [s]")
        okbtn = QtGui.QPushButton('Ok')
        nobtn = QtGui.QPushButton('Cancel')
        okbtn.clicked.connect(self.confirmfunc)
        nobtn.clicked.connect(self.cancelfunc)
        listgui.addRow(devslbl,desclbl)
        listgui.addRow(self.textboxDevs,self.textboxDesc)
        listgui.addRow(rowslbl,self.textboxRows)
        listgui.addRow(tmrlbl,self.textboxTmr)
        listgui.addRow(okbtn, nobtn)
        self.resize(self.sizeHint().width(), self.sizeHint().height())
    def confirmfunc(self):
        # All values defined in the edit window are to be sent to the parent as is
        textDevs = str(self.textboxDevs.toPlainText())
        textDescs = str(self.textboxDesc.toPlainText())
        self.newlistDevs = textDevs.split('\n')
        self.newlistDescs = textDescs.split('\n')
        # Check if all devices have domain, description and limits defined: (otherwise don't close)
        if abs(len(self.newlistDevs)-len(self.newlistDescs)) == 0:
            self.parent.timerinterval = self.textboxTmr.value()
            if self.parent.devdoms != self.newlistDevs or self.parent.devdesc != self.newlistDescs:
                self.parent.devdoms = self.newlistDevs
                self.parent.devdesc = self.newlistDescs
                self.parent.reloadflag = 1
            if self.parent.Nrows != self.textboxRows.value():
                self.parent.Nrows = self.textboxRows.value()
                self.parent.reloadflag = 1
            # Then close the window
            self.close()
        else:
            # Number of domains and descriptions do not match, so do not send new values to parent and do not close
            self.parent.reloadflag = 0
            QtGui.QMessageBox.warning(self,"Error","Number of domains and descriptions must be the same.")
    def cancelfunc(self):
        # Just close the window, no values sent back
        self.parent.reloadflag = 1
        self.close()

if __name__ == '__main__':
    # The GUI has been launched, check control library package (argv 1)
    ctrl_library = sys.argv[1]
    # Check if a saved configuration file is defined and if so, load it
    try:
        inp = sys.argv[2]
    except:
        inp = 0
    app = QtGui.QApplication(sys.argv)
    goflag = 1
    if ctrl_library == "Tango":
        import PyTango as PT
    elif ctrl_library == "EPICS":
        print("Not yet implemented.")
        goflag = 0
    elif ctrl_library == "Randomizer":
        import random
    elif ctrl_library == "Finance":
        import pandas_datareader as pdr
    else:
        goflag = 0
    # All seems to be fine so start the GUI
    if goflag == 1:
        window = Dialog(inp,ctrl_library)
        window.show()
        sys.exit(app.exec_())
