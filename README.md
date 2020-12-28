# DynaGUI README

DynaGUI stands for Dynamic Graphical User Interface and is a method to construct temporary, permanent and/or a set of GUI:s for users in a simple and fast manner. Developed during shift works at a particle accelerator, the initial goal was to fill in some functions that were then missing: Fast dynamic construction of new control system GUI:s for various purposes.

Different devices can have different attributes, depending on what type of device it is. For example, the Beam Position Monitors (BPM:s) of a particle accelerator reveal information about the transverse beam position whilst magnets' power supplies both reads and can set the current set-point of the magnet.

The BPM:s' device servers do, however, not only reveal information about the beam itself but also contain information of how their data should be treated, such as if they may generate an interlock (InterlockEnabled) or if they should have the Automatic Gain Control enabled or disabled. These signals are handled as true or false flags, meaning that a simple GUI can be constructed to read and also control the true or false-flags. This was the initial application in the package, which is the DynaGUI TF. For simplicity reasons, their states are revealed by their colour:
True = Green
False = Red
non-valid attribute = Magenta
Device disconnected = Maroon

For the case of having a GUI that reads numerical values, each device needs two fields: A field with the domain address for the device and another with the numerical value of the defined attribute, which resulted in the second application DynaGUI NV. This application has also evolved to enable 1D and 2D plotting (showing devices along the vertical axis, time along the horizontal axis, and the values using intensity colours).

The third and last application in this package is the DynaGUI Alarms, which allows a user to set up a list of channels returning numerical values continuously and a second list of limit values (or conditions). This application sounds an alarm for the channel with a value not fulfilling the criteria and paints its description background red in the GUI. Since different devices can have different attributes, inside the DynaGUI NV and DynaGUI TF, the devices which do not have the selected attribute obtain a magenta-coloured background.

The package has then evolved to have the ability to analyse data from any file containing plot data and also live-streamed data from other sources, such as the stock market using Pandas. A random data value package has also been implemented for testing and demonstration purposes.

## Installation procedure
In order to use the PyTango package, the TANGO Controls has to be installed, then follow steps b. TANGO Controls can be obtained from https://www.tango-controls.org/downloads/.

If TANGO is not required by the end user, see steps a.

1. In order to setup this package, ensure that Python 3.x (3.7 is recommended) is installed on the computer.
2. Check Python version used with the PIP package manager such that it points to the correct Python version (pip -V).
3. a) Use PIP to install all packages required, see [requirements](requirements.yml), or use conda to create the environment:

    conda env create --file environments.yml

   b) Use PIP to install all packages required, see [requirements with PyTango](requirements_tango.yml), or use conda to create the environment:

    conda env create --file environment_tango.yml

4. If all required Python packages have been successfully installed, the package is ready.

## Getting Started
This section is a tutorial. Begin with Part 1, followed by Parts 2-4.

### Part 1: The Launcher
The package can be launched by executing `python Launcher.py` in a terminal from the package's location. Upon execution, a widget will open that looks like this:
<table>
    <tr>
        <td>
            <img alt="DynaGUI Launcher" src="figureLauncher.png">
        </td>
    </tr>
</table>
Depending on which packages are installed, different buttons will be enabled and disabled. The package that is included with Python is Random and is hence expected to always load properly, and which is hence used in the examples in this section. The ideal procedure would be if this tutorial is completed using the Random package and then repeated using the package DynaGUI is intended to be used with (EPICS, Tango or Finance) with real data acquisition.

### Part 2: The Boolean Controller (also referred to as TF)
Clicking on Boolean Controller beneath the selected package in the launcher will open a widget that looks like this:
<table>
    <tr>
        <td>
            <img alt="DynaGUI TF" src="figureTF.png">
        </td>
    </tr>
</table>
Each button represents an individual device. The status of each device with the attribute selected are indicated in the different colours discussed previously. If the state is 0 (False) or 1 (True), a signal can be sent out to the device such that the state indicated by the attribute is switched to the opposite for the device. Changing attribute can be carried out by selecting a different one from the attributes drop-down menu. Editing the device configuration is possible by clicking on Edit DynaGUI, which opens up a widget with a list of devices and another list of attributes similar to this:
<table>
    <tr>
        <td>
            <img alt="DynaGUI TF" src="figureEditTF.png">
        </td>
    </tr>
</table>

### Part 3: Value Alarms
Clicking on Value Alarms beneath the selected package in the launcher will open a widget that looks like this:
<table>
    <tr>
        <td>
            <img alt="DynaGUI Alarms" src="figureAlarms.png">
        </td>
    </tr>
</table>
Each checkbox represents a device together with an attribute, that is, the full address to a subscriptable object which returns a numerical value. The value next to it is the latest retrieved value of the object. The symbol dropdown menu can be either smaller than or larger than the expected value, which is defined in the numerical inputs to the right. To run, press the bottom button (and then press again to stop). If a row's logics condition is false, the software will notify with sound and mark the row's background red. Similar to the Boolean Controller described in Part 2, the devices can be edited and the alarm timing set by clicking on Edit DynaGUI which opens up a widget similar to this:
<table>
    <tr>
        <td>
            <img alt="DynaGUI TF" src="figureEditAlarms.png">
        </td>
    </tr>
</table>

