# Python Gui for FROG System

### Setup

This GUI is meant to communicate with an Ocean Optics (Insight) spectrometer, and a Thorlabs K-cube. This is done
through the seabreeze and thorlabs-apt packages, respectively.

To run the program you need to have the thorlabs-apt and seabreeze packages installed in your environment. After
installing seabreeze, you need to run seabreeze_os_setup in administrator mode. All this does is it copies a lot of 
.inf files for various Ocean Optics spectrometers into *C:/Windows/INF/*, the default folder where windows searches 
for drivers when a USB device is plugged in. The program may fail to install a number of drivers, however, the USB200 
and more recent USB4000 ought to work. 

Alternatively, instead of running seabreeze_os_setup, you can add the drivers yourself. To do that you should install 
omnidriver from the OceanInsight website. You will need a password to use omnidriver in developer mode, but you do 
not need that to get the drivers. After installing, all the USB drivers you will need are located in the winusb_driver 
folder in the installation directory, typically located in *C:/Program Files/Ocean Optics/OmniDriver/winusb_driver/*. 
After plugging in the spectrometer, open Device Manager and find the unknown USB device. Right click the device, go to 
properties and select Update Driver. When prompted where to search for drivers, direct it to the winusb_driver folder,
and it should detect and install the correct driver. 

In addition to installing thorlabs-apt you also need to install the Thorlabs's APT software downloadable from their
website. After installation, you need to copy the APT.dll file typically located in *C:/Program Files/Thorlabs/APT/APT
Server* into the same folder as the thorlabs_apt module for your python environment. In Anaconda/Miniconda, this 
typically would mean copying it to *.../site-packages/thorlabs_apt-0.2-py3.7.egg/thorlabs_apt/*.

Lastly, you need to have the numpy, scipy, pyqt and pyqtgraph packages installed in your environment. 
