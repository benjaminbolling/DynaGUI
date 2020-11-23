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
# Import PyQt5 or PyQt4
try:
    import PyQt5.QtWidgets as QtGui
    from PyQt5 import QtCore
except:
    from PyQt4 import QtCore, QtGui


class Dialog(QtGui.QDialog):
    """This is the class in which the DynaGUI window is constructed."""
    def __init__(self, inp, ctrl_library):
        """Intialization of start-up parameters and Qt."""
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("DynaGUI TF")
        self.ctrl_library = ctrl_library
        # Input 0 means load with standard pre-defined configurations (no file to load to during start-up)
        if inp == 0:
            loadflag = 0
        else:
            try:
                self.loadfile(inp,1) # 1 means that a file is being loaded before anything was constructed (load on start)
                self.Nrows
                loadflag = 1
            except:
                loadflag = 0
        if loadflag == 0:
            # All channel attributes (which can be 0/1) needed, used for initialization during start-up
            self.listofattributes = ['Attribute1',
                                   'Attribute2',
                                   'Attribute3']
            # Some list of channels, used for initialization during start-up
            self.devlist = ['section1/discipline1/device1',
                            'section1/discipline1/device2',
                            'section3/discipline1/device1',
                            'section3/discipline2/device1']
            self.Nrows = 20
        # Show or hide enable/disable all btn
        self.showallhideflag = False
        if ctrl_library == "Randomizer":
            self.devstat = []
            for m in range(len(self.devlist)):
                self.devstat.append(1)
        # Create the layout of the GUI
        self.createLayout()
        # Run the script for generating the dynamical buttons
        self.getallDevs()
    def createLayout(self):
        """Create the layout of the widget."""
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
    def savebtnclicked(self):
        """Save the current configuration to a file."""
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
        """The button was clicked to load a file."""
        nameoffile = QtGui.QFileDialog.getOpenFileName(self, 'Load File', "", "DynaGUI TF files (*.dg1)")[0]
        if not nameoffile:
            self.bottomlabel.setText("Cancelled loading configuration.")
        else:
            self.loadfile(nameoffile,0) # 0 means that there is data to be replaced
    def loadfile(self,nameoffile,inp2):
        """Load a previously saved configuration."""
        file = open(nameoffile, 'r')
        splitToLoad = file.read()
        splitToLoad = splitToLoad.split("##IamYourSeparator##")
        identifier = splitToLoad[0].split('\n')
        while("" in identifier): # Get rid of empty strings
            identifier.remove("")
        if identifier[0] == 'IamaDynaGUIfile':
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
                # Destroy the current buttons since inp2 is 0
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
                self.bottomlabel.setToolTip("Loaded configuration from file: "+nameoffile)
            except:
                if inp2 == 0:
                    self.bottomlabel.setText("Conf. file error: Missing separator(s).")
        else:
            if inp2 == 0:
                self.bottomlabel.setText("Not a DynaGUI file - missing identifier.")
    def enableallbuttonclicked(self):
        """Set the attribute selected to true for all channels."""
        if ctrl_library == "Randomizer":
            self.devstat.clear()
        for item in self.buttonGroup.buttons():
            proxy = item.text()
            if self.ctrl_library == "Tango":
                prox=[PT.DeviceProxy(str(proxy))]
                # Get the states of all channels, one at a time
                for dev in prox:
                    try:
                        val = dev.read_attribute(str(self.listofattributeslistbox.currentText())).value
                        # Try to write to the channel
                        if val is False: # If false, interlock is disabled.
                            dev.write_attribute(str(self.listofattributeslistbox.currentText()),True)
                    except:
                        item.setStyleSheet('background-color: fuchsia')
            elif ctrl_library == "Randomizer":
                self.devstat.append(1)
        self.statuscheck()
    def killdynamicbuttongroup(self):
        """Destroy / kill all buttons currently constructed in the buttongroup."""
        self.bottomlabel.setText(str("Loading " + str(self.listofattributeslistbox.currentText()) + " statuses..."))
        for i in reversed(range(self.sublayout.count())):
            item = self.sublayout.itemAt(i)
            if isinstance(item, QtGui.QWidgetItem):
                item.widget().close()
        for button in self.groupBox.findChildren(QtGui.QPushButton):
            button.deleteLater()
    def getallDevs(self):
        """Construct all necessary buttons."""
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
                # Reached maximum number of rows; start a new column and set row to 0
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
        """Check status of the attribute for all channels."""
        if ctrl_library == "Randomizer":
            n = -1
        # Loop through all control buttons
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
        """A control button has been clicked, input is the id of the button clicked."""
        if ctrl_library == "Randomizer":
            n = -1
        # Begin by looping through all buttons
        for item in self.buttonGroup.buttons():
            if ctrl_library == "Randomizer":
                n += 1
            # The button id has been found in the button group
            if button is item:
                # The text of the item is the channel's channel
                proxy = item.text()
                # Change the value from false to true or true to false for the different control libraries and then update the statuses and colours
                if self.ctrl_library == "Tango":
                    prox=[PT.DeviceProxy(str(proxy))]
                    for dev in prox:
                        try:
                            val = dev.read_attribute(str(self.listofattributeslistbox.currentText())).value
                            if val is True: # If true --> Interlock is enabled.
                                dev.write_attribute(str(self.listofattributeslistbox.currentText()),False)
                            if val is False: # If true --> Interlock is disabled.
                                dev.write_attribute(str(self.listofattributeslistbox.currentText()),True)
                            # wait 0.5 seconds so the signal is sent and retrieved before reading the channel's status again
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
        """Launch the edit DynaGUI window."""
        listGui = listbtnGUI(self)
        listGui.setModal(True)
        listGui.exec_()
        # The listbox with current attributes must be cleared and then populated with the new items
        self.listofattributeslistbox.clear()
        self.listofattributeslistbox.addItems(self.listofattributes)
        if self.showallhideflag is True:
            self.enableallbutton.show()
        elif self.showallhideflag is False:
            self.enableallbutton.hide()
        # Remove all control buttons
        self.killdynamicbuttongroup()
        # Construct all control buttons
        self.getallDevs()
        # The layout should be minimal, so make it unrealistically small (x=10, y=10 [px]) and then resize to minimum.
        self.setMaximumSize(10,10)
        self.resize(self.sizeHint().width(), self.sizeHint().height())

