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
try:
    import PyQt5.QtWidgets as QtGui
    import PyQt5.QtGui as QtGui2
    from PyQt5 import QtCore
except:
    from PyQt4 import QtCore, QtGui

class Dialog(QtGui.QWidget):
    def __init__(self, inp, ctrl_library):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("DynaGUI NV - "+str(ctrl_library))
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
            if self.ctrl_library == "Tango": # Some MAX IV Laboratory devices and attributes
                self.devlist = ['r3-319s2/dia/dcct-01',
                                'r1-101s/dia/dcct-01',
                                'r1-108/dia/bpm-02',
                                'r1-109/dia/bpm-01',
                                'r3-a110811cab14/dia/bbbz-01',
                                'b105a/dia/bsmon-01'
                                ]
                self.listofbpmattributes = ['lifetime',
                                            'xpossa',
                                            'State',
                                            'SRAM_MD_MODES',
                                            'SRAM_RMS'
                                            ]
            elif self.ctrl_library == "EPICS": # Some ESS PV:s
                self.PV_list = ['LAB:AMC-002-4:I1-YP-TR1-ArrayData',
                                #'LAB:AMC-002-4:I1-YP-AvgValue',
                                #'LAB:AMC-002-4:I2-YP-AvgValue',
                                #'LEBT-010:PwrC-SolPS-01:CurR',
                                #'LEBT-010:PwrC-SolPS-02:CurR'
                                ]
                self.PV_descriptions = ['LAB wave 1',
                                        #'LAB scalar 1',
                                        #'LAB scalar 2',
                                        #'LEBT_Sol-01_Current',
                                        #'LEBT_Sol-02_Current'
                                        ]
            elif ctrl_library == "Finance":
                self.stocknames = ['AAPL',
                                   'TSLA',
                                   'FB',
                                   'BAX',
                                   'AVGO',
                                   'UBER']
            elif ctrl_library == "Randomizer":
                self.devlist = []
                for m in range(0,35):
                    self.devlist.append(str("Random_device_"+str(m)))
                self.listofbpmattributes = []
                for m in range(0,8):
                    self.listofbpmattributes.append(str("Random_attribute_"+str(m)))
            elif ctrl_library == "HistoricalData":
                self.devlist = ["Define",
                                "your",
                                "Devices'",
                                "Names",
                                "Here",
                                "Separated",
                                "by",
                                "Rows"]
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
        if self.ctrl_library == "Tango":
            self.listofbpmattributeslistbox = QtGui.QComboBox(self)
            self.listofbpmattributeslistbox.addItems(self.listofbpmattributes)
            self.listofbpmattributeslistbox.currentIndexChanged.connect(self.statuscheck)
            self.toplayout.addWidget(self.listofbpmattributeslistbox)
        elif self.ctrl_library == "Randomizer":
            self.listofbpmattributeslistbox = QtGui.QComboBox(self)
            self.listofbpmattributeslistbox.addItems(self.listofbpmattributes)
            self.listofbpmattributeslistbox.currentIndexChanged.connect(self.statuscheck)
            self.toplayout.addWidget(self.listofbpmattributeslistbox)
        # elif self.ctrl_library == "EPICS": DO NOT add, EPICS uses PV:s and not devices with attributes
        # elif self.ctrl_library == "Finance": DO NOT add, makes no sense.
        # elif self.ctrl_library == "HistoricalData": DO NOT add, makes no sense.

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
        if self.ctrl_library == "Tango":
            self.horizlayout0.addWidget(self.getAllAttsBtn)
        elif ctrl_library == "Randomizer":
            self.horizlayout0.addWidget(self.getAllAttsBtn)
        # elif self.ctrl_library == "EPICS" or "Finance" or "HistoricalData": DO NOT add, EPICS uses PV:s and not devices with attributes

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
        self.plot1Dbutton.clicked.connect(self.plotin1D)
        self.horizlayout2.addWidget(self.plot1Dbutton)

        # Now we create a button to plot the selected attribute for the available devices for which this is a valid attribute
        self.plot2Dbutton = QtGui.QPushButton("2D Plot")
        self.plot2Dbutton.clicked.connect(self.plotin2D)
        self.horizlayout2.addWidget(self.plot2Dbutton)
        self.wildcardsbtn = QtGui.QPushButton("Import Devices using WildCards")
        if self.ctrl_library != "Tango":
            self.wildcardsbtn.setEnabled(False)
            self.wildcardsbtn.setToolTip("Currently available for: Tango")
        elif self.ctrl_library == "Finance":
            self.plot2Dbutton.setEnabled(False)
            self.plot2Dbutton.setToolTip("Will be available in a future release.")
        self.wildcardsbtn.clicked.connect(self.wildcardsImportClicked)
        self.horizlayout2.addWidget(self.wildcardsbtn)

        # Run the script for generating the dynamical buttons
        self.getallDevs()

    def savebtnclicked(self):
        # To save the configuration
        yesorno, nameoffile = QtGui.QFileDialog.getSaveFileName(self, 'Save to File')
        if not nameoffile:
            self.bottomlabel.setText("Cancelled save configuration.")
        else:
            file = open(nameoffile, 'w')
            if self.ctrl_library == "Tango":
                self.toSave = str('IamaDynaGUIfile' + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.devlist) + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.listofbpmattributes) + '\n' + "##IamYourSeparator##\n" + str(self.Nrows))
            elif self.ctrl_library == "EPICS":
                self.toSave = str('IamaDynaGUIfile' + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.PV_list) + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.PV_descriptions) + '\n' + "##IamYourSeparator##\n" + str(self.Nrows))
            elif self.ctrl_library == "Finance":
                self.toSave = str('IamaDynaGUIfile' + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.stocknames) + '\n' + "##IamYourSeparator##\n" + str(self.Nrows))
            elif self.ctrl_library == "HistoricalData":
                self.toSave = str('IamaDynaGUIfile' + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.devlist) + '\n' + "##IamYourSeparator##\n" + str(self.Nrows))
            elif ctrl_library == "Randomizer":
                self.toSave = str('IamaDynaGUIfile' + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.devlist) + '\n' + "##IamYourSeparator##\n" + '\n'.join(self.listofbpmattributes) + '\n' + "##IamYourSeparator##\n" + str(self.Nrows))
            file.write(self.toSave)
            file.close()
            self.bottomlabel.setText("Configuration saved to file.")
            self.bottomlabel.setToolTip("Saved configuation to file: "+nameoffile)

    def loadbtnclicked(self):
        # File loading initialization
        nameoffile = QtGui.QFileDialog.getOpenFileName(self, 'Load File')
        if not nameoffile:
            self.bottomlabel.setText("Cancelled loading configuration.")
        else:
            self.loadfile(nameoffile,0)

    def loadfile(self,nameoffile,inp2):
        # The actual loading of the file
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
                listofbpmattributes = splitToLoad[2].split("\n")
                while("" in listofbpmattributes): # Get rid of empty strings
                    listofbpmattributes.remove("")
                Nrows = splitToLoad[3].split("\n")[1]
                if self.ctrl_library == "Tango":
                    self.devlist = devlist
                    self.listofbpmattributes = listofbpmattributes
                elif ctrl_library == "Randomizer":
                    self.devlist = devlist
                    self.listofbpmattributes = listofbpmattributes
                elif self.ctrl_library == "EPICS":
                    self.PV_list = devlist
                    self.PV_descriptions = listofbpmattributes
                elif self.ctrl_library == "Finance":
                    self.stocknames = devlist
                elif self.ctrl_library == "HistoricalData":
                    self.stocknames = devlist
                self.Nrows = float(Nrows)
                # Destroy the current buttons / configuration
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
        # Destroy all buttons currently constructed in the buttongroup.
        if self.ctrl_library == "EPICS":
            self.bottomlabel.setText(str("Loading defined PV statuses..."))
        elif self.ctrl_library == "Finance":
            self.bottomlabel.setText("Loading stocks...")
        else:
            self.bottomlabel.setText(str("Loading " + str(self.listofbpmattributeslistbox.currentText()) + " statuses..."))
        for i in reversed(range(self.sublayout.count())):
            item = self.sublayout.itemAt(i)
            if isinstance(item, QtGui.QWidgetItem):
                item.widget().close()
        for n in self.buttonGroup.buttons():
            self.buttonGroup.removeButton(n)
        for lineedit in self.groupBox.findChildren(QtGui.QLineEdit):
            lineedit.deleteLater()
        for button in self.groupBox.findChildren(QtGui.QPushButton):
            button.deleteLater()

    def getallDevs(self):
        # Construct all necessary buttons
        rowcount = -1
        colcount = 0

        # Here the construction begins for all the pushbuttons, and we make them all belong to the groupbox.
        if self.ctrl_library == "Tango":
            alldevs = self.devlist
        elif self.ctrl_library == "Randomizer":
            alldevs = self.devlist
        elif self.ctrl_library == "EPICS":
            alldevs = self.PV_list
        elif self.ctrl_library == "Finance":
            alldevs = self.stocknames
        elif self.ctrl_library == "HistoricalData":
            alldevs = self.devlist

        for n,index in enumerate(alldevs):
            rowcount += 1
            if self.ctrl_library == "Tango":
                button = QtGui.QPushButton(str(self.devlist[n]), self.groupBox)
            elif ctrl_library == "Randomizer":
                button = QtGui.QPushButton(str(self.devlist[n]), self.groupBox)
            elif self.ctrl_library == "EPICS":
                button = QtGui.QPushButton(str(self.PV_descriptions[n]), self.groupBox)
                button.setToolTip(index)
            elif self.ctrl_library == "Finance":
                button = QtGui.QPushButton(str(self.stocknames[n]), self.groupBox)
            elif self.ctrl_library == "HistoricalData":
                button = QtGui.QPushButton(str(self.devlist[n]), self.groupBox)
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
        # Get status of all devices in the list ; depends on controlsystem
        self.maxsize = 0
        TaurusList = []
        for bval,item in enumerate(self.buttonGroup.buttons()):
            try:
                if self.ctrl_library == "EPICS":
                    proxy = self.PV_list[bval]
                else:
                    proxy = item.text()
                if self.ctrl_library == "Tango":
                    prox = [PT.DeviceProxy(str(proxy))]
                    try:
                        for bd in prox:
                            val = bd.read_attribute(str(self.listofbpmattributeslistbox.currentText())).value
                            if platform.system() == "Linux":
                                item.setStyleSheet('background-color: lime')
                            elif platform.system() == "Darwin":
                                item.setStyleSheet('background-color: green')
                            else:
                                item.setStyleSheet('background-color: lime')
                            lineedits = self.groupBox.findChildren(QtGui.QLineEdit)
                            if hasattr(val, "__len__"):
                                val = 'nscalar, len = '+str(len(val))
                            else:
                                val = "{0:.4f}".format(val)
                            lineedits[bval].setText(str(val))
                            font = lineedits[bval].font()
                            try:
                                ffont = QtGui2.QFont(font)
                                thissize = QtGui2.QFontMetrics(ffont).boundingRect(lineedits[bval].text()).width()
                            except:
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
                elif self.ctrl_library == "EPICS":
                    PV = epics.PV(proxy, auto_monitor=True)
                    state = PV.status # Connected => 1
                    if state == 0:
                        try:
                            val = PV.value
                            try:
                                if val != 0:
                                    state = 1
                            except:
                                None
                            if state == 0:
                                try:
                                    if len(val) > 1:
                                        state = 1
                                except:
                                    None
                        except:
                            None
                    if state == 1:
                        if platform.system() == "Linux":
                            item.setStyleSheet('background-color: lime')
                        elif platform.system() == "Darwin":
                            item.setStyleSheet('background-color: green')
                        else:
                            item.setStyleSheet('background-color: lime')
                        count = PV.count
                        lineedits = self.groupBox.findChildren(QtGui.QLineEdit)
                        if isinstance(count, int):
                            if count == 1:
                                val = PV.value
                            elif count > 1:
                                val = 'nscalar, len = '+str(count)
                            TaurusList.append(str(proxy))
                        else:
                            val = 'no value...'
                        lineedits[bval].setText(str(val))
                        font = lineedits[bval].font()
                        try:
                            ffont = QtGui2.QFont(font)
                            thissize = QtGui2.QFontMetrics(ffont).boundingRect(lineedits[bval].text()).width()
                        except:
                            ffont = QtGui.QFont(font)
                            thissize = QtGui.QFontMetrics(ffont).boundingRect(lineedits[bval].text()).width()
                        if thissize > self.maxsize:
                            self.maxsize = thissize
                    else:
                        item.setStyleSheet('QPushButton {background-color: maroon; color: white}')
                        lval = -1
                        for lineedit in self.groupBox.findChildren(QtGui.QLineEdit):
                            lval += 1
                            if lval == bval:
                                lineedit.setText("-")
                elif self.ctrl_library == "Finance":
                    try:
                        try:
                            val = float(pdr.get_quote_yahoo(proxy)['price'].values.tolist()[0])
                        except:
                            val = float(pdr.get_quote_yahoo(proxy)['preMarketPrice'].values.tolist()[0])
                        state = 1
                        TaurusList.append(str(proxy))
                    except:
                        print("failed to retreive data for "+proxy)
                        state = 0
                    if state == 1:
                        if platform.system() == "Linux":
                            item.setStyleSheet('background-color: lime')
                        elif platform.system() == "Darwin":
                            item.setStyleSheet('background-color: green')
                        else:
                            item.setStyleSheet('background-color: lime')
                        lineedits = self.groupBox.findChildren(QtGui.QLineEdit)
                        lineedits[bval].setText(str(val))
                        font = lineedits[bval].font()
                        try:
                            ffont = QtGui2.QFont(font)
                            thissize = QtGui2.QFontMetrics(ffont).boundingRect(lineedits[bval].text()).width()
                        except:
                            ffont = QtGui.QFont(font)
                            thissize = QtGui.QFontMetrics(ffont).boundingRect(lineedits[bval].text()).width()
                        if thissize > self.maxsize:
                            self.maxsize = thissize
                    else:
                        item.setStyleSheet('QPushButton {background-color: maroon; color: white}')
                        lval = -1
                        for lineedit in self.groupBox.findChildren(QtGui.QLineEdit):
                            lval += 1
                            if lval == bval:
                                lineedit.setText("-")
                elif self.ctrl_library == "Randomizer":
                    val = random.random()
                    if platform.system() == "Linux":
                        item.setStyleSheet('background-color: lime')
                    elif platform.system() == "Darwin":
                        item.setStyleSheet('background-color: green')
                    else:
                        item.setStyleSheet('background-color: lime')
                    lineedits = self.groupBox.findChildren(QtGui.QLineEdit)
                    lineedits[bval].setText(str(val))
                    font = lineedits[bval].font()
                    try:
                        ffont = QtGui2.QFont(font)
                        thissize = QtGui2.QFontMetrics(ffont).boundingRect(lineedits[bval].text()).width()
                    except:
                        ffont = QtGui.QFont(font)
                        thissize = QtGui.QFontMetrics(ffont).boundingRect(lineedits[bval].text()).width()
                    if thissize > self.maxsize:
                        self.maxsize = thissize
                    TaurusList.append(str(proxy))
                elif self.ctrl_library == "HistoricalData":
                    val = 0.
                    if platform.system() == "Linux":
                        item.setStyleSheet('background-color: lime')
                    elif platform.system() == "Darwin":
                        item.setStyleSheet('background-color: green')
                    else:
                        item.setStyleSheet('background-color: lime')
                    lineedits = self.groupBox.findChildren(QtGui.QLineEdit)
                    if hasattr(val, "__len__"):
                        val = 'nscalar, len = '+str(len(val))
                    else:
                        val = "{0:.4f}".format(val)
                    lineedits[bval].setText(str(val))
                    font = lineedits[bval].font()
                    try:
                        ffont = QtGui2.QFont(font)
                        thissize = QtGui2.QFontMetrics(ffont).boundingRect(lineedits[bval].text()).width()
                    except:
                        ffont = QtGui.QFont(font)
                        thissize = QtGui.QFontMetrics(ffont).boundingRect(lineedits[bval].text()).width()
                    if thissize > self.maxsize:
                        self.maxsize = thissize
                    TaurusList.append(str(proxy))
            except:
                item.setStyleSheet('QPushButton {background-color: maroon; color: white}')
            print("Loading: "+str("{0:.2f}".format(100*(bval+1)/len(self.buttonGroup.buttons())))+"%")
        self.TaurusList = TaurusList
        for lineedit in self.groupBox.findChildren(QtGui.QLineEdit):
            try:
                lineedit.setFixedWidth(self.maxsize+25)
            except:
                lineedit.setFixedWidth(50)
        if self.ctrl_library == "Tango":
            self.bottomlabel.setText(str(str(self.listofbpmattributeslistbox.currentText()) + " statuses loaded."))
        elif self.ctrl_library == "Randomizer":
            self.bottomlabel.setText(str(str(self.listofbpmattributeslistbox.currentText()) + " statuses loaded."))
        if self.ctrl_library == "HistoricalData":
            self.bottomlabel.setText(str("Select 1D or 2D plotting for the historical datafile."))
        elif self.ctrl_library == "EPICS":
            self.bottomlabel.setText(str("PV statuses loaded."))
        self.setMaximumSize(10,10)
        self.resize(self.sizeHint().width(), self.sizeHint().height())

    def getAllAttsClicked(self):
        dev_ids = []
        valid_devs = []
        valid_attr_names = []
        if self.ctrl_library == "Tango":
            alldevs = self.devlist
        elif self.ctrl_library == "Randomizer":
            alldevs = self.devlist
        elif self.ctrl_library == "HistoricalData":
            alldevs = self.devlist
        elif self.ctrl_library == "EPICS":
            alldevs = self.PV_list
        for dev in alldevs:
            dev_id = dev.split("/")
            dev_id = dev_id[len(dev_id)-1]
            if dev_id not in [str(x) for x in dev_ids]:
                dev_ids.append(dev_id)
                valid_devs.append(dev)
        for dev in valid_devs:
            try:
                if self.ctrl_library == "Tango":
                    for devi in [PT.DeviceProxy(dev)]:
                        atts = devi.attribute_list_query()[:]
                        for att in atts:
                            if att.name not in [str(x) for x in valid_attr_names]:
                                valid_attr_names.append(att.name)
                elif self.ctrl_library == "Randomizer" or self.ctrl_library == "HistoricalData":
                    valid_attr_names = []
                    for n in range(5):
                        valid_attr_names.append("Random attribute "+str(n))
            except:
                None
        self.listofbpmattributes = valid_attr_names
        self.listofbpmattributeslistbox.clear()
        self.listofbpmattributeslistbox.addItems(self.listofbpmattributes)
        self.setMaximumSize(10,10)
        self.resize(self.sizeHint().width(), self.sizeHint().height())

    def plotin2D(self):
        TaurusList = []
        DevsNames = []
        if self.ctrl_library == "Tango":
            attr = str(self.listofbpmattributeslistbox.currentText())
        elif self.ctrl_library ==  "Randomizer":
            attr = str(self.listofbpmattributeslistbox.currentText())
        scalars =[]
        for devs in self.TaurusList:
            if self.ctrl_library == "EPICS" or self.ctrl_library == "Finance":
                TaurusList.append(str(devs))
            else:
                TaurusList.append(str(devs)+"/"+attr)
            DevsNames.append(str(devs))
            if self.ctrl_library == "Tango":
                prox = [PT.DeviceProxy(str(devs))]
                for bd in prox:
                    val = bd.read_attribute(str(self.listofbpmattributeslistbox.currentText())).value
            elif self.ctrl_library == "Randomizer":
                val = random.random()
            elif self.ctrl_library == "HistoricalData":
                val = 0.
            elif self.ctrl_library == "EPICS":
                val = epics.PV(devs, auto_monitor=True).value
            elif self.ctrl_library == "Finance":
                try:
                    try:
                        val = float(pdr.get_quote_yahoo(devs)['price'].values.tolist()[0])
                    except:
                        val = float(pdr.get_quote_yahoo(devs)['preMarketPrice'].values.tolist()[0])
                except:
                    print("failed to retreive data for "+devs)
                    val = 0
            if hasattr(val, "__len__"):
                scalars.append(1)
            else:
                print("scalar")
                scalars.append(0)
        if sum(scalars) == 0:
            self.scalarflag = 1 # it is a scalar
        else:
            self.scalarflag = 0 # it is a vector
        if len(TaurusList) < 1:
            if self.ctrl_library == "EPICS":
                self.bottomlabel.setText("No active defined PVs found.")
            elif self.ctrl_library == "Finance":
                self.bottomlabel.setText("No stocks with defined names could be imported.")
            else:
                self.bottomlabel.setText("No devices found with attribute "+attr+".")
        elif self.scalarflag == 0:
            QtGui.QMessageBox.information(self,"Error",'Cannot 2D plot vectors yet.')
        else:
            self.toSpecTaurusList = TaurusList
            self.okflag = 0
            prep2D = prep2DGUI(self)
            prep2D.exec_()
            if self.okflag == 1:
                self.specflag = 0
                spectro = Spectrogram(self)
                spectro.show()

    def plotin1D(self):
        TaurusList = []
        DevsNames = []
        if self.ctrl_library == "Tango":
            attr = str(self.listofbpmattributeslistbox.currentText())
        elif self.ctrl_library ==  "Randomizer":
            attr = str(self.listofbpmattributeslistbox.currentText())
        for devs in self.TaurusList:
            if self.ctrl_library == "EPICS" or self.ctrl_library == "Finance":
                TaurusList.append(str(devs))
            else:
                TaurusList.append(str(devs)+"/"+attr)
            DevsNames.append(str(devs))
            if self.ctrl_library == "Tango":
                prox = [PT.DeviceProxy(str(devs))]
                for bd in prox:
                    val = bd.read_attribute(str(self.listofbpmattributeslistbox.currentText())).value
            elif self.ctrl_library ==  "Randomizer":
                val = random.random()
            elif self.ctrl_library == "EPICS":
                val = epics.PV(devs, auto_monitor=True).value
            elif ctrl_library == "Finance":
                try:
                    val = float(pdr.get_quote_yahoo(devs)['price'].values.tolist()[0])
                except:
                    val = float(pdr.get_quote_yahoo(devs)['preMarketPrice'].values.tolist()[0])
        if len(TaurusList) < 1:
            failflag = 1
            if self.ctrl_library == "EPICS":
                self.bottomlabel.setText("No active defined PVs found.")
            else:
                self.bottomlabel.setText("No devices found with attribute "+attr+".")
            if self.ctrl_library == "EPICS":
                reply = QtGui.QMessageBox.question(self, 'Issue', 'No active defined PV:s found.  Enter archiving mode?', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    failflag = 0
                    self.archivingonly = 1
                    self.toSpecTaurusList = self.PV_list
                    self.toSpecDevList = self.PV_list
        else:
            failflag = 0
            self.archivingonly = 0
            self.toSpecTaurusList = TaurusList
            self.toSpecDevList = DevsNames
        self.okflag = 0
        if failflag == 0:
            if self.archivingonly == 0:
                prep1D = prep1DGUI(self)
                prep1D.exec_()
            else:
                self.okflag = 1
            if self.okflag == 1:
                lt = PyQtGraphPlotter(self)
                lt.resize(800,600)
                lt.show()

    def handleButtonClicked(self,button):
        for item in self.buttonGroup.buttons():
            if button is item:
                if item.palette().button().color().name() == "#800000":
                    self.bottomlabel.setText("Cannot establish contact with this device.")
                else:
                    proxy = item.text()
                    if self.ctrl_library == "Tango":
                        self.bottomlabel.setText("Launching AtkPanel for "+str(proxy)+".")
                        os.system("atkpanel "+str(proxy) +"  &")
                    elif self.ctrl_library == "Randomizer":
                        QtGui.QMessageBox.information(self,"Control panel", "Random control panel is empty.")
                    elif self.ctrl_library == "Finance":
                        stock = item.text()
                        data = pdr.get_quote_yahoo(item.text())
                        list = [data.columns.values.tolist()] + data.values.tolist()
                        datalist1 = ""
                        datalist2 = ""
                        minwidth = 0
                        for n in range(len(list[0])):
                            if str(list[0][n]) == "financialCurrency" or str(list[0][n]) == "longName" or str(list[0][n]) == "price":
                                datalist1 = datalist1 + str(str(list[0][n])+" :  "+str(list[1][n])+"\n")
                            else:
                                datalist2 = datalist2 + str(str(list[0][n])+" :  "+str(list[1][n])+"\n")
                        datalist = datalist1 + "\n- - - - - - - - - -\n" + datalist2
                        msg = QtGui.QMessageBox(self)
                        msg.setWindowTitle(str(stock)+" info")
                        msg.setText(datalist)
                        layout = msg.layout()
                        item = layout.itemAtPosition(0, 1)
                        widget = item.widget()
                        widget.setFixedWidth(500)
                        msg.show()
                    elif self.ctrl_library == "EPICS":
                        QtGui.QMessageBox.information(self,"Control panel", "EPICS device control and/or information panel is currently empty")

    def wildcardsImportClicked(self):
        wildGUI = wildcardsGUI(self)
        wildGUI.setModal(True)
        wildGUI.exec_()
        print(self.PV_list)
        if self.reloadflag == 1:
            reply = QtGui.QMessageBox.question(self, 'Duplicates', 'Remove any duplicate(s)?', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                if self.ctrl_library == "Tango":
                    self.devlist = list(dict.fromkeys(self.devlist))
                elif self.ctrl_library == "Randomizer":
                    self.devlist = list(dict.fromkeys(self.devlist))
                elif self.ctrl_library == "EPICS":
                    self.PV_list = list(dict.fromkeys(self.PV_list))

            if self.ctrl_library == "EPICS":
                if len(self.PV_descriptions) < len(self.PV_list):
                    for m in range(len(self.PV_descriptions),len(self.PV_list)):
                        self.PV_descriptions.append(self.PV_list[m])
            self.maxsize = 0
            self.killdynamicbuttongroup()
            self.getallDevs()
            # The layout should be minimal, so make it unrealistically small (x=10, y=10 [px]) and then resize to minimum.
            self.resizeDynaGUI()
            self.reloadflag = 0

    def listbtnclicked(self):
        listGui = listbtnGUI(self)
        listGui.setModal(True)
        listGui.exec_()
        if self.ctrl_library == "Tango":
            self.listofbpmattributeslistbox.clear()
            self.listofbpmattributeslistbox.addItems(self.listofbpmattributes)
        elif self.ctrl_library == "Randomizer":
            self.listofbpmattributeslistbox.clear()
            self.listofbpmattributeslistbox.addItems(self.listofbpmattributes)

        if self.reloadflag == 1:
            devlist = []
            if self.ctrl_library == "Tango":
                for n in self.devlist:
                    if n not in devlist:
                        devlist.append(n)
                self.devlist = devlist
            elif self.ctrl_library == "Randomizer":
                for n in self.devlist:
                    if n not in devlist:
                        devlist.append(n)
                self.devlist = devlist
            elif self.ctrl_library == "EPICS":
                for n in self.PV_list:
                    if n not in devlist:
                        devlist.append(n)
                self.PV_list = devlist
            elif self.ctrl_library == "Finance":
                for n in self.stocknames:
                    if n not in devlist:
                        devlist.append(n)
                self.stocknames = devlist
            self.maxsize = 0
            self.killdynamicbuttongroup()
            self.getallDevs()
            self.resizeDynaGUI()
            self.reloadflag = 0

    def resizeDynaGUI(self):
            self.setMaximumSize(10,10)
            self.resize(self.sizeHint().width(), self.sizeHint().height())

    def get_all_functions_from_module(module, functions={}):
        for f in math.__dict__:
          obj = getattr(math, f)
          if callable(obj):
           functions[f] = obj
        return functions

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Exit', 'Are you sure you want to exit? All unsaved data will be lost.', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            self.close()
        else:
            event.ignore() # Works for all

class listbtnGUI(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(listbtnGUI, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Edit DynaGUI NV")
        listgui = QtGui.QFormLayout(self)

        if self.parent.ctrl_library == "Tango":
            devslbl = QtGui.QLabel("List of devices:")
            self.textboxDevs = QtGui.QPlainTextEdit('\n'.join(parent.devlist))
            attrlbl = QtGui.QLabel("List of device attributes:")
            self.textboxAttr = QtGui.QPlainTextEdit('\n'.join(parent.listofbpmattributes))
        elif self.parent.ctrl_library == "Randomizer":
            devslbl = QtGui.QLabel("List of devices:")
            self.textboxDevs = QtGui.QPlainTextEdit('\n'.join(parent.devlist))
            attrlbl = QtGui.QLabel("List of device attributes:")
            self.textboxAttr = QtGui.QPlainTextEdit('\n'.join(parent.listofbpmattributes))
        elif self.parent.ctrl_library == "Finance":
            devslbl = QtGui.QLabel("List of devices:")
            self.textboxDevs = QtGui.QPlainTextEdit('\n'.join(parent.stocknames))
        elif self.parent.ctrl_library == "EPICS":
            devslbl = QtGui.QLabel("List of Process Variables:")
            self.textboxDevs = QtGui.QPlainTextEdit('\n'.join(parent.PV_list))
            attrlbl = QtGui.QLabel("List of PV descriptions:")
            self.textboxAttr = QtGui.QPlainTextEdit('\n'.join(parent.PV_descriptions))
        rowslbl = QtGui.QLabel("Max. number of rows:")
        self.textboxRows = QtGui.QDoubleSpinBox()
        self.textboxRows.setValue(parent.Nrows)

        okbtn = QtGui.QPushButton('Ok')
        nobtn = QtGui.QPushButton('Cancel')
        listgui.addRow(devslbl)
        listgui.addRow(self.textboxDevs)
        if self.parent.ctrl_library != "Finance":
            listgui.addRow(attrlbl)
            listgui.addRow(self.textboxAttr)
        listgui.addRow(rowslbl,self.textboxRows)
        listgui.addRow(okbtn, nobtn)
        okbtn.clicked.connect(self.confirmfunc)
        nobtn.clicked.connect(self.cancelfunc)

    def confirmfunc(self):
        textDevs = str(self.textboxDevs.toPlainText())
        self.newlistDevs = textDevs.split()

        if self.parent.ctrl_library == "Tango":
            if self.parent.devlist != self.newlistDevs:
                self.parent.devlist = self.newlistDevs
                self.parent.reloadflag = 1

            textAtts = str(self.textboxAttr.toPlainText())
            self.newlistAtts = textAtts.split()
            self.parent.listofbpmattributes = self.newlistAtts

        elif self.parent.ctrl_library == "Randomizer":
            if self.parent.devlist != self.newlistDevs:
                self.parent.devlist = self.newlistDevs
                self.parent.setMaximumSize(10,10)
                self.parent.resize(self.sizeHint().width(), self.sizeHint().height())
                self.parent.reloadflag = 1

            textAtts = str(self.textboxAttr.toPlainText())
            self.newlistAtts = textAtts.split()
            self.parent.listofbpmattributes = self.newlistAtts

        elif self.parent.ctrl_library == "EPICS":
            if self.parent.PV_list != self.newlistDevs:
                self.parent.PV_list = self.newlistDevs
                self.parent.reloadflag = 1

            textAtts = str(self.textboxAttr.toPlainText())
            self.newlistAtts = textAtts.split()
            self.parent.PV_descriptions = self.newlistAtts

        elif self.parent.ctrl_library == "Finance":
            if self.parent.stocknames != self.newlistDevs:
                self.parent.stocknames = self.newlistDevs
                self.parent.reloadflag = 1

        if self.parent.Nrows != self.textboxRows.value():
            self.parent.Nrows = self.textboxRows.value()
            self.parent.reloadflag = 1

        self.close()

    def cancelfunc(self):
        self.close() # Works for all

class wildcardsGUI(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(wildcardsGUI, self).__init__(parent)
        self.parent = parent
        text,ok = QtGui.QInputDialog.getText(self,"Get devices","Define wildcards",text="lebt*sol*curr")
        self.setWindowTitle("Import PyTango Devices using WildCards")
        listgui = QtGui.QFormLayout(self)
        nobtn = QtGui.QPushButton('Cancel')
        nobtn.clicked.connect(self.cancelfunc)
        if ok and text:
            if self.parent.ctrl_library == "Tango":
                db = PT.Database()
                self.devs = db.get_device_exported(str(text))
            elif self.parent.ctrl_library == "Randomizer":
                self.devs = []
                inptxt = text.split("/")
                for m in range(len(inptxt)):
                    self.devs.append("RandomDevice_"+str(m)+"_"+str(inptxt[m]))
            elif self.parent.ctrl_library == "EPICS":
                pv_repo='https://pos.esss.lu.se/data/getData.json'
                pv_page = requests.get(pv_repo)
                pv_data = json.loads(pv_page.content)
                pv_list = []
                for i in pv_data:
                    for j in pv_data[i]:
                        for k in pv_data[i][j]:
                            pv_list.append(k)
                self.devs = []
                pv_list_lower = [x.casefold() for x in pv_list]
                wildcc = text.casefold()
                for ind,pv in enumerate(pv_list_lower):
                    if fnmatch.fnmatch(pv,wildcc):
                        self.devs.append(pv_list[ind])
                if len(self.devs) == 0:
                    self.devs = ['-']

            self.devs = '\n'.join(self.devs)
            devslbl = QtGui.QLabel("List of devices found:")
            self.textboxDevs = QtGui.QPlainTextEdit(self.devs)
            okbtn = QtGui.QPushButton('Ok')
            listgui.addRow(devslbl)
            listgui.addRow(self.textboxDevs)
            okbtn.clicked.connect(self.confirmfunc)
            devslbl2 = QtGui.QLabel("Remove all the devices you do not want to import.\nPressing Ok will add all the above defined devices to DynaGUI.")
            listgui.addRow(devslbl2)
            listgui.addRow(okbtn,nobtn)
        else:
            lbl = QtGui.QLabel("WildCard import of devices cancelled.")
            nobtn.setText("Ok")
            listgui.addRow(lbl)
            listgui.addRow(nobtn)
        self.setLayout(listgui)

    def confirmfunc(self):
        textDevs = str(self.textboxDevs.toPlainText())
        self.newlistDevs = textDevs.split()
        noflag = 0
        if len(self.newlistDevs) > 40:
            reply = QtGui.QMessageBox.question(self,"Warning", "You are about to load "+str(len(self.newlistDevs))+ " devices into DynaGUI NV. Too many can overload the computer. Proceed?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                noflag = 1
        if noflag == 0:
            for dev in self.newlistDevs:
                if self.parent.ctrl_library == "Tango":
                    self.parent.devlist.append(dev)
                elif self.parent.ctrl_library == "Randomizer":
                    self.parent.devlist.append(dev)
                elif self.parent.ctrl_library == "EPICS":
                    self.parent.PV_list.append(dev)
            self.parent.reloadflag = 1
            self.close()

    def cancelfunc(self):
        self.close() # Works for Tango

class Surfogram(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(Surfogram, self).__init__(parent)
        pg.opengl.GLSurfacePlotItem # Future contour (3D) plotting

class prep1DGUI(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(prep1DGUI, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Setup 1D plotting")
        listgui = QtGui.QFormLayout(self)

        freqlbl = QtGui.QLabel("Plotting frequency: [Hz]")
        self.textboxF = QtGui.QDoubleSpinBox()
        self.textboxF.setValue(parent.toSpecupdateFrequency)

        if parent.ctrl_library == "Finance":
            self.textboxF.setMaximum(1)


        minulbl = QtGui.QLabel("# of minutes to show the plotting: [min]")
        self.textboxM = QtGui.QDoubleSpinBox()
        self.textboxM.setValue(parent.toSpecminutes)

        self.textboxF.setMinimum(0.01)
        self.textboxM.setMinimum(0.1)

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
        self.close() # Works for all

class prep2DGUI(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(prep2DGUI, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Setup 2D spectrogram plotting")
        listgui = QtGui.QFormLayout(self)


        freqlbl = QtGui.QLabel("Plotting frequency: [Hz]")
        self.textboxF = QtGui.QDoubleSpinBox()
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
        self.close() # Works for all

class Spectrogram(QtGui.QDialog):
    def __init__(self, parent = Dialog):
        super(Spectrogram, self).__init__(parent)
        self.ctrl_library = parent.ctrl_library
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
        print(self.tSize)
        print(self.DevsSize)
        self.plotarr = np.zeros((int(self.tSize),int(self.DevsSize)))
        x = []
        for minute in range(-int(self.minutes), int(self.minutes/10), 2):
            if minute == 0:
                x.append('Now')
            else:
                x.append(format('%s min') % minute)
        xt = [i for i in range(0, int(self.updateFrequency)*(self.minutes+1)*60, int(self.updateFrequency*2*60))]
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
        self.t.start(int(1000/self.updateFrequency))

    def editcm(self):
        items = ("CM1","CM2","CM3")
        item,ok = QtGui.QInputDialog.getItem(self,"Edit CM:s","Select CM #:",items,0,False)
        if ok and item:
            if item == "CM1":
                self.cm1 = self.getcm(self.cm1,'CM1')
            elif item == "CM2":
                self.cm2 = self.getcm(self.cm2,'CM2')
            elif item == "CM3":
                self.cm3 = self.getcm(self.cm3,'CM3')
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
        self.refarr = self.plotarr[int(self.tSize-1),:]

    def plotTrace(self): # From JonPet
        fig = plt.figure()
        i = round(float(self.isoV.value()))
        if i == self.tSize:
            i = self.tSize - 1
        if str(self.plotvsstoredbtn.text()) == 'Plotting vs stored':
            arr = (self.plotarr[int(i),:]) - self.refarr
            yaxis = " (real - stored values)"
        elif str(self.plotvsstoredbtn.text()) == 'Plotting real values':
            arr = (self.plotarr[int(i),:])
            yaxis = " (real values)"
        plt.plot(arr, picker=5)
        plt.xlabel('Device index')
        plt.ylabel(str(self.title+yaxis))
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
            sensname = self.sensorNames[ind[0]].split('/')
            if len(sensname) > 2:
                sensname = '  '.join([sensname[0], sensname[2]])
            elif len(sensname) > 1:
                sensname = '  '.join([sensname[1], sensname[0]])
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
            if self.ctrl_library == "Tango":
                prox = [PT.DeviceProxy(str("/".join(inp.split('/')[:-1])))]
                for bd in prox:
                    val = bd.read_attribute(attr).value
            elif self.ctrl_library == "Randomizer":
                val = random.random()
            elif self.ctrl_library == "EPICS":
                val = epics.PV(inp, auto_monitor=True).value
            elif self.ctrl_library == "Finance":
                try:
                    try:
                        val = float(pdr.get_quote_yahoo(inp)['price'].values.tolist()[0])
                    except:
                        val = float(pdr.get_quote_yahoo(inp)['preMarketPrice'].values.tolist()[0])
                except:
                    print("Warning: Failed to retreive data for "+inp)
                    val = 0

            y.append(str(val))
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
        self.close() # Must add waveform support

class PyQtGraphPlotter(QtGui.QMainWindow):
    def __init__(self, parent = Dialog):
        super(PyQtGraphPlotter, self).__init__(parent)
        self.ctrl_library = parent.ctrl_library
        self.parent = parent
        self.central_widget = QtGui.QStackedWidget()

        self.setCentralWidget(self.central_widget)
        self.contWidget = PyQtGraphContainerWidget(self)
        if self.parent.archivingonly == 0:
            self.contWidget.plotbtn.clicked.connect(self.startstop)
        elif self.parent.archivingonly == 1:
            self.contWidget.plotbtn.setEnabled(False)
            self.contWidget.plotbtn.setText("Archiving Mode")
            self.archivemode = 1
        self.contWidget.loadbtn.clicked.connect(self.loadclick)
        self.contWidget.savebtn.clicked.connect(self.saveclick)
        self.contWidget.plotsettingsbtn.clicked.connect(self.PlotSettings)
        self.contWidget.showhidelegends.clicked.connect(self.showhidelegend)
        self.contWidget.resetbtn.clicked.connect(self.reset)
        self.contWidget.hideshowallbtn.clicked.connect(self.showhideall)
        self.central_widget.addWidget(self.contWidget)
        self.pyqtgraphtimer = QtCore.QTimer()
        self.devslist = []
        self.sensorNames = parent.toSpecTaurusList

        for ind, inp in enumerate(parent.toSpecTaurusList):
            self.attr = inp.split('/')
            self.attr = str(self.attr[len(self.attr)-1])
            self.devslist.append(str("/".join(inp.split('/')[:-1])))
            self.data_y0desc = parent.toSpecDevList
        self.cols = len(self.devslist)

        self.minutes = parent.toSpecminutes
        self.updateFrequency = parent.toSpecupdateFrequency

        self.contWidget.plot.setXRange(-60 * 1.01 * self.minutes,0)
        if self.ctrl_library == "Tango":
            self.setWindowTitle(self.attr)
        elif self.ctrl_library == "Randomizer":
            self.setWindowTitle("Random Values Plotted")
        elif self.ctrl_library == "EPICS":
            self.setWindowTitle("Process Variables")
        self.devsPlotting = []
        self.colorlist=[[255,255,255],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255],[128,0,0],[139,0,0],[165,42,42],[178,34,34],[220,20,60],[255,99,71],[255,127,80],[205,92,92],[240,128,128],[233,150,122],[250,128,114],[255,160,122],[255,69,0],[255,140,0],[255,165,0],[255,215,0],[184,134,11],[218,165,32],[238,232,170],[189,183,107],[240,230,140],[128,128,0],[154,205,50],[85,107,47],[107,142,35],[124,252,0],[127,255,0],[173,255,47],[0,100,0],[0,128,0],[34,139,34],[50,205,50],[144,238,144],[152,251,152],[143,188,143],[0,250,154],[0,255,127],[46,139,87],[102,205,170],[60,179,113],[32,178,170],[47,79,79],[0,128,128],[0,139,139],[224,255,255],[0,206,209],[64,224,208],[72,209,204],[175,238,238],[127,255,212],[176,224,230],[95,158,160],[70,130,180],[100,149,237],[0,191,255],[30,144,255],[173,216,230],[135,206,235],[135,206,250],[25,25,112],[0,0,128],[0,0,139],[0,0,205],[65,105,225],[138,43,226],[75,0,130],[72,61,139],[106,90,205],[123,104,238],[147,112,219],[139,0,139],[148,0,211],[153,50,204],[186,85,211],[128,0,128],[216,191,216],[221,160,221],[238,130,238],[218,112,214],[199,21,133],[219,112,147],[255,20,147],[255,105,180],[255,182,193],[255,192,203],[250,235,215],[245,245,220],[255,228,196],[255,235,205],[245,222,179],[255,248,220],[255,250,205],[250,250,210],[255,255,224],[139,69,19],[160,82,45],[210,105,30],[205,133,63],[244,164,96],[222,184,135],[210,180,140],[188,143,143],[255,228,181],[255,222,173],[255,218,185],[255,228,225],[255,240,245],[250,240,230],[253,245,230],[255,239,213],[255,245,238],[245,255,250],[112,128,144],[119,136,153],[176,196,222],[230,230,250],[255,250,240],[240,248,255],[248,248,255],[240,255,240],[255,255,240],[240,255,255],[105,105,105],[128,128,128],[169,169,169],[192,192,192],[211,211,211],[220,220,220],[245,245,245]]
        self.colorind = []
        self.delays_y0 = []
        self.delays_y = []
        self.ch_sublayout = QtGui.QGridLayout(self.contWidget.chGroupBox)
        for n in range(self.cols):
            self.delays_y0.append(0)
            m = n
            while m > len(self.colorlist)-1:
                m = m - len(self.colorlist)
            self.colorind.append(self.colorlist[m])
        self.listInit()
        self.constructLegendItem()

        self.scrollarea = QtGui.QScrollArea(self)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setMinimumWidth(int(self.maxwidth*1.5+50))
        self.scrollarea.setWidget(self.contWidget.chGroupBox)
        self.contWidget.layout.addWidget(self.scrollarea,0,7,3,1)
        self.contWidget.setLayout(self.contWidget.layout)

        self.pyqtgraphtimer.timeout.connect(self.updater)
        if self.ctrl_library == "Tango":
            self.ylabel = self.attr
        elif self.ctrl_library == "Randomizer":
            self.ylabel = self.attr
        elif self.ctrl_library == "EPICS":
            self.ylabel = "PV value(s)"
        elif self.ctrl_library == "Finance":
            self.ylabel = "USD"

        self.contWidget.plot.setLabel('left',self.ylabel,color='white',size = 30)
        self.scrollarea.setVisible(False)

        if self.archivemode == 1:
            self.loadclick()

    def showhideall(self):
        if self.contWidget.hideshowallbtn.text() == "Hide All":
            self.contWidget.hideshowallbtn.setText("Show All")
            for chBox in self.contWidget.chGroupBox.findChildren(QtGui.QCheckBox):
                chBox.setChecked(False)
        elif self.contWidget.hideshowallbtn.text() == "Show All":
            self.contWidget.hideshowallbtn.setText("Hide All")
            for chBox in self.contWidget.chGroupBox.findChildren(QtGui.QCheckBox):
                chBox.setChecked(True)

    def showhidelegend(self):
        if self.contWidget.showhidelegends.text() == "Hide legend":
            self.contWidget.showhidelegends.setText("Show legend")
            self.scrollarea.setVisible(False)
        elif self.contWidget.showhidelegends.text() == "Show legend":
            self.contWidget.showhidelegends.setText("Hide legend")
            self.scrollarea.setVisible(True)

    def colorbtnRGBchange(self,inp):
        prevsetting = self.colorind[int(inp)]
        prevset = ', '.join(str(x) for x in prevsetting)
        text,ok = QtGui.QInputDialog.getText(self,"Set linecolor","Define the color of the line in [R,G,B] format:",text=prevset)
        if ok and text:
            text = text.split(',')
            cm = []
            errflag = 0
            for n in text:
                try:
                    cm.append(int(n))
                except:
                    QtGui.QMessageBox.information(self,"Error",'Cannot convert input to integer: '+str(n))
                    errflag = 1
            if len(cm) == 3:
                if errflag == 0:
                    self.colorind[int(inp)] = cm
                    for ind,btn in enumerate(self.contWidget.chGroupBox.findChildren(QtGui.QPushButton)):
                        if str(ind) == inp:
                            col0 = str(cm[0])
                            col1 = str(cm[1])
                            col2 = str(cm[2])
                            btn.setStyleSheet("background-color:rgb("+col0+","+col1+","+col2+")");
                    self.chBoxCheck()
            else:
                QtGui.QMessageBox.information(self,"Error",'Incorrect N of inputs')

    def chBoxCheck(self):
        devsPlotting = []
        devs_original = len(self.data_x0)

        print(len(self.data_y0))
        print(len(self.data_y))

        for ind,chBox in enumerate(self.contWidget.chGroupBox.findChildren(QtGui.QCheckBox)):
            if chBox.isChecked() == 1:
                devsPlotting.append(1)
                timestamps = []
                if ind < devs_original:
                    for timestamp in self.data_x0[ind]:
                        if self.archivemode == 0:
                            timestamps.append(timestamp - time.time() + self.delays_y0[ind])
                        elif self.archivemode == 1:
                            if ind < len(self.sensorNames):
                                timestamps.append(timestamp + self.delays_y0[ind])
                            else:
                                timestamps.append(timestamp)
                    if self.archivemode == 0:
                        self.curve[ind].setData(timestamps, self.data_y0[ind],pen=pg.mkPen(self.colorind[ind], width=2))
                    elif self.archivemode == 1 and ind < len(self.sensorNames):
                        self.curve[ind].setData(timestamps, self.data_y0[ind],pen=pg.mkPen(self.colorind[ind], width=2))
                    else:
                        self.curve[ind].setData(timestamps, self.data_y[ind-len(self.sensorNames)],pen=pg.mkPen(self.colorind[ind], width=2))
            elif chBox.isChecked() == 0:
                devsPlotting.append(0)
                self.curve[ind].clear()
        self.devsPlotting = devsPlotting

    def funccalculator(self,linenum,equation,nn):
        if equation == 'none':
            outputval = 0
        else:
            spltA = equation.split('PV[')
            if len(spltA) > 1:
                parts = []
                for partA in spltA:
                    spltB = partA.split(']')
                    for partB in spltB:
                        parts.append(partB)
                equationparts = []
                for partC in range(len(parts)):
                    if int(partC/2) - partC/2 == 0: # even --> string
                        equationparts.append(parts[partC])
                    else: # odd --> value from PV
                        value = self.data_y0[int(parts[partC])][nn]
                        equationparts.append(str(value))
                das_equation = "".join(equationparts)
            else:
                das_equation = equation
            try:
                outputval = numexpr.evaluate(das_equation)
            except:
                QtGui.QMessageBox.information(self,"Error",'Cannot interpret equation for line '+str(linenum)+":\n"+str(self.equations[linenum]))
                self.equations[linenum] = 'none'
                outputval = self.data_y0[linenum][nn]
        return outputval

    def listInit(self):
        self.data_x0 = []
        self.curve = []
        self.data_y = []
        self.data_x = []
        self.data_ydesc = []
        self.data_y0 = []
        self.time_0 = -1
        self.equations = []
        self.functions = []
        self.archivemode = self.parent.archivingonly
        for n in range(self.cols):
            self.curve.append(self.contWidget.plot.getPlotItem().plot(name=self.data_y0desc[n]))
            if self.parent.archivingonly == 0:
                if self.ctrl_library == "Tango":
                    prox = [PT.DeviceProxy(self.devslist[n])]
                    for bd in prox:
                        val = bd.read_attribute(self.attr).value
                elif self.ctrl_library == "Randomizer":
                    val = random.random()
                elif self.ctrl_library == "EPICS":
                    val = epics.PV(str(self.sensorNames[n]), auto_monitor=True).value
                elif self.ctrl_library == "Finance":
                    try:
                        val = float(pdr.get_quote_yahoo(self.sensorNames[n])['price'].values.tolist()[0])
                    except:
                        val = float(pdr.get_quote_yahoo(self.sensorNames[n])['preMarketPrice'].values.tolist()[0])
                self.data_y0.append([val])
            else:
                self.data_y0.append([0])
            self.data_x0.append([time.time()])
            self.devsPlotting.append(1)

    def updater(self):
        if self.archivemode == 0:
            maxval = 0
            maxvallbl = -1
            for n, inp in enumerate(self.devslist):
                if self.ctrl_library == "Tango":
                    prox = [PT.DeviceProxy(inp)]
                    for bd in prox:
                        val = bd.read_attribute(self.attr).value
                elif self.ctrl_library == "Randomizer":
                    val = self.data_y0[n][-1]+0.2*(0.5-random.random())
                elif self.ctrl_library == "EPICS":
                    val = epics.PV(str(self.sensorNames[n]), auto_monitor=True).value
                elif self.ctrl_library == "Finance":
                    try:
                        val = float(pdr.get_quote_yahoo(self.sensorNames[n])['price'].values.tolist()[0])
                    except:
                        val = float(pdr.get_quote_yahoo(self.sensorNames[n])['preMarketPrice'].values.tolist()[0])
                self.data_y0[n].append(val)
                self.data_x0[n].append(time.time())
                tormv = []
                for nn in range(len(self.data_x0[n])):
                    if self.data_x0[n][nn] - time.time() < -60 * 1.01 * self.minutes:
                        tormv.append(nn)
                for nnn in range(len(tormv)):
                    del(self.data_x0[n][0])
                    del(self.data_y0[n][0])
                timestamps = []
                for timestamp in self.data_x0[n]:
                    timestamps.append(timestamp - time.time() + self.delays_y0[n])
                if self.devsPlotting[n] == 1:
                    if val > maxval:
                        maxval = val
                        maxvallbl = n
                    self.curve[n].setData(timestamps, self.data_y0[n], pen=pg.mkPen(self.colorind[n], width=2))
            timestamps = self.update_userlist()
            for n in range(len(self.data_ydesc)):
                if self.devsPlotting[n+len(self.devslist)] == 1:
                    self.curve[n+len(self.devslist)].setData(timestamps, self.data_y[n], pen=pg.mkPen(self.colorind[n+len(self.devslist)], width=2))
            self.contWidget.graphlbl1.setText("Maximum value / from PV:\n"+str("{0:.10f}".format(maxval))+" / "+str(maxvallbl))

    def update_userlist(self):
        timestamps = []
        for n in range(len(self.data_ydesc)):
            val = self.funccalculator(n,self.equations[n],len(self.data_y0[n])-1)
            self.data_y[n].append(val)
            self.data_x[n].append(time.time())
            tormv = []
            for nn in range(len(self.data_x[n])):
                if self.data_x[n][nn] - time.time() < -60 * 1.01 * self.minutes:
                    tormv.append(nn)
            for nnn in range(len(tormv)):
                del(self.data_x[n][0])
                del(self.data_y[n][0])
            timestamps = []
            for timestamp in self.data_x[n]:
                timestamps.append(timestamp - time.time() + self.delays_y[n])
        return timestamps

    def reset(self):
        reply = QtGui.QMessageBox.question(self, 'Reset, clear', 'Are you sure you want to clear all data? All plotting data will be lost.', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            del self.data_x0
            del self.data_y
            del self.data_x
            del self.data_ydesc
            del self.data_y0
            self.data_x0 = []
            self.data_y = []
            self.data_x = []
            self.data_ydesc = []
            self.data_y0 = []
            for n in range(self.cols):
                self.curve[n].clear()
                self.data_x0.append([0])
                self.data_y0.append([0])

    def PlotSettings(self):
        self.okflag = 0
        if self.pyqtgraphtimer.isActive():
            activeflag = 1
        else:
            activeflag = 0
        settingsW = PyQtGraphSetup(self)
        settingsW.exec_()
        if self.okflag == 1:
            if activeflag == 1:
                self.pyqtgraphtimer.stop()
            self.killdynamiclegendgroup()
            self.constructLegendItem()
            self.acceptNewPlotSettings()
            self.createLineDict()
            maxrows = 20
            colcount = 0
            rowcount = -1
            chBoxes = self.contWidget.chGroupBox.findChildren(QtGui.QCheckBox)
            for ind in range(len(self.data_y0desc)):
                rowcount += 1
                if rowcount == maxrows-1:
                    rowcount = -1
                    colcount += 2
            rowcount += 1
            self.chBoxCheck()
            if activeflag == 1:
                self.pyqtgraphtimer.start(1000/self.updateFrequency)

    def createLineDict(self):

        if len(self.rmvList) > 1:
            self.rmvList.sort()

        for m in reversed(range(len((self.rmvList)))):
            self.data_x[self.rmvList[m]].clear()
            self.data_y[self.rmvList[m]].clear()
            self.curve[self.rmvList[m]].clear()
            self.devsPlotting[self.rmvList[m]].clear()

        self.devsPlotting = [i for i in self.devsPlotting  if i]
        self.data_x = [i for i in self.data_x  if i]
        self.data_y = [i for i in self.data_y  if i]

        for n in range(len(self.data_y),len(self.data_ydesc)):
            self.devsPlotting.append(1)
            self.data_x.append([0])
            self.data_y.append([0])
            self.curve.append(self.contWidget.plot.getPlotItem().plot(name=self.data_ydesc[n]))

    def constructLegendItem(self):
        rowcount = -1
        colcount = 0
        maxrows = 20
        colind = -1
        self.maxwidth = 0
        for ind,dev in enumerate(self.data_y0desc):
            rowcount += 1
            colind += 1
            chBox = QtGui.QCheckBox(str(dev))
            chBox.setToolTip(str(self.devslist[ind]))
            btn = QtGui.QPushButton()
            colorscheme = self.colorind[colind]
            col0 = str(colorscheme[0])
            col1 = str(colorscheme[1])
            col2 = str(colorscheme[2])
            btn.setStyleSheet("background-color:rgb("+col0+","+col1+","+col2+")");
            btn.setFixedWidth(20)
            chBox.setChecked(self.devsPlotting[ind])
            chBox.stateChanged.connect(self.chBoxCheck)
            btn.clicked.connect(partial(self.colorbtnRGBchange,str(ind)))
            try:
                fm = QtGui2.QFontMetrics(chBox.font())
            except:
                fm = QtGui.QFontMetrics(chBox.font())
            chBoxWidth = fm.width(chBox.text())
            chBox.setFixedWidth(int(chBoxWidth*1.5))
            if chBoxWidth > self.maxwidth:
                self.maxwidth = chBoxWidth
            self.ch_sublayout.addWidget(chBox,rowcount,colcount+1,1,1)
            self.ch_sublayout.addWidget(btn,rowcount,colcount,1,1)
            if rowcount == maxrows-1:
                rowcount = -1
                colcount += 2
            if colind > len(self.colorind)-1:
                colind = -1

        for ind,dev in enumerate(self.data_ydesc):
            rowcount += 1
            colind += 1
            if colind > len(self.colorind)-1:
                if colind < len(self.colorlist):
                    self.colorind.append(self.colorlist[colind])
                else:
                    colind = 0
            chBox = QtGui.QCheckBox(str(dev))
            chBox.setToolTip(str(self.equations[ind]))
            btn = QtGui.QPushButton()
            colorscheme = self.colorind[colind]
            col0 = str(colorscheme[0])
            col1 = str(colorscheme[1])
            col2 = str(colorscheme[2])
            btn.setStyleSheet("background-color:rgb("+col0+","+col1+","+col2+")");
            btn.setFixedWidth(20)
            chBox.setChecked(self.devsPlotting[ind])
            chBox.stateChanged.connect(self.chBoxCheck)
            btn.clicked.connect(partial(self.colorbtnRGBchange,str(ind+len(self.data_y0desc))))
            try:
                fm = QtGui2.QFontMetrics(chBox.font())
            except:
                fm = QtGui.QFontMetrics(chBox.font())
            chBoxWidth = fm.width(chBox.text())
            chBox.setFixedWidth(chBoxWidth*1.5)
            if chBoxWidth > self.maxwidth:
                self.maxwidth = chBoxWidth
            self.ch_sublayout.addWidget(chBox,rowcount,colcount+1,1,1)
            self.ch_sublayout.addWidget(btn,rowcount,colcount,1,1)
            if rowcount == maxrows-1:
                rowcount = -1
                colcount += 2
        chBoxes = self.contWidget.chGroupBox.findChildren(QtGui.QCheckBox)
        for chBox in chBoxes:
            chBox.setMinimumWidth(self.maxwidth+50)

    def killdynamiclegendgroup(self):
        # Destroy / kill all chboxes and buttons currently constructed in the ch_sublayout.
        for i in reversed(range(self.ch_sublayout.count())):
            item = self.ch_sublayout.itemAt(i)
            if isinstance(item, QtGui.QWidgetItem):
                item.widget().close()
        for chbox in self.contWidget.chGroupBox.findChildren(QtGui.QCheckBox):
            chbox.deleteLater()
        for button in self.contWidget.chGroupBox.findChildren(QtGui.QPushButton):
            button.deleteLater()

    def acceptNewPlotSettings(self):
        reply = QtGui.QMessageBox.question(self, 'Rescaling', 'Rescale horizontal axis?', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.contWidget.plot.setXRange(-60 * 1.01 * self.minutes,0)
        self.contWidget.plot.setLabel('left',self.ylabel,color='white',size = 30)
        if self.archivemode == 0:
            reply = QtGui.QMessageBox.question(self, 'Equations application', 'Do you want the equations to be applied on previous values in the plot?', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                applyall = True
            else:
                applyall = False
        else:
            applyall = True
        if applyall == True:
            for n in range(len(self.data_ydesc)):
                data_y = []
                # for m in range(len(self.data_y[n])):
                #     data_y.append(self.funccalculator(n,self.equations[n],m))
                # for n in range(self.cols,self.cols+len(self.data_ydesc)): # vector
                # self.curve[n].setData(self.data_x0[n], self.data_y0[n], pen=pg.mkPen(self.colorind[n], width=2)) # vector

    def loadclick(self):
        items = ['From DataBase', 'From File']
        dlg = QtGui.QInputDialog(self)
        item, ok = QtGui.QInputDialog.getItem(self, 'Loadtype', 'Select where to load data from:',items, 0, False)
        if ok and item:
            self.contWidget.plotbtn.setText('Start Plotting')
            self.pyqtgraphtimer.stop()
            if str(item) == 'From File':
                nameoffile = QtGui.QFileDialog.getOpenFileName(self, 'Load File')
                if any(map(lambda x: any(x), nameoffile)):
                    if isinstance(nameoffile, tuple):
                        nameoffile = str(nameoffile[0])
                    file0 = open(nameoffile, 'r')
                    filecont = file0.read()
                    fileparts = filecont.split("\n")
                    information = fileparts[0]
                    data_x = fileparts[2].split("=")[1]
                    data_y = fileparts[3].split("=")[1]
                    data_x = data_x.split('[[')[1]
                    data_y = data_y.split('[[')[1]
                    data_x = data_x.split(']]')[0]
                    data_y = data_y.split(']]')[0]
                    data_x = data_x.split('], [')
                    data_y = data_y.split('], [')

                    timeinfo = information.split("Plotting frequency: ")[1]
                    timeinfo = timeinfo.split("Hz")[0]

                    data_x_L = []
                    data_y_L = []

                    for x in data_x:
                        data_x_L.append(x.split(','))
                    for y in data_y:
                        data_y_L.append(y.split(','))

                    reply = QtGui.QMessageBox.question(self, 'Loading data', 'Enter data analysis mode?', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        self.pyqtgraphtimer.stop()
                        self.contWidget.plotbtn.setText('Start Plotting')
                        equations = []
                        for n in range(self.cols):
                            self.curve[n].clear()
                        for n in range(len(data_x)):
                            data_x_i = [float(i) for i in data_x_L[n]]
                            data_x_f = []
                            for m in range(len(data_x_i)):
                                data_x_f.append((data_x_i[m]-data_x_i[0])/float(timeinfo))
                            data_y_i = [float(i) for i in data_y_L[n]]

                            self.curve[n].setData(data_x_f, data_y_i, pen=pg.mkPen(self.colorind[n], width=2))
                            self.contWidget.plot.setXRange(data_x_f[0],data_x_f[len(data_x_f)-1])
                    else:
                        filename = nameoffile.split("/")
                        filename = filename[len(filename)-1]
                        plotW = pg.plot(title="Loaded Data from File "+str(filename[len(filename)-1]))
                        for n in range(len(data_x)):
                            data_x_i = [float(i) for i in data_x_L[n]]
                            data_x_f = []
                            for m in range(len(data_x_i)):
                                data_x_f.append((data_x_i[m]-data_x_i[0])/float(timeinfo))
                            data_y_i = [float(i) for i in data_y_L[n]]
                            plotW.plot(data_x_f,data_y_i,pen=pg.mkPen(self.colorind[n], width=2),name="Line "+str(n))
                        plotW.showGrid(x=True,y=True)
                        plotW.addLegend()
                        plotW.setLabel('bottom',information)

            elif str(item) == 'From DataBase':
                self.okflag = 0
                ittt = ArchiverCalendarWidget(self)
                ittt.exec_()
                if self.okflag == 1:
                    if self.parent.ctrl_library == "Tango":
                        items2 = ['Cassandra']
                    elif self.parent.ctrl_library == "EPICS":
                        items2 = ['EPICS']
                    elif self.parent.ctrl_library == "Finance":
                        items2 = ['YAHOO Finance']
                    item2, ok = QtGui.QInputDialog.getItem(self, 'Database Type', 'Select archiver',items2, 0, False)
                    if ok and item2:
                        stopflag = 0
                        if str(item2) == 'EPICS':
                            trystart = datetime.datetime.combine(self.startdate,self.starttime)
                            trystop = datetime.datetime.combine(self.enddate,self.stoptime)
                            trystart = trystart.strftime('%Y-%m-%dT%H:%M:%SZ')
                            trystop = trystop.strftime('%Y-%m-%dT%H:%M:%SZ')
                            archiver_url = 'http://archiver-01.tn.esss.lu.se:17668/retrieval/data/getData.json?pv={}&from={}&to={}'
                            reply = QtGui.QMessageBox.question(self, 'Customize', 'Use predefined archiver URL?\n'+archiver_url,QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                            if reply == QtGui.QMessageBox.No:
                                archiver_url_new, ok = QtGui.QInputDialog.getText(self,"Custom Archiver URL","Define the custom archiver URL")
                                try:
                                    x = []
                                    y = []
                                    data_x_i = []
                                    data_y_i = []
                                    data_x_ff = []
                                    data_x_f = []
                                    for ind, PV in enumerate(self.data_y0desc):
                                        url = archiver_url_new.format(PV,trystart,trystop)
                                        pv_page = requests.get(url)
                                        pv_rawdata = json.loads(pv_page.content)
                                        pv_value=[i['val'] for i in pv_rawdata[0]['data']]
                                        pv_time=[datetime.datetime.utcfromtimestamp(i['secs']+i['nanos']/1e9) for i in pv_rawdata[0]['data']]
                                        x.append(pv_time)
                                        y.append(pv_value)
                                        data_x_i.append(pv_time)
                                        data_x_f.append([time.mktime(xx.timetuple()) for xx in data_x_i[ind]])
                                        data_x_ff.append([datetime.datetime.fromtimestamp(value).strftime("%Y/%m/%d %H:%M:%S") for value in data_x_f[ind]])
                                        data_y_i.append([float(i) for i in y[ind]])
                                except:
                                    reply = QtGui.QMessageBox.question(self, 'Fail', 'Failed to use custom archiver url:\n'+archiver_url_new+'\nUse pre-defined one instead?',QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                            if reply == QtGui.QMessageBox.Yes:
                                x = []
                                y = []
                                data_x_i = []
                                data_y_i = []
                                data_x_ff = []
                                data_x_f = []
                                for ind, PV in enumerate(self.data_y0desc):
                                    url = archiver_url.format(PV,trystart,trystop)
                                    pv_page = requests.get(url)
                                    pv_rawdata = json.loads(pv_page.content)
                                    pv_value=[i['val'] for i in pv_rawdata[0]['data']]
                                    pv_time=[datetime.datetime.utcfromtimestamp(i['secs']+i['nanos']/1e9) for i in pv_rawdata[0]['data']]
                                    x.append(pv_time)
                                    y.append(pv_value)
                                    data_x_i.append(pv_time)
                                    data_x_f.append([time.mktime(xx.timetuple()) for xx in data_x_i[ind]])
                                    data_x_ff.append([datetime.datetime.fromtimestamp(value).strftime("%Y/%m/%d %H:%M:%S") for value in data_x_f[ind]])
                                    data_y_i.append([float(i) for i in y[ind]])

                        elif str(item2) == 'YAHOO Finance' or str(item2) == "STOOQ Finance":
                            trystart = datetime.datetime.combine(self.startdate,self.starttime)
                            trystop = datetime.datetime.combine(self.enddate,self.stoptime)
                            trystart = trystart.strftime('%Y-%m-%dT%H:%M:%SZ')
                            trystop = trystop.strftime('%Y-%m-%dT%H:%M:%SZ')
                            startd = trystart.split("T")[0].split("-")
                            endd = trystop.split("T")[0].split("-")
                            data_y_i = []
                            data_x_i = []
                            data_x_f = []
                            data_x_ff = []
                            for idx, sn in enumerate(self.sensorNames):
                                if str(item2) == "YAHOO Finance":
                                    data = pdr.get_data_yahoo(str(sn), start=datetime.datetime(int(startd[0]), int(startd[1]), int(startd[2])), end=datetime.datetime(int(endd[0]), int(endd[1]), int(endd[2])))['Close']
                                elif str(item2) == "STOOQ Finance":
                                    data = pdr.get_data_stooq(str(sn), start=datetime.datetime(int(startd[0]), int(startd[1]), int(startd[2])), end=datetime.datetime(int(endd[0]), int(endd[1]), int(endd[2])))['Close']
                                data2append = []
                                for m in range(0,len(data)):
                                    data2append.append(data[m])
                                data_y_i.append(data2append) # the list of dataframes of the stocks
                            dates = data.index.copy()
                            x = []
                            for m in range(len(dates)):
                                x.append(str(dates[m]))

                            for ind in range(0,len(x)):
                                data_x_i.append([datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S') for i in x])
                                data_x_f.append([time.mktime(xx.timetuple()) for xx in data_x_i[ind]])
                                data_x_ff.append([datetime.datetime.fromtimestamp(value).strftime("%Y/%m/%d %H:%M:%S") for value in data_x_f[ind]])

                        elif str(item2) == 'Cassandra':
                            try:
                                from Cassandra_ImportData import CassImp
                                errflag = 0
                            except:
                                errflag = 1
                                QtGui.QMessageBox.information(self,'Error', 'Cassandra Database seems to be inaccessible or not properly installed.\nCheck connection and if [ cassandra.cluster ] is properly installed.')
                            if errflag == 0:
                                x = []
                                y = []
                                data_x_i = []
                                data_y_i = []
                                data_x_ff = []
                                data_x_f = []
                                for ind, device in enumerate(self.sensorNames):
                                    dev = device.split('/')
                                    dev = '*'.join(dev)
                                    xval,yval = CassImp().readingdata(dev,str(self.startdate),str(self.enddate))
                                    x.append(xval)
                                    y.append(yval)
                                    data_x_i.append([datetime.datetime.strptime(i,'%Y-%m-%d_%H:%M:%S.%f') for i in x[ind]])
                                    data_x_f.append([time.mktime(xx.timetuple()) for xx in data_x_i[ind]])
                                    data_x_ff.append([datetime.datetime.fromtimestamp(value).strftime("%Y/%m/%d %H:%M:%S") for value in data_x_f[ind]])
                                    data_y_i.append([float(i) for i in y[ind]])
                            else:
                                stopflag = 1
                        if stopflag == 0:
                            if self.parent.archivingonly == 0:
                                reply = QtGui.QMessageBox.question(self, 'Loading data', 'Enter data analysis mode?', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                                if reply == QtGui.QMessageBox.Yes:
                                    anamode = 1
                                else:
                                    anamode = 0
                            else:
                                anamode = 1
                                self.parent.archivingonly = 0
                            if anamode == 1:
                                self.archivemode = 1
                                self.data_x0 = data_x_f
                                self.data_y0 = data_y_i[:]
                                if self.contWidget.plotbtn.text() == 'Stop Plotting':
                                    self.pyqtgraphtimer.stop()
                                    self.contWidget.plotbtn.setText('Start Plotting')
                                delays_y0 = []
                                for n in range(self.cols):
                                    self.curve[n].clear()
                                    delays_y0.append(0)
                                self.delays_y0 = delays_y0
                                for n in range(len(self.sensorNames)):
                                    if n == 0:
                                        xmin = min(data_x_f[n])
                                        xmax = max(data_x_f[n])
                                    else:
                                        if min(data_x_f[n]) < xmin:
                                            xmin = min(data_x_f[n])
                                        if max(data_x_f[n]) > xmax:
                                            xmin = min(data_x_f[n])
                                    self.curve[n].setData(data_x_f[n],data_y_i[n], pen=pg.mkPen(self.colorind[n], width=2))
                                    xtii = self.contWidget.plot.getAxis('bottom')
                                    xdict0 = dict(zip(data_x_f[0],data_x_ff[0]))
                                    xdict = dict(zip(data_x_f[n],data_x_ff[n]))
                                    xlen = len(data_x_f[0])
                                    xticks = [list(xdict0.items())[1::int(xlen*0.95)],list(xdict.items())[1::2]]
                                    xtii.setTicks(xticks)
                                self.contWidget.plot.setXRange(xmin,xmax)
                                self.contWidget.graphlbl1.setText(" ")
                            else:
                                plotW = pg.plot(title="Loaded Data from Archiver")
                                for n in range(self.cols):
                                    plotW.plot(data_x_f[n],data_y_i[n],pen=pg.mkPen(self.colorind[n], width=2),name="Line "+str(n),tickStrings = data_x_ff[n])
                                    xtii = plotW.getAxis('bottom')
                                    xdict0 = dict(zip(data_x_f[0],data_x_ff[0]))
                                    xdict = dict(zip(data_x_f[n],data_x_ff[n]))
                                    xlen = len(data_x_f[0])
                                    xticks = [list(xdict0.items())[1::int(xlen*0.95)],list(xdict.items())[1::2]]
                                    xtii.setTicks(xticks)
                                plotW.showGrid(x=True,y=True)

    def saveclick(self):
        options = QtGui.QFileDialog.Options()
        options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName = QtGui.QFileDialog.getSaveFileName(self,"QtGui.QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if any(map(lambda x: any(x), fileName)):
            if isinstance(fileName, tuple):
                fileName = str(fileName[0])
            file0 = open(fileName, 'w')
            self.toSave = str(self.data_y0)
            self.toSave = str('Date and time for save: '+str(datetime.datetime.now())+'. '+"Ylabel: "+self.ylabel+'. Plotting frequency: '+str(self.updateFrequency) + 'Hz. Plotting time range: -'+str(self.minutes*60)+'-0 s.'+'\n\n'+'x [s] = '+str(self.data_x)+'\n'+'y = '+str(self.data_y))
            file0.write(self.toSave)
            file0.close()

    def startstop(self):
        self.archivemode = 0
        if self.contWidget.plotbtn.text() == 'Start Plotting':
            self.contWidget.plotbtn.setText('Stop Plotting')
            self.pyqtgraphtimer.start(int(1000/self.updateFrequency))
            self.contWidget.plot.setXRange(-60 * 1.01 * self.minutes,0)
            if self.time_0 == -1:
                self.time_0 = time.time()
        elif self.contWidget.plotbtn.text() == 'Stop Plotting':
            self.contWidget.plotbtn.setText('Start Plotting')
            self.pyqtgraphtimer.stop()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Exit', 'Are you sure you want to exit? All plotting data will be lost.', QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            self.pyqtgraphtimer.stop()
            self.close()
        else:
            event.ignore() # Must add waveform support

class ArchiverCalendarWidget(QtGui.QDialog):
    def __init__(self, parent = PyQtGraphPlotter):
        super(ArchiverCalendarWidget, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QtGui.QGridLayout()
        self.cal1 = QtGui.QCalendarWidget(self)
        self.cal2 = QtGui.QCalendarWidget(self)
        self.cal1.setGridVisible(True)
        self.cal2.setGridVisible(True)
        self.cal1.clicked[QtCore.QDate].connect(self.showDate1)
        self.cal2.clicked[QtCore.QDate].connect(self.showDate2)
        self.cal1.setMaximumDate(QtCore.QDate(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day))
        self.cal2.setMaximumDate(QtCore.QDate(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day))
        self.starttimeHH = QtGui.QSpinBox()
        self.starttimeHH.setValue(0)
        self.starttimeHH.setMinimum(0)
        self.starttimeHH.setMaximum(23)
        self.stoptimeHH = QtGui.QSpinBox()
        self.stoptimeHH.setValue(23)
        self.stoptimeHH.setMinimum(0)
        self.stoptimeHH.setMaximum(23)
        self.starttimeMM = QtGui.QSpinBox()
        self.starttimeMM.setValue(0)
        self.starttimeMM.setMinimum(0)
        self.starttimeMM.setMaximum(59)
        self.stoptimeMM = QtGui.QSpinBox()
        self.stoptimeMM.setValue(0)
        self.stoptimeMM.setMinimum(0)
        self.stoptimeMM.setMaximum(59)
        self.starttimeSS = QtGui.QSpinBox()
        self.starttimeSS.setValue(0)
        self.starttimeSS.setMinimum(0)
        self.starttimeSS.setMaximum(59)
        self.stoptimeSS = QtGui.QSpinBox()
        self.stoptimeSS.setValue(0)
        self.stoptimeSS.setMinimum(0)
        self.stoptimeSS.setMaximum(59)

        self.okbtn = QtGui.QPushButton('Ok')
        nobtn = QtGui.QPushButton('Cancel')
        self.okbtn.clicked.connect(self.okclicked)
        nobtn.clicked.connect(self.cancelclicked)
        self.okbtn.setEnabled(False)

        self.lbl01 = QtGui.QLabel("Select start-date:")
        self.lbl02 = QtGui.QLabel("Select end-date:")

        self.lbl03 = QtGui.QLabel("Select start-time: [HH MM SS]")
        self.lbl04 = QtGui.QLabel("Select end-time: [HH MM SS]")

        layout.addWidget(self.lbl01,0,0,1,3)
        layout.addWidget(self.lbl02,0,3,1,3)
        layout.addWidget(self.cal1,1,0,1,3)
        layout.addWidget(self.cal2,1,3,1,3)
        layout.addWidget(self.lbl03,2,0,1,3)
        layout.addWidget(self.lbl04,2,3,1,3)

        layout.addWidget(self.starttimeHH,3,0,1,1)
        layout.addWidget(self.starttimeMM,3,1,1,1)
        layout.addWidget(self.starttimeSS,3,2,1,1)

        layout.addWidget(self.stoptimeHH,3,3,1,1)
        layout.addWidget(self.stoptimeMM,3,4,1,1)
        layout.addWidget(self.stoptimeSS,3,5,1,1)

        layout.addWidget(self.okbtn,4,0,1,3)
        layout.addWidget(nobtn,4,3,1,3)

        self.flag0 = 1
        self.flag1 = 1

        self.setLayout(layout)

    def showDate1(self, date):
        self.startdate = date
        self.flag0 = 0
        if self.flag1 == 0:
            self.okbtn.setEnabled(True)

    def showDate2(self, date):
        self.enddate = date
        self.cal1.setMaximumDate(date)
        self.flag1 = 0
        if self.flag0 == 0:
            self.okbtn.setEnabled(True)

    def okclicked(self):
        self.parent.startdate = self.startdate.toPyDate()
        self.parent.enddate = self.enddate.toPyDate()
        self.parent.starttime = datetime.datetime.strptime(str(str(self.starttimeHH.value())+":"+str(self.starttimeMM.value())+":"+str(self.starttimeSS.value())),'%H:%M:%S').time()
        self.parent.stoptime = datetime.datetime.strptime(str(str(self.stoptimeHH.value())+":"+str(self.stoptimeMM.value())+":"+str(self.stoptimeSS.value())),'%H:%M:%S').time()
        self.parent.okflag = 1
        self.close()

    def cancelclicked(self):
        self.parent.okflag = 0
        self.close() # Add support for EPICS and different archiving systems

class PyQtGraphSetup(QtGui.QDialog):
    def __init__(self, parent = PyQtGraphPlotter):
        super(PyQtGraphSetup, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("Settings")
        listgui = QtGui.QGridLayout()
        freqlbl = QtGui.QLabel("Plotting frequency: [Hz]")
        self.textboxF = QtGui.QDoubleSpinBox()
        self.textboxF.setValue(parent.updateFrequency)
        minulbl = QtGui.QLabel("# of minutes in spectrogram: [min]")
        self.textboxM = QtGui.QDoubleSpinBox()
        self.textboxM.setValue(parent.minutes)
        yaxilbl = QtGui.QLabel("Define the Y-label for the plot:")
        self.textboxL = QtGui.QLineEdit(parent.ylabel)
        helpbutton = QtGui.QPushButton("Help")
        equationslbl = QtGui.QPushButton("Pre-defined mathematical functions")
        equationsedit = QtGui.QPushButton("Edit user-defined mathematical functions")
        okbtn = QtGui.QPushButton('Ok')
        nobtn = QtGui.QPushButton('Cancel')
        addLineBtn = QtGui.QPushButton("Add New Line")
        rmvLineBtn = QtGui.QPushButton("Remove Line")
        self.parent.rmvList = []
        self.rmvList = []
        self.addlist = []
        self.tabs = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tabs.addTab(self.tab1,"PV:s")
        self.tabs.addTab(self.tab2,"Functions")
        self.tabgridL1 = QtGui.QGridLayout()
        self.tabgridL2 = QtGui.QGridLayout()

        self.equations = self.parent.equations[:]
        self.data_ydesc = self.parent.data_ydesc[:]
        self.delays_y0 = self.parent.delays_y0[:]
        self.delays_y = self.parent.delays_y[:]

        self.generatePVsTab()
        self.generateFunctionsTab()

        rowL = 0
        if self.parent.parent.archivingonly == 0 and self.parent.archivemode == 0:
            listgui.addWidget(freqlbl,rowL,0,1,1)
            listgui.addWidget(self.textboxF,rowL,1,1,1)
            listgui.addWidget(minulbl,rowL+1,0,1,1)
            listgui.addWidget(self.textboxM,rowL+1,1,1,1)
            rowL = 2
        listgui.addWidget(yaxilbl,rowL,0,1,1)
        listgui.addWidget(self.textboxL,rowL,1,1,1)
        rowL += 1
        listgui.addWidget(addLineBtn,rowL,1,1,1)
        listgui.addWidget(helpbutton,rowL,0,1,1)
        rowL += 1
        listgui.addWidget(equationslbl,rowL,0,1,1)
        listgui.addWidget(rmvLineBtn,rowL,1,1,1)
        rowL += 1
        listgui.addWidget(equationsedit,rowL,0,1,1)
        rowL += 1
        listgui.addWidget(self.tabs,rowL,0,1,2)
        rowL += 1
        listgui.addWidget(okbtn,rowL,0,1,1)
        listgui.addWidget(nobtn,rowL,1,1,1)

        self.setLayout(listgui)

        helpbutton.clicked.connect(self.helpclicked)
        equationslbl.clicked.connect(self.mathfunctionslist)
        addLineBtn.clicked.connect(self.addnewline)
        rmvLineBtn.clicked.connect(self.removeline)
        okbtn.clicked.connect(self.confirmfunc)
        nobtn.clicked.connect(self.cancelfunc)

    def generatePVsTab(self):
        self.eq_1_ChBoxGroup = QtGui.QGroupBox()
        self.eq_1_layout = QtGui.QGridLayout()
        self.eq_1_layout.addWidget(self.eq_1_ChBoxGroup)
        self.eq_1_layout = QtGui.QGridLayout(self.eq_1_ChBoxGroup)
        self.eq_1_layout.addWidget(QtGui.QLabel("PV"),0,0,1,1)
        self.eq_1_layout.addWidget(QtGui.QLabel("Description"),0,1,1,1)
        self.eq_1_layout.addWidget(QtGui.QLabel("Delay [s]"),0,2,1,1)
        row = 0
        for N in range(len(self.parent.data_y0desc)):
            row += 1
            textbox = QtGui.QLineEdit(str(self.parent.data_y0desc[N]), self.eq_1_ChBoxGroup)
            lbl = QtGui.QLabel(str(self.parent.devslist[N])+" (line "+str(N)+"):")
            spin = QtGui.QDoubleSpinBox()
            spin.setDecimals(9)
            spin.setRange(-1e8, 1e8) # +/- 3 years maximum
            spin.setValue(float(self.delays_y0[N]))
            self.eq_1_layout.addWidget(lbl,row,0,1,1)
            self.eq_1_layout.addWidget(textbox,row,1,1,1)
            self.eq_1_layout.addWidget(spin,row,2,1,1)
        if row < 4:
            self.tabgridL1.addWidget(self.eq_1_ChBoxGroup,0,0,1,1)
        else:
            self.scrollarea1 = QtGui.QScrollArea(self)
            self.scrollarea1.setWidgetResizable(True)
            self.scrollarea1.setWidget(self.eq_1_ChBoxGroup)
            self.tabgridL1.addWidget(self.scrollarea1,0,0,1,1)
            #listgui.addWidget(self.scrollarea,rowL,0,1,2)
        self.tab1.setLayout(self.tabgridL1)

    def generateFunctionsTab(self):
        self.eq_2_ChBoxGroup = QtGui.QGroupBox()
        self.eq_2_layout = QtGui.QGridLayout()
        self.eq_2_layout.addWidget(self.eq_2_ChBoxGroup)
        self.eq_2_layout = QtGui.QGridLayout(self.eq_2_ChBoxGroup)
        self.eq_2_layout.addWidget(QtGui.QLabel("Name"),0,0,1,2)
        self.eq_2_layout.addWidget(QtGui.QLabel("Equation"),0,2,1,1)
        self.eq_2_layout.addWidget(QtGui.QLabel("Delay [s]"),0,3,1,1)
        row = 0
        for N in range(len(self.data_ydesc)):
            row += 1
            textboxE = QtGui.QLineEdit(str(self.equations[N]), self.eq_2_ChBoxGroup)
            textboxD = QtGui.QLineEdit(str(self.data_ydesc[N]), self.eq_2_ChBoxGroup)
            lbl = QtGui.QLabel(str("(line "+str(N)+"):"))
            spin = QtGui.QDoubleSpinBox()
            spin.setDecimals(9)
            spin.setRange(-1e8, 1e8) # +/- 3 years maximum
            spin.setValue(float(self.delays_y[N]))
            textboxE.editingFinished.connect(partial(self.equationChanged,N,textboxE))
            self.eq_2_layout.addWidget(textboxD,row,0,1,1)
            self.eq_2_layout.addWidget(lbl,row,1,1,1)
            self.eq_2_layout.addWidget(textboxE,row,2,1,1)
            self.eq_2_layout.addWidget(spin,row,3,1,1)
        self.scrollarea2 = QtGui.QScrollArea(self)
        self.scrollarea2.setWidgetResizable(True)
        self.scrollarea2.setWidget(self.eq_2_ChBoxGroup)
        self.tabgridL2.addWidget(self.scrollarea2,0,0,1,1)
        self.tab2.setLayout(self.tabgridL2)

    def equationChanged(self,index,equation):
        self.equations[index] = equation.text()

    def addnewline(self):
        text1,ok1 = QtGui.QInputDialog.getText(self,"New Line","Define the name of the new line:")
        if ok1 and text1:
            if text1 in self.data_ydesc:
                QtGui.QMessageBox.information(self,'Error','Duplicate names are not allowed.')
            else:
                text2,ok2 = QtGui.QInputDialog.getText(self,"New Line","Define the equation for the new line:")
                if ok2 and text2:
                    self.delays_y.append(0)
                    self.data_ydesc.append(text1)
                    self.equations.append(text2)
                    self.addlist.append(len(self.data_ydesc)-1)
                    self.generateFunctionsTab()

    def removeline(self):
        items = self.data_ydesc
        if len(items) > 0:
            item,ok = QtGui.QInputDialog.getItem(self,"Remove lines","Which lines?",items,0,False)
            if item and ok:
                for n in range(len(self.data_ydesc)):
                    if str(item) == str(self.data_ydesc[n]):
                        ind = n
                self.delays_y.pop(ind)
                self.data_ydesc.pop(ind)
                self.equations.pop(ind)
                rmvtrue = 1
                for nn in range(len(self.addlist)):
                    if self.addlist[nn] == ind:
                        rmvind = nn
                        rmvtrue = 0
                if rmvtrue == 1:
                    for n in range(len(self.parent.data_ydesc)):
                        if str(item) == str(self.parent.data_ydesc[n]):
                            self.rmvList.append(n)
                else:
                    self.addlist.pop(rmvind)
                self.generateFunctionsTab()

    def helpclicked(self):
        QtGui.QMessageBox.information(self,'Help','RV means readvalue.')

    def mathfunctionslist(self):
        funcs = "\n".join(self.get_all_functions_from_module(math).keys())
        QtGui.QMessageBox.information(self,'Mathematical Functions', 'Pre-defined mathematical functions: \n\n'+funcs)

    def get_all_functions_from_module(self, module, functions={}):
        for f in math.__dict__:
          obj = getattr(math, f)
          if callable(obj):
           functions[f] = obj
        return functions

    def testequations(self,equation):
            if equation == 'none':
                outputval = 0
            else:
                spltA = equation.split('PV[')
                if len(spltA) > 1:
                    parts = []
                    for partA in spltA:
                        spltB = partA.split(']')
                        for partB in spltB:
                            parts.append(partB)
                    equationparts = []
                    for partC in range(len(parts)):
                        if int(partC/2) - partC/2 == 0: # even --> string
                            equationparts.append(parts[partC])
                        else: # odd --> value from PV
                            value = self.parent.data_y0[int(parts[partC])][0]
                            equationparts.append(str(value))
                    das_equation = "".join(equationparts)
                else:
                    das_equation = equation
                numexpr.evaluate(das_equation)

    def confirmfunc(self):
        descriptions_y0 = []
        delays_y0 = []
        cols1 = int(len(self.eq_1_ChBoxGroup.findChildren(QtGui.QLineEdit)) / len(self.eq_1_ChBoxGroup.findChildren(QtGui.QDoubleSpinBox))) - 1
        m = -1
        for spin in self.eq_1_ChBoxGroup.findChildren(QtGui.QDoubleSpinBox):
            delays_y0.append(float(spin.value()))
        for n, textbx in enumerate(self.eq_1_ChBoxGroup.findChildren(QtGui.QLineEdit)):
            m += 1
            if m == 0:
                descriptions_y0.append(str(textbx.text()))
            elif m == cols1:
                m = -1
        equations = []
        descriptions_y = []
        delays_y = []
        if len(self.data_ydesc) > 0:
            cols2 = int(len(self.eq_2_ChBoxGroup.findChildren(QtGui.QLineEdit)) / len(self.data_ydesc)) - 1
            m = -1
            for spin in self.eq_2_ChBoxGroup.findChildren(QtGui.QDoubleSpinBox):
                delays_y.append(float(spin.value()))
            for n, textbx in enumerate(self.eq_2_ChBoxGroup.findChildren(QtGui.QLineEdit)):
                m += 1
                if m == 0:
                    equations.append(str(textbx.text()))
                elif m == cols2:
                    m = -1
                else:
                    descriptions_y.append(str(textbx.text()))

        equationerrorflag = 0

        for ind, equation in enumerate(equations):
            try:
                self.testequations(equation)
            except:
                if equationerrorflag == 0:
                    equationerrormessage = str('Error with equations for:\n'+str(descriptions_y[ind])+"  ,  "+str(equation))
                    equationerrorflag = 1
                else:
                    equationerrormessage = str(equationerrormessage+'\n'+str(descriptions_y[ind])+"  ,  "+str(equation))
        if equationerrorflag == 1:
            QtGui.QMessageBox.information(self,'Equation error(s)', equationerrormessage)
        elif equationerrorflag == 0:
            self.parent.rmvList = self.rmvList
            self.parent.minutes = self.textboxM.value()
            self.parent.updateFrequency = self.textboxF.value()
            self.parent.ylabel = self.textboxL.text()
            self.parent.equations = equations
            self.parent.data_ydesc = descriptions_y
            self.parent.data_y0desc = descriptions_y0
            self.parent.delays_y0 = delays_y0
            self.parent.delays_y = delays_y
            self.parent.okflag = 1
            self.close()

    def cancelfunc(self):
        self.parent.okflag = 0
        self.close() # ???

class PyQtGraphContainerWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PyQtGraphContainerWidget, self).__init__(parent)
        pg.setConfigOption('background','k')
        pg.setConfigOption('foreground','w')
        self.layout = QtGui.QGridLayout()
        self.plot = pg.PlotWidget()
        self.plot.setLabel('bottom','Time [s]',color='red',size = 30)
        self.plot.showGrid(x=True,y=True)
        self.layout.addWidget(self.plot,0,0,1,7)
        self.chGroupBox = QtGui.QGroupBox()

        self.plotbtn = QtGui.QPushButton('Start Plotting')
        self.layout.addWidget(self.plotbtn, 1,0,1,1)
        self.plotsettingsbtn = QtGui.QPushButton('Plot Settings')
        self.layout.addWidget(self.plotsettingsbtn, 2,0,1,1)
        self.loadbtn = QtGui.QPushButton('Load Plot Data')
        self.layout.addWidget(self.loadbtn, 2,1,1,1)
        self.savebtn = QtGui.QPushButton('Save Plot Data')
        self.layout.addWidget(self.savebtn, 2,2,1,1)
        self.resetbtn = QtGui.QPushButton('Reset plot')
        self.layout.addWidget(self.resetbtn, 2,3,1,1)

        self.showhidelegends = QtGui.QPushButton("Show legend")
        self.layout.addWidget(self.showhidelegends, 2,6,1,1)
        self.hideshowallbtn = QtGui.QPushButton("Hide All")
        self.layout.addWidget(self.hideshowallbtn, 1,6,1,1)

        self.datapointlbl = QtGui.QLabel("Information\nDatapoint\nSelected")
        self.datapointlbl.setText("")
        self.layout.addWidget(self.datapointlbl, 1,4,2,1)

        self.graphlbl1 = QtGui.QLabel("Maximum value / from line:\n value / line")
        self.graphlbl1.setStyleSheet("font-size: 20pt")
        self.layout.addWidget(self.graphlbl1, 1,5,2,1)

        self.plot1Dbtn = QtGui.QPushButton("1D layout")
        self.plot2Dbtn = QtGui.QPushButton("2D layout")
        self.plot3Dbtn = QtGui.QPushButton("3D layout")
        self.layout.addWidget(self.plot1Dbtn, 1,1,1,1)
        self.layout.addWidget(self.plot2Dbtn, 1,2,1,1)
        self.layout.addWidget(self.plot3Dbtn, 1,3,1,1)


        self.setLayout(self.layout)

if __name__ == '__main__':
    import os, platform, sys, time, datetime, fnmatch, numexpr, math
    import numpy as np
    import pyqtgraph as pg
    from functools import partial
    import matplotlib.pyplot as plt
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
        import epics, requests, json
    elif ctrl_library == "Randomizer":
        import random
    elif ctrl_library == "Finance":
        from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
        from pandas.plotting import register_matplotlib_converters
        from pandas import DataFrame
        import pandas_datareader as pdr
    elif ctrl_library == "HistoricalData":
        import pandas_datareader as pdr
    else:
        goflag = 0
    if goflag == 1:
        window = Dialog(inp,ctrl_library)
        window.show()
        sys.exit(app.exec_()) # Works for all