### Part 4: Plotting (also referred to as NV)
Clicking on Plotting beneath the selected package in the launcher will open a widget that looks like the top-left widget in the figure below:
<table>
    <tr>
        <td>
            <img alt="DynaGUI NV" src="figureNV.png">
        </td>
    </tr>
</table>
This widget is the so-called DynaGUI NV widget and is used for subscribing to different device's various attributes' numerical values (scalars and waveforms/arrays), with its editing widget being equivalent to the one from the Boolean Controller described in Part 2.

From here, pressing the 1D plot button, the selected attribute will be sent for plotting together with the devices that have shown numerical values for the attribute selected. A new widget opens up that prompts the plotting frequency and number of minutes to show in the plot. Pressing Ok will open up a widget that looks like the right widget in the figure above, except for the lines. Press Start Plotting to begin the data acquisition. Clicking on Plot Settings opens up a widget similar to the bottom-left widget. Clicking on Add New Line opens up a new widget prompting for the (legend) name of the new line, followed by a widget prompting for the equation for the new line which can be a function of another or multiple other line(s).

Clicking on the 2D plot button opens up a widget that looks like this:
<table>
    <tr>
        <td>
            <img alt="DynaGUI NV 2D plotting" src="figure2D.png">
        </td>
    </tr>
</table>
This widget shows each device or waveform index along the vertical axis and the time is plotted along the horizontal axis. With this, each pixel in the plot is assigned with its unique numerical value coming from a device and/or waveform at a given point in time. This value is represented in the pixel with the colour defined by the colour-map definition (to the right in the figure above). To see the different values at a point in time, drag the yellow marker line to the position in time and click on Plot Trace, which will open up a widget that looks like this:
<table>
    <tr>
        <td>
            <img alt="DynaGUI NV 2D plotting" src="figure2Dtrace.png">
        </td>
    </tr>
</table>
The vertical axis from the 2D plot was converted to the horizontal axis, and colour intensity converted to the vertical axis.

### Part 5: Getting Started Tutorial Completion
Congratulations, you have now gone through the tutorial of all the applications of the DynaGUI package. Note that all configurations of the different applications can be saved and loaded at a later point in time. More information can be found under the next section User Guide.

## User Guide
The user guide contains more information on how to use the package, see [User Guide](UserGuide.pdf).

## Package Motivation
Package usages include multiple scenarios for simple financial analysis or at research and industrial complexes where a control system is used that can be incorporated within Python. We will address some case studies below for the different applications in this package.

The first package built was DynaGUI TF (TF = True/False) for the Tango control system with the goal to give the user a quick overview of user-defined devices' statuses of various boolean value attributes by giving each device their own button. Using colour coding for each devices' state, DynaGUI TF offers a time-efficient method for checking multiple devices' attribute states. DynaGUI TF was used a lot to check e.g. BPM statuses (e.g. is interlock enabled for them and is automatic gain control enabled). Whether they should be true or false can change over time, and therefore, it was important to check and ensure that all had proper states set.

Since the limitation with the DynaGUI TF was such that it could only read boolean values, the DynaGUI NV was developed such that numerical values could also be read. However, colour-coding cannot be used to show numerical value statuses, meaning that for this GUI, each device gets two objects, with the first being a button showing if the device is connected to and attribute is valid, if device is connected to but the attribute is not valid, or the device is disconnected (using colour-coding green, magenta and maroon, respectively.). The button can be clicked on to launch a control panel for the device or for more information about the device, whilst the second object is a label which shows the actual value (if it has been obtained). This has been used for launching control panels (AtkPanels) which are built on the Tango control system for the devices and for checking if their values are ok or not, such as the water temperatures and water flows for cooling magnets in the accelerator. It can also be used to plot the measured current from Beam Current Monitors and, by setting up user-defined functions, it can e.g. plot the difference in measured current between two (or more) beam charge monitors to monitor the beam current loss between them.

By using DynaGUI NV, the need for an alarm if a numerical value surpasses some limit was realised. Therefore, the DynaGUI Alarms application was realised as an extension to the two former applications, which was used to monitor e.g. transverse beam emittance and beam energy spread at a synchrotron. When the energy spread or emittance became higher than the user-defined limit, an alarm sounded and notified the operators.

As a future development to test the openness of DynaGUI NV and DynaGUI alarms, a "Finance" package was added to them to monitor stock prices: DynaGUI NV which monitors stock prices in a 1D plot with the ability for users to add functions that are applied to realtime stock price data, whilst DynaGUI Alarms sounds an alarm if a stock price becomes higher or lower than a user-defined limit.

## Dependencies
The package depends on multiple Python packages depending on if it is to be used with Tango, EPICS, Finance, Random, or only historical data plotting and browsing.

## History
The package was initially developed in 2019 by Benjamin Bolling during his time as an Accelerator Operator at MAX IV Laboratory. It has since then evolved to its current state as it is today.

## Comparison to other packages
Many graphical user interface (GUI) toolkits exists for building GUI:s with the Python language, e.g. PyQt, Tkinter and wxPython. All three packages, however, requires that the user does now coding and has time to build a GUI. With the idea of this package being its openness and fast-paced construction for GUI:s, a similar package would be PyGTK which, however, requires a little amount of programming. The author is presently unaware of any Python-based dynamic GUI construction package.

## License
This package is intended to be free and open-source. For more information, see [license](LICENCE.txt).
