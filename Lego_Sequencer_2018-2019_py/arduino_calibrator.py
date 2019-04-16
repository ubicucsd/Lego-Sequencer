import pandas as pd
import numpy as np
import time

import serial
from serial import Serial #don't know if necessary but 

delay = .001


        
read_serial_signal()

def send_calibration(color_range_df):

    for color in color_range_df: 
        for sig in color_range_df[color]:
            ser.write(str(color_range_df[sig,color]))
            ser.write("\n")
class simple_color_determination()

    cls_color_df = None #color samples to calibrate with
    color_det_df = None #df of color signal ranges
    ser = serial.Serial()
    debug = True
    
    def __init__ (self, port = "COM3", calibration_file = None):
        filler = "nothing yet"
        connect(port)
        
        if calibration_file == None:
            cls_color_df = get_calibration_data()
            color_det_df = simple_calibration(cls_color_df)
        
        else:
            color_det_df = pd.read_csv(calibration_file, sep = "\t", index_col = 0)
            
    def write_calibration_df (file):
        color_det_df.to_csv(file, sep = "\t")

    def connect(port = "COM3"):

        ser.port = port #May need to change port if not finding arduino.
        #ser.port = 1
        ser.baudrate = 9600
        ser.timeout = 0
        
        if ser.isOpen() == False:
            ser.open()
      
        #test to make sure it connected
        try:
            x = ser.read()
            print(x)
            print("Connection Success")
        except:
            ser.close()
            print("Connection Failed")

    def disconnect():
        ser.close()
        
        
    def read_serial_signal():

        connect()
        
        ser.write(b" ")
        #time.sleep(.6)
        ser.readline()
        
        lines = []
        for i in range(20): 
            ser.write(b" ")
            time.sleep(delay)
            line = ser.readline()
            
            if debug:
                print (line)
            
            #split line with comma and drop lines without data of interest
            line = str(line).strip().split(",")
            if len(line) < 3:
                continue
            
            #get RGB values
            line[-1] = line[-1][:-5]
            line = line[1:]
            line = [int(x.split("=")[1].strip()) for x in line]
            
            lines.append(line)
                
        if debug:
            print (lines)
            
        return lines
    def get_calibration_data(colors = ["Green", "Blue", "Red","Yellow"]):

        color_df = pd.DataFrame(columns = ["Color", "Red","Green","Blue"])

        in_color = "Starting"
        colors = colors + ["Done"]
        
        while in_color != "Done":
            in_color = input("Calibrating: type 'Blue', 'Green', 'Red' to calibrate the color or 'Done' to stop")
           
            if in_color not in colors:
                print ("Sorry, I didn't catch that. Please match the spelling exactly")
            
            elif color == "Done":
                break
                
            else:
                data = read_colors()
                for dt in data:
                    data_append = [color] + dt
                    color_df.append(data_append)
        return color_df
               
    def simple_calibration (color_df, quartile = .1, out_file = None):
        
        if type(color_df) == str:
            color_df = pd.read_csv(color_df)
        
        colors = list(set(color_df["Color"]))
        signals = "Red","Green","Blue"
        color_ranges = pd.DataFrame()
        
        for color in colors:
            
            for sig in signals:
                color_max = np.quantile(color_df[color,sig],quartile)
                color_min = np.quantile(color_df[color,sig],1-quantile)
                
                
                color_ranges.loc[color,sig + "_lower"] = color_min
                color_ranges.loc[color,sig + "_upper"] = color_max
        print (color_ranges)
        
        if out_file != none:
            color_ranges.to_csv(out_file)
            
        return color_ranges
        

    def simple_color_class (color_ranges, rgb):

        signals = ["Red", "Green", "Blue"]
        
        for color in color_ranges.index:
            
            is_color = True
            
            for sig_ind in range(len(signals)):
                
                if rgb[sig_ind] < color_ranges.loc[color,signals[sig_ind]+"_lower"]:
                    is_color = False
                    break
                        
                if rgb[sig_ind] > color_ranges.loc[color,signals[sig_ind]+"_upper"]:
                    is_color = False
                    break
                    
            if is_color:
                return color
                
                
        return "Unknown"
        
        
    def simple_colors_read (color_ranges):

        data = read_serial_signal()
        
        colors = (list(color_ranges.index))
        colors.append("Unknown")
        
        color_counter = [0]*len(colors)
        
        for line in data:
            curr_col = simple_color_class(color_range_df,line)
            color_counter[colors.index(curr_col)] += 1
        
        mode_color =  colors[color_counter.index(max(color_counter))]
        
        return mode_color
    