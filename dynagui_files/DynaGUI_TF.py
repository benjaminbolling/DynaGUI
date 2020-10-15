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
import time, sys, platform

class Dialog(QtGui.QDialog):
    def __init__(self, inp, ctrl_library):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("DynaGUI TF")
        self.ctrl_library = ctrl_library
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
            self.listofattributes = ['Attribute1',
                                   'Attribute2',
                                   'Attribute3']

            # Some list of devices
            self.devlist = ['section1/discipline1/device1',
                            'section1/discipline1/device2',
                            'section3/discipline1/device1',
                            'section3/discipline2/device1']
            self.Nrows = 20
        self.reloadflag = 0
        self.showallhideflag = False

        if ctrl_library == "Randomizer":
            self.devstat = []
            for m in range(len(self.devlist)):
                self.devstat.append(1)

        # Construct the toplayout and make it stretchable
        self.toplayout = QtGui.QVBoxLayout(self)
        self.toplayout.addStretch()

        # Construct the combobox for the list of attributes
        self.listofattributeslistbox = QtGui.QComboBox(self)
        self.listofattributeslistbox.addItems(self.listofattributes)
        self.listofattributeslistbox.currentIndexChanged.connect(self.statuscheck)
        self.toplayout.addWidget(self.listofattributeslistbox)

        # Here we add a button that sets the selected attribute as TRUE for all the BPM:s in the selected ring
        self.enableallbutton = QtGui.QPushButton("Enable all")
        self.enableallbutton.clicked.connect(self.enableallbuttonclicked)
        self.enableallbutton.hide()

        # Construct the button for setting up a dynamic list of attributes
        self.listbtn = QtGui.QPushButton("Edit DynaGUI")
        self.listbtn.clicked.connect(self.listbtnclicked)
        self.listbtn.setEnabled(True)
        self.toplayout.addWidget(self.listbtn)

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
        self.horizlayout = QtGui.QHBoxLayout(self.loadsavewdg)

        # Construct the load and save buttons, connect them to their functions and add them to their horizontal container
        self.loadbtn = QtGui.QPushButton("Load")
        self.savebtn = QtGui.QPushButton("Save")
        self.loadbtn.clicked.connect(self.loadbtnclicked)
        self.loadbtn.setShortcut("Ctrl+o")
        self.loadbtn.setToolTip("Load a configuration (ctrl+o).")
        self.savebtn.clicked.connect(self.savebtnclicked)
        self.savebtn.setShortcut("Ctrl+s")
        self.savebtn.setToolTip("Save a configuration (ctrl+s).")
        self.horizlayout.addWidget(self.loadbtn)
        self.horizlayout.addWidget(self.savebtn)

        # Now we create a button to update the status selected in the combobox for all the dynamically constructed buttons
        self.updatebutton = QtGui.QPushButton("Update statuses")
        self.updatebutton.clicked.connect(self.statuscheck)
        self.toplayout.addWidget(self.updatebutton)
        self.toplayout.addWidget(self.enableallbutton)

        # Run the script for generating the dynamical buttons
        self.getallDevs()

    def savebtnclicked(self):
        nameoffile = QtGui.QFileDialog.getSaveFileName(self, 'Save to File', "", "DynaGUI TF files (*.dg1)")[0]
        if not nameoffile:
            self.bottomlabel.setText("Cancelled save configuration.")
        else:
            file = open(nameoffile, 'w')
            self.toSave = str('IamaDynaGUIfile' + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.devlist) + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.listofattributes) + '\n' + "##IamYourSeparator##\n" + str(self.Nrows))
            file.write(self.toSave)
            file.close()
            self.bottomlabel.setText("Configuration saved to file.")
            self.bottomlabel.setToolTip("Saved configuation to file: "+nameoffile)

    def loadbtnclicked(self):
        nameoffile = QtGui.QFileDialog.getOpenFileName(self, 'Load File', "", "DynaGUI TF files (*.dg1)")[0]
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
            if identifier[0] == 'IamaDynaGUIfile':
                print("Identified as a DynaGUI file.")
                try:
                    devlist = splitToLoad[1].split("\n")
                    while("" in devlist): # Get rid of empty strings
                        devlist.remove("")
                    listofattributes = splitToLoad[2].split("\n")
                    while("" in listofattributes): # Get rid of empty strings
                        listofattributes.remove("")
                    Nrows = splitToLoad[3].split("\n")[1]
                    self.devlist = devlist
                    self.listofattributes = listofattributes
                    self.Nrows = float(Nrows)
                    # Destroy the current buttons.
                    if inp2 == 0:
                        self.listofattributeslistbox.clear()
                        self.listofattributeslistbox.addItems(self.listofattributes)
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

    def enableallbuttonclicked(self):
        if ctrl_library == "Randomizer":
            self.devstat.clear()
        for item in self.buttonGroup.buttons():
            proxy = item.text()
            if self.ctrl_library == "Tango":
                prox=[PT.DeviceProxy(str(proxy))]
                # Get the states of all devices, one at a time (val)
                for dev in prox:
                    try:
                        val = dev.read_attribute(str(self.listofattributeslistbox.currentText())).value
                        # Try to write to the device
                        if val is False: # If false, interlock is disabled.
                            dev.write_attribute(str(self.listofattributeslistbox.currentText()),True)
                    except:
                        item.setStyleSheet('background-color: fuchsia')
            elif ctrl_library == "Randomizer":
                self.devstat.append(1)
        self.statuscheck()

    def killdynamicbuttongroup(self):
        # Destroy / kill all buttons currently constructed in the buttongroup.
        self.bottomlabel.setText(str("Loading " + str(self.listofattributeslistbox.currentText()) + " statuses..."))
        for i in reversed(range(self.sublayout.count())):
            item = self.sublayout.itemAt(i)
            if isinstance(item, QtGui.QWidgetItem):
                item.widget().close()
        for button in self.groupBox.findChildren(QtGui.QPushButton):
            button.deleteLater()

    def getallDevs(self):
        # Construct all necessary buttons
        self.BPMproxies = self.devlist

        rowcount = -1
        colcount = 0

        self.devstat = []
        for m in range(len(self.devlist)):
            self.devstat.append(1)

        # Here the construction begins for all the pushbuttons, and we make them all belong to the groupbox.
        for index in self.BPMproxies:
            rowcount += 1
            button = QtGui.QPushButton(index, self.groupBox)
            self.sublayout.addWidget(button,rowcount,colcount,1,1)
            self.groupBox.setStyleSheet("text-align:center")
            if rowcount == self.Nrows - 1:
                rowcount = -1
                colcount += 1

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
        if ctrl_library == "Randomizer":
            n = -1
        for item in self.buttonGroup.buttons():
            try:
                proxy = item.text()
                if self.ctrl_library == "Tango":
                    prox = [PT.DeviceProxy(str(proxy))]
                    try:
                        for bd in prox:
                            val = bd.read_attribute(str(self.listofattributeslistbox.currentText())).value
                            if val is True:
                                if platform.system() == "Linux":
                                    item.setStyleSheet('background-color: lime')
                                elif platform.system() == "Darwin":
                                    item.setStyleSheet('background-color: green')
                                else:
                                    item.setStyleSheet('background-color: lime')
                            elif val is False:
                                item.setStyleSheet('background-color: red')
                    except:
                        item.setStyleSheet('background-color: fuchsia')
                elif ctrl_library == "Randomizer":
                    n += 1
                    print(n)
                    print(self.devstat)
                    if self.devstat[n] == 1:
                        if platform.system() == "Linux":
                            item.setStyleSheet('background-color: lime')
                        elif platform.system() == "Darwin":
                            item.setStyleSheet('background-color: green')
                        else:
                            item.setStyleSheet('background-color: lime')
                    elif self.devstat[n] == 0:
                        item.setStyleSheet('background-color: red')
            except:
                item.setStyleSheet('QPushButton {background-color: maroon; color: white}')
        self.bottomlabel.setText(str(str(self.listofattributeslistbox.currentText()) + " statuses loaded."))

    def handleButtonClicked(self,button):
        if ctrl_library == "Randomizer":
            n = -1
        for item in self.buttonGroup.buttons():
            if ctrl_library == "Randomizer":
                n += 1
            if button is item:
                proxy = item.text()
                if self.ctrl_library == "Tango":
                    prox=[PT.DeviceProxy(str(proxy))]
                    for dev in prox:
                        try:
                            val = dev.read_attribute(str(self.listofattributeslistbox.currentText())).value
                            if val is True: # If true --> Interlock is enabled.
                                dev.write_attribute(str(self.listofattributeslistbox.currentText()),False)
                            if val is False: # If true --> Interlock is disabled.
                                dev.write_attribute(str(self.listofattributeslistbox.currentText()),True)
                            time.sleep(0.5)
                            val2 = dev.read_attribute(str(self.listofattributeslistbox.currentText())).value
                            if val2 is True:
                                if platform.system() == "Linux":
                                    item.setStyleSheet('background-color: lime')
                                elif platform.system() == "Darwin":
                                    item.setStyleSheet('background-color: green')
                                else:
                                    item.setStyleSheet('background-color: lime')
                            elif val2 is False:
                                item.setStyleSheet('background-color: red')
                        except:
                            item.setStyleSheet('background-color: fuchsia')
                elif ctrl_library == "Randomizer":
                    if self.devstat[n] == 1:
                        self.devstat[n] = 0
                        item.setStyleSheet('background-color: red')
                    elif self.devstat[n] == 0:
                        self.devstat[n] = 1
                        if platform.system() == "Linux":
                            item.setStyleSheet('background-color: lime')
                        elif platform.system() == "Darwin":
                            item.setStyleSheet('background-color: green')
                        else:
                            item.setStyleSheet('background-color: lime')

    def listbtnclicked(self):
        listGui = listbtnGUI(self)
        listGui.setModal(True)
        listGui.exec_()
        self.listofattributeslistbox.clear()
        self.listofattributeslistbox.addItems(self.listofattributes)
        if self.showallhideflag is True:
            self.enableallbutton.show()
        elif self.showallhideflag is False:
            self.enableallbutton.hide()

        if self.reloadflag == 1:
            print("Reload")
            self.killdynamicbuttongroup()
            self.getallDevs()
            self.reloadflag = 2

        if self.reloadflag == 2:
            # The layout should be minimal, so make it unrealistically small (x=10, y=10 [px]) and then resize to minimum.
            self.setMaximumSize(10,10)
            self.resize(self.sizeHint().width(), self.sizeHint().height())
            self.reloadflag = 0

