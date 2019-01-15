# Lego_Sequencer

How to run:
    The arduino should already have the color_recognizer_Space_To_continue
    script loaded. To run the GUI run python arduinoGUIScratch.py
    from this folder. This is necessary for it to find the ubic logo.
    
    packages required are:
    pyserial: Required for talking to arduino. Imported as serial in script.
    Pillow: Required for using image in gui. Imported as PIL in script.
    tkinter: Should be present by default. May be manually imported
             for linux but may be easier to reinstall python if you are
             having trouble with windows.
    
    if you do not have pyserial or Pillow, use pip to install these
    packages.
    
arduinoGUIScratch.py:
    Runs the GUI and talks to Arduino

color_recognizer_Space_To_continue.ino
    Arduino script. Should already be loaded onto the arduino.
    Can be loaded onto other arduino's to make more sequencers.
    Works by reading color for a second and taking the mode color
    detected.

color_recognizer.ino: 
    Earlier version of color_recognizer_Space_To_continue.
    Probably don't need.
    continuosly detects color.
    
color_sensor.ino:
    Original script that we copied.
    also probably not necessary.
    