## DynaGUI README

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


## Screenshots

DynaGUI Launcher.
<table>
    <tr>
        <td>
            <img alt="DynaGUI Launcher" src="figure2.png">
        </td>
    </tr>
</table>

DynaGUI TF.
<table>
    <tr>
        <td>
            <img alt="DynaGUI TF" src="figure4.png">
        </td>
    </tr>
</table>

DynaGUI NV and 1D plotting.
<table>
    <tr>
        <td>
            <img alt="DynaGUI NV" src="figure1.png">
        </td>
    </tr>
</table>

DynaGUI NV 2D plotting.
<table>
    <tr>
        <td>
            <img alt="DynaGUI NV 2D plotting" src="figure3.png">
        </td>
    </tr>
</table>

DynaGUI Alarms.
<table>
    <tr>
        <td>
            <img alt="DynaGUI Alarms" src="figure5.png">
        </td>
    </tr>
</table>

