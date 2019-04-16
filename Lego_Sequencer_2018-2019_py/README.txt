How to run:

The arduino should already have the code necessary to run it
otherwise you will need to download the arduino IDE and recompile
the appropriate code onto the arduino.
    To run the GUI run:
    python Ard_Simp_Calab_Gui.py <port> <Calibration File>
    from this folder. This is necessary for it to find the ubic logo.
    Note the default port is usually COM3 but if you are having 
    trouble finding the right port you can go to device manager on
    windows to find it.
    
packages required are:
    pyserial: Required for talking to arduino. Imported as serial in script.
    Pillow: Required for using image in gui. Imported as PIL in script.
    tkinter: Should be present by default. May be manually imported
             for linux but may be easier to reinstall python if you are
             having trouble with windows.
             
    pandas: Required for loading the calabration file
    
    if you do not have pyserial or Pillow, use pip to install these
    packages.
    
If the arduino is not detecting the colors correctly you can change the
calabration files till it does.