from tkinter import *
#from tkinter import messagebox
from tkinter import ttk
#import threading

#import matplotlib.pyplot as plt
#import numpy as np


class RootGUI():
    def __init__(self):
        '''Initializing the root GUI and other comps of the program'''
        self.root = Tk()
        self.root.title("GOAT HELMHOLTZ CAGE")
        self.root.geometry("800x600")
        self.root.config(bg="white")

# Manuel/Auto Selection
class ModeGui():
    def __init__(self, root):
        '''
        Initialize the connexion GUI and initialize the main widgets
        '''
        # Initializing the Widgets
        self.root = root
        self.frame = LabelFrame(root, text="Select Manuel or Auto", padx=5, pady=5, bg="white")
        self.label_Mode = Label(self.frame, text="Mode: ", bg="white", width=15, anchor="w")
        
        self.input_frame = LabelFrame(root, text="Input Desired Magnetic Field", padx=5, pady=5, bg="white")
        
        self.entry_data = {}
        axises = ["x_axis", "y_axis", "z_axis"]

        for axis in axises:
            self.entry_data[axis] = StringVar()
            self.entry_data[axis].set("000")

        self.label_x = Label(self.input_frame, text="X-axis: ", bg="white", width= 15, anchor="w")
        self.entry_x = Entry(self.input_frame, textvariable=self.entry_data['x_axis'])

        self.label_y = Label(self.input_frame, text="Y-axis: ", bg="white", width= 15, anchor="w")
        self.entry_y = Entry(self.input_frame, textvariable=self.entry_data['y_axis'])

        self.label_z = Label(self.input_frame, text="Z-axis: ", bg="white", width= 15, anchor="w")
        self.entry_z = Entry(self.input_frame, textvariable=self.entry_data['z_axis'])

        # Setup the Drop option menu
        self.ModeOptionMenu()

        # Add the control buttons for refreshing the COMs & Connect
        self.btn_Gen_Sim = Button(self.frame, text="Generate Sim",
                                  width=10, state="disabled", command=self.Gen_Sim_ctrl)

        # Optional Graphic parameters
        self.padx = 20
        self.pady = 5

        # Put on the grid all the elements
        self.publish()

    def publish(self):
        '''
         Method to display all the Widget of the main frame
        '''
        self.frame.grid(row=0, column=0, padx=5, pady=5)
        #  rowspan=3, columnspan=3,
        self.label_Mode.grid(column=1, row=2)
        self.drop_Mode.grid(column=2, row=2, padx=self.padx)
        self.btn_Gen_Sim.grid(column=3, row=2)

        self.input_frame.grid(row=1, column=0, padx=5, pady=5)
        # rowspan=3, columnspan=7,
        self.label_x.grid(row=1, column=1)
        self.entry_x.grid(row=1, column=2)
        self.label_y.grid(row=2, column=1)
        self.entry_y.grid(row=2, column=2)
        self.label_z.grid(row=3, column=1)
        self.entry_z.grid(row=3, column=2)
        

    def ModeOptionMenu(self):
        '''
         Method to Get the available COMs connected to the PC
         and list them into the drop menu
        '''
        # Generate the list of available coms
        modes = ["-", "Auto (PySol)", "Zero", "Manuel"]

        self.clicked_Mode = StringVar()
        self.clicked_Mode.set(modes[0])
        self.drop_Mode = OptionMenu(
            self.frame, self.clicked_Mode, *modes, command=self.mode_ctrl)

        self.drop_Mode.config(width=10)

    def mode_ctrl(self, widget):
        '''
        Mehtod to keep the connect button disabled if all the
        conditions are not cleared
        '''

        if ("-" in self.clicked_Mode.get()):
            self.btn_Gen_Sim["state"] = "disabled"            
        else:
            self.btn_Gen_Sim["state"] = "active"
            if ("Auto" in self.clicked_Mode.get()):
                print("Auto mode selected")
            elif ("Zero" in self.clicked_Mode.get()):
                print("Zero mode selected")
            elif ("Manuel" in self.clicked_Mode.get()):
                self.entry_x.focus()
                print("manual mode selected")

    def Gen_Sim_ctrl(self):
        print(self.entry_x.get())
        print("Generate Simulation")

if __name__ == "__main__":
    RootGUI()
