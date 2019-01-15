from tkinter import *
import serial
from serial import Serial #don't know if necessary but 
import time
#import atexit - probably not necessary (since atexit isn't anywhere else) uncomment last resort
import PIL
from PIL import ImageTk, Image
delay = 1.1



class App:
    def __init__(self, master, ser):
    
        #IMPORTANT!!!!!
        #CHANGE LINE BELOW TO WHEREVER YOU STORED THE IMAGE!!!!!!!!!!!
        #
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #-------------------------------------------------------------
        
        UBICImageFIle = "ubic logo.png"
        
        #----------------------------------------------------------------------------------
        #IMPORT CHANGE ABOVE!!!!! 
        
        img = Image.open(UBICImageFIle)
        img = img.resize((750,375),Image.ANTIALIAS)
        UBICImage = ImageTk.PhotoImage(img)
        
        
        
        self.ser  = ser
        
        #Make seq Label
        self.seqLabel = Label(master,text = "Seq:",font=("Courier", 50),bg = "maroon3")
        self.seqLabel.grid(row = 10, column = 0, columnspan=5,sticky="n")
        
        #Make title
        self.seqTitle = Label(master,text = "UCSD Monster Sequencer!",font=("Courier", 50),bg = "deep sky blue")
        self.seqTitle.grid(row = 1, column = 0, columnspan=5,sticky="n")
        
 
        #Make reset button- resets the seq label text
        self.slogan = Button(master,
                         text="Sequence New Monster",
                         command=self.write_reset, font=("Courier", 20),bg = "red3")
                         
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
        ser.write(b" ")
        
        nuc = ser.readline()
        time.sleep(delay)
        
        nuc = ser.readline()
        self.seqLabel["text"] = self.seqLabel["text"] + str(nuc)[2:-5]
        
#Set up serial port
ser = serial.Serial()
ser.port = "COM3"
#ser.port = 1
ser.baudrate = 9600
ser.timeout = 0

#open it
if ser.isOpen() == False:
  ser.open()
  
#test to make sure it connected
try:
    x = ser.read()
    print(x)

except:
    ser.close()
    
#make tinker 
root = Toplevel()
#root = Tk()
root.title("Monster Sequencer!")
root.geometry("800x500+500+300")
root.configure(bg = "deep sky blue")
root.columnconfigure(1, weight=1)
app = App(root,ser)

#keep tkinter running
root.mainloop()

ser.close()

