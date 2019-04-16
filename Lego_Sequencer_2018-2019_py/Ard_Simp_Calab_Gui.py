from tkinter import *
import serial
from serial import Serial #don't know if necessary but 
import time
#import atexit - probably not necessary (since atexit isn't anywhere else) uncomment last resort
import PIL
from PIL import ImageTk, Image
import arduino_calibrator_simple
import os
import arduino_calibrator_simple as acs
import sys

delay = 1.1



class App:
    color_reader = None
    def __init__(self, master, port = "COM3", Color_Calib_File = "Simple_Color_Calib_File.txt"):
    
        self.color_reader = acs.simple_color_determinator(port, Color_Calib_File)
        
        #UBIC file, if not finding it make sure running program from ubic logo
        #or hard code location of ubic logo
        UBICImageFIle = "ubic logo.png"
        
        img = Image.open(UBICImageFIle)
        img = img.resize((750,375),Image.ANTIALIAS)
        UBICImage = ImageTk.PhotoImage(img)
        
        
        #Make seq Label
        self.seqLabel = Label(master,text = "Seq:",font=("Courier", 50),bg = "white")
        self.seqLabel.grid(row = 10, column = 0, columnspan=5,sticky="n")
        
        #Make title
        self.seqTitle = Label(master,text = "UCSD Monster Sequencer!",font=("Courier", 50),bg = "deep sky blue")
        self.seqTitle.grid(row = 1, column = 0, columnspan=5,sticky="n")
        
 
        #Make reset button- resets the seq label text
        self.slogan = Button(master,
                         text="Sequence New Monster",
                         command=self.write_reset, font=("Courier", 20),bg = "red")
                         
        self.slogan.grid(row=5, column=0,  sticky="e")#, padx=0, pady=0)
      
        #create seq new nucleotide button. Calls write next to read color of next nuc
        self.next = Button(master,
                         text="Sequence Nucleotide",
                         command=self.write_next, font=("Courier", 20),bg = "green2")
        self.next.grid(row=5, column=4, padx=0, pady=0, sticky="n")

        
        self.UBICLabel = Label(master, image = UBICImage)
        self.UBICLabel.grid(row = 3, column = 0, columnspan = 5)
        self.UBICLabel.image = UBICImage
        
        #self.fillerLabel = Label(master, text = "      ", bg = "deep sky blue",font=("Courier", 20) )
        #self.fillerLabel.grid(row = 5, column = 2)
        
        #background 
        #self.fillerLabel2 = Label(master, text = "", bg = "deep sky blue" )
        self.fillerLabel2 = Label(master, text = "", bg = "deep sky blue" )
        self.fillerLabel2.grid(row = 6, column = 3)
        
        
    #closes connection
    def quit(self):
        ser.close()
    
    #resets text of seq
    def write_reset(self):
        self.seqLabel["text"] = "Seq:"

    #get next nucleotide from arduino and update seq text
    def write_next(self):
        
        
        color = self.color_reader.read_color()
        #time.sleep(delay)
        print(color)
        color_nuc_dict = {"Blue": "C", "Green":"G","Red": "T", "Yellow":"A","Unknown":"A"}
        nuc = color_nuc_dict[color]
        #nuc = ser.readline()
        self.seqLabel["text"] = self.seqLabel["text"] + nuc
        

    
def main ():
    #make tinker 
    root = Toplevel()
    #root = Tk()
    root.title("Monster Sequencer!")
    root.geometry("800x500+500+300")
    root.configure(bg = "deep sky blue")
    #root.configure(bg = "white")
    root.columnconfigure(1, weight=1)
    
    port = "COM3"
    calab_file = "Simple_Color_Calib_File.txt"
    
    if len(sys.argv) > 1:
        port = sys.argv[1]
    
    if len(sys.argv) > 2:
        calab_file = sys.argv[2]
        
    if not os.path.exists(calab_file):
        print ("Warning: Calibration file '%s' does not exist"%calab_file)
        print("Manual calibration will be required")
        
        
    
    app = App(root, port, calab_file)

    #keep tkinter running
    root.mainloop()
    

if __name__ == '__main__':

    main()