import pandas as pd
import numpy as np
import time

import serial
from serial import Serial #don't know if necessary but 

delay = .1

class simple_color_determinator():

    cls_color_df = None #color samples to calibrate with
    color_det_df = None #df of color signal ranges
    
    debug = True
    
    def __init__ (self, port = "COM3", calibration_file = None):
    
        self.ser = serial.Serial()
        self.connect(self.ser,port)
        
        if calibration_file == None:
            self.cls_color_df = self.get_calibration_data()
            self.color_det_df = self.simple_calibration(self.cls_color_df)
        
        else:
            self.color_det_df = pd.read_csv(calibration_file, sep = "\t", index_col = 0)
            
    def write_calibration_df (self,file):
        self.color_det_df.to_csv(file, sep = "\t")

    def connect(self,ser,port = "COM3"):

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

    def disconnect(self):
        ser.close()
        
        
    def read_serial_signal(self):

        #self.connect(self.ser,)
        
        self.ser.write(b' ')
        #time.sleep(.6)
        self.ser.readline()
        
        lines = []
        for i in range(20): 
            #self.ser.write(b" ")
            time.sleep(delay)
            line = self.ser.readline()
            
            if self.debug:
                print (line)
            
            #split line with comma and drop lines without data of interest
            line = str(line).strip().split(",")
            if len(line) < 3:
                continue
            
            #get RGB values
            line[-1] = line[-1][:-5]
            line = line[1:4]
            line = [int(x.split("=")[1].strip()) for x in line]
            
            lines.append(line)
                
        if self.debug:
            print (lines)
            
        return lines
    def get_calibration_data(self,colors = ["Green", "Blue", "Red","Yellow"]):

        color_df = pd.DataFrame(columns = ["Color", "Red","Green","Blue"])

        in_color = "Starting"
        colors_dict = {}
        for color in colors:
            colors_dict[color] = color
            colors_dict[color.lower()[0]] = color
            colors_dict[color.lower()] = color
        
        print(colors_dict)
        
        colors_dict["Done"] = "Done"
        
        self.ser.write(b'd')
        
        while in_color != "Done":
            print("Calibrating: type '(b)lue', '(g)reen', '(r)ed',(y)elllow to calibrate the color or 'Done' to stop")
            in_color = input()
            
            if in_color not in colors_dict:
                print ("Sorry, I didn't catch that. Please match the spelling exactly")
            
            elif in_color == "Done":
                break
                
            else:
                data = self.read_serial_signal()
                for dt in data:
                    color = colors_dict[in_color]
                    data_append = pd.DataFrame(data = ([[color] + dt]),columns = color_df.columns)
                    #data_append = [[color] + dt]
                    color_df = color_df.append(data_append,ignore_index = True)
                    
        if self.debug:
            print(color_df.head())
            print(color_df.tail())
        
        return color_df
               
    def simple_calibration (self, color_df, quartile = .1, out_file = None):
        
        if type(color_df) == str:
            color_df = pd.read_csv(color_df)
        
        colors = list(set(color_df["Color"]))
        signals = "Red","Green","Blue"
        color_ranges = pd.DataFrame()
        
        for color in colors:
            
            for sig in signals:
            
                color_max = color_df.loc[(color_df["Color"] == color), sig].max()
                color_min = color_df.loc[(color_df["Color"] == color), sig].min()
                #color_max = np.percentile(color_df.loc[(color_df["Color"] == color), sig],quartile)
                #color_min = np.percentile(color_df.loc[(color_df["Color"] == color), sig],1-quartile)
                
                #if diff between min and max small add some wiggle room
                if (color_max - color_min) < 10:
                    color_max = color_max + 5
                    color_min = color_min -5
                    
                
                color_ranges.loc[color,sig + "_lower"] = color_min
                color_ranges.loc[color,sig + "_upper"] = color_max
        
        if self.debug:
            print (color_ranges)
        
        if out_file != None:
            color_ranges.to_csv(out_file)
            
        return color_ranges
        

    def simple_color_class (self, color_ranges, rgb):

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
        
        
    def read_color (self):

    
        color_ranges =  self.color_det_df
        data = self.read_serial_signal()
        
        colors = (list(color_ranges.index))
        colors.append("Unknown")
        
        color_counter = [0]*len(colors)
        
        for line in data:
            curr_col = self.simple_color_class(color_ranges,line)
            print(curr_col)
            color_counter[colors.index(curr_col)] += 1
        
        color_counter.pop(-1) #get rid of unknown - no one cares
        mode_color = "Unknown"
        mode_color =  colors[color_counter.index(max(color_counter))]
        
        if self.debug:
            print(color_counter)
        #print(mode_color)
        return mode_color
    
    
#test = simple_color_determinator()