class listbtnGUI(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(listbtnGUI, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Edit DynaGUI TF")
        listgui = QtGui.QFormLayout(self)

        devslbl = QtGui.QLabel("List of devices::")
        self.textboxDevs = QtGui.QPlainTextEdit('\n'.join(parent.devlist))

        attrlbl = QtGui.QLabel("List of device attributes:")
        self.textboxAttr = QtGui.QPlainTextEdit('\n'.join(parent.listofattributes))

        rowslbl = QtGui.QLabel("Max. number of rows:")
        self.textboxRows = QtGui.QSpinBox()
        self.textboxRows.setValue(parent.Nrows)

        self.showhideenableallbtn = QtGui.QCheckBox("Show the 'Enable All' button")
        self.showhideenableallbtn.setChecked(parent.showallhideflag)

        okbtn = QtGui.QPushButton('Ok')
        nobtn = QtGui.QPushButton('Cancel')
        listgui.addRow(devslbl)
        listgui.addRow(self.textboxDevs)
        listgui.addRow(attrlbl)
        listgui.addRow(self.textboxAttr)
        listgui.addRow(rowslbl,self.textboxRows)
        listgui.addRow(self.showhideenableallbtn)
        listgui.addRow(okbtn, nobtn)
        okbtn.clicked.connect(self.confirmfunc)
        nobtn.clicked.connect(self.cancelfunc)

    def confirmfunc(self):
        textDevs = str(self.textboxDevs.toPlainText())
        self.newlistDevs = textDevs.split()

        if self.parent.showallhideflag != self.showhideenableallbtn.isChecked():
            self.parent.showallhideflag = self.showhideenableallbtn.isChecked()
            self.parent.reloadflag = 2

        if self.parent.devlist != self.newlistDevs:
            self.parent.devlist = self.newlistDevs
            self.parent.reloadflag = 1

        textAtts = str(self.textboxAttr.toPlainText())
        self.newlistAtts = textAtts.split()
        self.parent.listofattributes = self.newlistAtts

        if self.parent.Nrows != self.textboxRows.value():
            self.parent.Nrows = self.textboxRows.value()
            self.parent.reloadflag = 1

        self.close()

    def cancelfunc(self):
        self.close()

if __name__ == '__main__':
    try:
        ctrl_library = sys.argv[1]
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
    else:
        goflag = 0
    if goflag == 1:
        window = Dialog(inp,ctrl_library)
        window.show()
        sys.exit(app.exec_())
