from tkinter import *
#from tkinter import messagebox
#from tkinter import ttk
#import threading

#import matplotlib.pyplot as plt
#import numpy as np


class RootGUI():
    def __init__(self):
        '''Initializing the root GUI and other comps of the program'''
        self.root = Tk()
        self.root.title("GOAT HELMHOLTZ CAGE")
        self.root.geometry("360x120")
        self.root.config(bg="white")

# Manuel/Auto Selection
class ModeGui():
    def __init__(self, root):
        '''
        Initialize the connexion GUI and initialize the main widgets
        '''
        # Initializing the Widgets
        self.root = root
        self.frame = LabelFrame(root, text="Select Manuel or Auto",
                                padx=5, pady=5, bg="white")
        self.label_Mode = Label(
            self.frame, text="Mode: ", bg="white", width=15, anchor="w")

        # Setup the Drop option menu
        self.ModeOptionMenu()

        # Add the control buttons for refreshing the COMs & Connect
        self.btn_Gen_Sim = Button(self.frame, text="Generate Sim",
                                  width=10,  command=self.Gen_Sim_ctrl)

        # Optional Graphic parameters
        self.padx = 20
        self.pady = 5

        # Put on the grid all the elements
        self.publish()

    def publish(self):
        '''
         Method to display all the Widget of the main frame
        '''
        self.frame.grid(row=0, column=0, rowspan=3,
                        columnspan=3, padx=5, pady=5)
        self.label_Mode.grid(column=1, row=2)

        self.drop_Mode.grid(column=2, row=2, padx=self.padx)

        self.btn_Gen_Sim.grid(column=3, row=2)

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
        print("Mode Set")
        # Checking the logic consistency to keep the connection btn
#         if "-" in self.clicked_Mode.get():
#             self.btn_Gen_Sim["state"] = "disabled"
#         else:
#             self.btn_Gen_Sim["state"] = "active"
    def Gen_Sim_ctrl(self):
        print("Generate Simulation")

if __name__ == "__main__":
    RootGUI()
    ComGui()