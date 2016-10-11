[![Build Status](https://travis-ci.org/NordicSemiconductor/nrfjprog.svg?branch=master)](https://travis-ci.org/NordicSemiconductor/nRF5-universal-prog)
[![PyPI](https://img.shields.io/pypi/l/Django.svg)](https://opensource.org/licenses/BSD-3-Clause)

# nRF5-universal-prog

Note: nRF5-universal-prog is not supported by Nordic Semiconductor. It is uploaded to GitHub to serve as a guide to using pynrfjprog/pyOCD/openOCD with nRF5 devices. However it works, and may be useful. For an officially supported, production quality, command line tool, see: https://infocenter.nordicsemi.com/index.jsp.

nRF5-universal-prog is a tool to program and debug Nordic Semiconductor's nRF5 series devices. Using a tool such as PyInstaller or py2exe this module can be converted to a stand-alone (cross-platform) executable. The user has the option to run nRF5-universal-prog without worrying about a python environment (as an exe), to run nRF5-universal-prog from python, or to use this module in their custom scripts as a higher-level alternative/supplement to pynrfjprog/pyOCD.

nRF5-universal-prog will by default assume that the PC is connected to a JLink debugger and use pynrfjprog accordingly. Add the --daplink argument to any command to tell nRF5-universal-prog that the PC is connected to a CMSIS-DAP/DAP-Link debugger and to use pyOCD instead of pynrfjprog.

Note, nRF5-universal-prog is slightly faster when running as a built executable instead of as a Python script.

# Running the .exe
1. In Releases, download the correct compressed folder for your operating system and extract it.
2. Either add the path containing 'nRF5-universal-prog.exe' to your environment variables or navigate to it's directory.
3. $ nRF5-universal-prog -h (nRF5-universal-prog.exe -h if path not added to your environment variables).
4. $ nRF5-universal-prog program -h
5. $ nRF5-universal-prog program -f PATH_TO_APP.hex -e -v -r

# Running in Python
1. Clone or download this repository and navigate to the repo's root directory ~/nRF5-universal-prog/.
2. $ python setup.py install or $ sudo pip install -r requirements.txt
  *  If installing via setup.py, the nRF5-universal-prog package will be installed in your system's Python environment.
3. $ python nrfjprog_cli.py --help
4. $ python nrfjprog_cli.py program --help
5. $ python nrfjprog_cli.py program --file PATH_TO_APP.hex --eraseall --verify --systemreset (--daplink)

# Structure
```python
nRF5-universal-prog\
  # LICENSE, README.md, setup.py and requirements.txt (used to install this module).
  nrfjprog_cli.py # Located outside the nRF5-universal-prog package so PyInstaller can build into an .exe properly. nRF5-universal-prog can be run in python with this file as well.
  nrfjprog\
    __init__.py # Package marker to make nrfjprog a module.
    __main__.py # This is where the command line interface is implemented. It parses arguments using argparse and fowards them to perform_command.py.
    nrfjprog_version.py # A global variable containing the current version number of nRF5-universal-prog.
      model\
        __init__.py # Package marker to make model a module.
        perform_command.py # Determines if a CMSIS-DAP/DAP-Link or JLink debugger is connected to the PC and fowards the command accordingly.
        perform_command_daplink.py # This is where the functionality of each command is implemented. Relies on the pyOCD module.
        perform_command_jlink.py # This is where the functionality of each command is implemented. Relies on the pynrfjprog module.
        device.py # Implements a class to represent the specs of a specific device (i.e. NRF52_FP1).
tests\
  unit_tests.py # All of the unit tests for nRF5-universal-prog.exe. Requires that dist/OS/ to be present on system which contains the built .exe for the system's OS.
```

# Architecture
```python
"""
Detailed below is how our software is stacked. Each layer depends on the layer below.
"""
nRF5-universal-prog.exe # Command line tool providing high level programming functionality for nRF5x devices.

pynrfjprog # Imports the nrfjprog DLL into Python and wraps it to be used in applications like this one or directly in scripts.
nrfjprogdll # A DLL that does some error checking and calls SEGGER's JLink API. Wraps JLink API specifically for nRF5x devices.
JLinkARMDLL # A DLL provided by SEGGER that works with SEGGER debuggers. Performs all low level operations with target device.

or, if using a CMSIS-DAP/DAP-Link debugger, then only:
pyOCD # https://github.com/mbedmicro/pyOCD.
```

# Bundling as an executable
```python
"""
PyInstaller bundles a Python application and all its dependencies into a single package and is tested against Windows, Mac OS X, and Linux. http://pythonhosted.org/PyInstaller/.
We will use PyInstaller to create an executable to distribute to the end user from our nRF5-universal-prog Python application. It will be multi platform.
Currently we bundle into a single package but we can also bundle into a single executable (one file) using PyInstaller.
"""
```
1. $ sudo pip install pyinstaller
2. Navigate to root directory of this repo and run $ pyinstaller nrfjprog_cli.py --clean --name  nRF5-universal-prog
3. Move the DLL's required by the [official nrfjprog.exe](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.tools/dita/tools/nrf5x_command_line_tools/nrf5x_nrfjprogexe.html) into ~/dist/nRF5-universal-prog/
4. Navigate to ~/dist/nRF5-universal-prog and run $ nRF5-universal-prog.exe --help
5. Add ~/dist/nRF5-universal-prog to your path and call $ nRF5-universal-prog -h from any directory.

# Coding Standard
*  https://google.github.io/styleguide/pyguide.html
*  http://www.clifford.at/style.html
*  http://semver.org/

# Future
We want nRF5-universal-prog to be flexible and open. We want it to be an option for our users all the way from development and testing to production programming.
