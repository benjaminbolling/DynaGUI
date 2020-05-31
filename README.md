####################################################################################################

					   DynaGUI README

####################################################################################################

This document serves as a complement to the main by including instructions on:

1. Pre-requirements
2. Installation procedure
3. How to use

####################################################################################################

					- Pre-requirements -

Minimum requirements:
	- Git	(https://www.atlassian.com/git/tutorials/install-git)
	- Python (stability checked on version 3.7)
	- Python packages
		- numexpr		https://pypi.org/project/numexpr/
		- numpy 		https://pypi.org/project/numpy/
		- pyqtgraph		https://pypi.org/project/pyqtgraph/
		- functools		https://pypi.org/project/functools/
		- matplotlib		https://pypi.org/project/matplotlib/
		- PyQt5 (or PyQt4)	https://pypi.org/project/PyQt5/

For Tango control systems, the following Python package is required:
	- PyTango		https://pypi.org/project/pytango/

For EPICS (Experimental Physics and Industrial Control System):
	- PyEpics		https://pypi.org/project/pyepics/
	- Requests		https://pypi.org/project/requests/

For the Finance analysis package:
	- Pandas		https://pypi.org/project/pandas/
	- Pandas Datareader	https://pypi.org/project/pandas-datareader/

####################################################################################################

				     - Installation procedure -

1. Ensure that Git is installed on the computer, see https://www.atlassian.com/git/tutorials/install-git.
2. Create a new folder on the computer called "DynaGUI".
3. Open a terminal in the DynaGUI folder.
4. Clone the package to the folder by executing the following command in the terminal:
	git clone https://github.com/benjaminbolling/DynaGUI.git
5. To run the application, execute the following command in a terminal in the DynaGUI folder:
	python3.7 Launcher.py



