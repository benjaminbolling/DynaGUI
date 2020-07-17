# DynaGUI test procedures
A manual testing procedure for the DynaGUI package.

## Test 0: The DynaGUI Launcher
First test to be done is to ensure that the launcher works as it is supposed to, which can be accomplished by launching a terminal, browsing to the location of the DynaGUI package and then executing | python Launcher.py |. From the launcher window, the three applications DynaGUI TF, DynaGUI Alarms and DynaGUI NV can be launched for the 4 different packages Tango, EPICS, Random and Finance. The Data Viewer package is not yet in a ready stage.


## Test 1: DynaGUI TF
Launch DynaGUI TF from the launcher for Tango (requires PyTango) or EPICS (requires PyEpics). If none of these packages are available and no devices are connectable, the testing package "Random" can be used. To launch DynaGUI TF, select Boolean Controller for the package to test it with.

In the DynaGUI TF, clicking on any item will make it change state if its colour is red or green. Select any attribute in the top combobox to change which attributes to observe (note that for Random it is not possible to view states for different attributes as there are no devices to communicate with).

The DynaGUI TF devices and attributes can be edited by pressing "Edit DynaGUI". Test the GUI editing by adding, editing and/or removing devices and attributes in their respective list. Change maximum number of rows and select or deselect the "Show the Enable All button" checkbox. Press Ok to confirm or Cancel. 

To save a configuration, press "Save" and select location and filename. The file format for DynaGUI TF configurations is '.dg1'. Confirm file configuration saving and loading methods by closing DynaGUI TF, launching DynaGUI TF again and then loading the file that was saved.

Finally, pressing update statuses fetches the current values of all devices having the specified attribute (except for the Random package).


## Test 2: DynaGUI Alarms
Launch DynaGUI Alarms from the launcher for Tango (requires PyTango), EPICS (requires PyEpics), Finance or Random. To launch DynaGUI Alarms, press Value Alarms for the package to test it with. Press the Edit DynaGUI-button to get to the GUI's editing screen, one column has the full device addresses (incl. the attribute) whilst the other one has a description for each respective device address. Hence, ensure both have the same number of rows (otherwise it will not be possible to proceed). Then select number of rows for the GUI and the alarms timer (time between each sweep), and press Ok to proceed or Cancel.

Test selecting and deselecting alarms, and try the Select All button and Unselect All button. Press the bottom button to begin monitoring the alarms with the defined alarm timer defined (green means it is monitoring, red that it is not monitoring). Edit the values next to the alarm descriptions for testing if the alarms are activated or not. The 'larger than'- and 'smaller than'-signs represent how the values should be (for smaller than sign, the read value has to be smaller than the limit, and vice versa). If this condition is not valid, an alarm will sound that reads the alarm description and "in alarm". The last alarm is also shown as a text together with a time stamp. The background colour is coded as following:

- Green: Ok
- Red: Alarm
- Grey: Skipped

The last things to test is saving and loading a DynaGUI Alarms configuration file, which can be done by pressing "Save". Define the filename and its location. Confirm by closing the DynaGUI Alarms application and then loading the saved file by pressing "Load" and browsing to the file.


## Test 3.1: DynaGUI NV
Launch DynaGUI NV from the launcher for Tango (requires PyTango), EPICS (requires PyEpics), Finance or Random. To launch DynaGUI NV, press Plotting for the package to test it with. Begin by repeating the above described test for DynaGUI TF in terms of editing the DynaGUI layout and then saving and loading the configurations. The "Get all attributes" function is currently only available for the Tango and Random packages. For Random, it generates 5 "random" attributes. For Tango, it obtains a list of all attributes for all devices whilst making sure that no duplicates exist. Press Update statuses to fetch the latest values for all devices or stocks.

## Test 3.2: DynaGUI 2D plotting
The next thing to test is the 2D plotting feature, which can be launched by pressing the "2D Plot" button. Define the plotting frequency and number of minutes to show in the spectrogram. There is still a bug with the intensity mapping, so one has to pull e.g. the top bar up or down slightly on the colour map intensity settings on the top-right side. Press start to begin plotting values. To edit the colormap, press Edit CM and select which CM colour to change (CM1-CM3: CM1 = zero-level value (black), CM2 = middle-level value (green), CM3 = high-level value (red)). The intensity setting can be edited by the user (change size of it, where the zero-level value is, and where the top-level value is). Scroll with the mouse hovering above it to zoom in/out the intensity map or the spectrogram. To reset zoom, right-click in the intensity settings or the spectrogram and select all. 

To plot the values at a specific time, press pause, drag the marker (located to the right in the spectrogram) to a point in time, and press plot trace. To plot the change over time rather than the intensity, press "Plotting real values" and it will change its text to "Plotting vs stored". It will then store the current values as reference values and plot all future values in the spectrogram with respect to the reference values (value = read-value - reference value). New reference values can be taken by clicking on "Store current position".

## Test 3.3: DynaGUI 1D plotting
The next thing to test is the 1D plotting feature, which can be launched by pressing the "1D Plot" button. Define the plotting frequency and number of minutes to show in the plot. To start plotting, press "Start Plotting". It will then change text to "Stop Plotting", which has to be clicked in order to pause the plotting and to be able to change plot settings or load plot data. Press Reset Plot to get rid of all plotted data (it will prompt you if you are really sure about this).

The saving and loading plot data needs more work and is not considered as in a ready state yet (and are hence disabled). The 1D/2D/3D-Layout buttons are also disabled and will in the future give the user a possibility to switch directly between a 1D Plot, 2D Plot and 3D Plot layouts.

Under Plot Settings, change the Plotting Frequency, number of minutes for the spectrogram, and the label of the vertical axis. In here, you can add new lines defined by you. Press Add New Line, define the name of it (no spaces and avoid using other characters than underscores),  e.g. myline_1, and press OK. Now define the equation of the new line. To use the values of other lines, type "PV[x]" where x is the number of the line to include (shown in parenthesis, e.g. line 8 means that x should be 8). Example equations to try out:

	2+PV[0]
	PV[1]-PV[2]
	sin(PV[3]-PV[4])

Add as many lines as you want, and press on the "Functions" tab to see all your lines. To remove a line, press "Remove Line" and select the line to remove. To see all mathematical functions available, press "Pre-defined mathematical functions". In a future version, the "user-defined mathematical functions" will also be available (e.g., func1(x) = x^2 + 3*x). Delays can also be defined for the lines (both negative and positive). Note that for user defined functions, the delays of the read-values are not taken into account (they use simply the last value) but will be fixed in a future version. Press Ok to confirm the new plot settings or Cancel. Select if the horizontal axis of the plot should be rescaled or not (e.g. select yes), and if you want the equations/functions to be applied on the previous values in the plot (e.g. select yes). Now start plotting. Press Show legend to see all the lines and also your new lines in the end. Press Hide All to hide all lines (which will change label to Show All that can be pressed to show all the lines). Lines can also be shown or hidden by selecting or unselecting their respective checkboxes. Line colours can be changed by pressing the colour-box next to each line's checkbox (using RGB). Test: Hide all lines. Select to show "myline_1". Press its colour box, type | 0, 255, 255 | and press Ok. The line should now be cyan.