class listbtnGUI(QtGui.QDialog):
    """This is the class in which the Edit DynaGUI window is constructed."""
    def __init__(self, parent = Dialog):
        """Initialize the parameters needed for this window."""
        super(listbtnGUI, self).__init__(parent)
        self.parent = parent
        # Only the widgets which require the parent parameters are constructed here
        self.textboxDevs = QtGui.QPlainTextEdit('\n'.join(parent.devlist))
        self.textboxAttr = QtGui.QPlainTextEdit('\n'.join(parent.listofattributes))
        self.textboxRows = QtGui.QSpinBox()
        self.textboxRows.setValue(parent.Nrows)
        self.showhideenableallbtn = QtGui.QCheckBox("Show the 'Enable All' button")
        self.showhideenableallbtn.setChecked(parent.showallhideflag)
        # Create the window layout
        self.createLayout()
    def createLayout(self):
        """Create the window layout."""
        self.setWindowTitle("Edit DynaGUI TF")
        listgui = QtGui.QFormLayout(self)
        devslbl = QtGui.QLabel("List of channels:")
        attrlbl = QtGui.QLabel("List of channel attributes:")
        rowslbl = QtGui.QLabel("Max. number of rows:")
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
        """All values defined in the edit window are sent to the parent as is."""
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
        # Then close the window
        self.close()
    def cancelfunc(self):
        """Just close the window, no values sent back to parent."""
        self.parent.reloadflag = 0
        self.close()

if __name__ == '__main__':
    """Import of all essential packages."""
    import time, sys, platform
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
    else:
        goflag = 0
    # All seems to be fine so start the GUI
    if goflag == 1:
        window = Dialog(inp,ctrl_library)
        window.show()
        sys.exit(app.exec_())
