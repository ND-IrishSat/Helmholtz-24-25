from tkinter import *
from tkinter import ttk
#import threading # Later will use threading for data managing 

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


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
        
        self.axises = ["x_axis", "y_axis", "z_axis"]
        self.default_magnetic_strength = "000"
        self.entry_data = {}
        self.initialize_magnetic_field()

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
                self.zero_magnetic_field()
                print("Zero mode selected")
            elif ("Manuel" in self.clicked_Mode.get()):
                self.entry_x.focus()
                print("manual mode selected")

    def Gen_Sim_ctrl(self):
        print(f"x: {self.entry_x.get()} y: {self.entry_y.get()} z: {self.entry_z.get()}")
        print("Generate Simulation")

    def initialize_magnetic_field(self):
        for axis in self.axises:
            self.entry_data[axis] = StringVar()
            self.entry_data[axis].set(self.default_magnetic_strength)

    def zero_magnetic_field(self):
        for axis in self.axises:
            self.entry_data[axis].set(self.default_magnetic_strength)

class GraphGui():
    def __init__(self, root):
        self.root = root
        #self.title("Magnetic Fields (X,Y,Z, Total")
        
        # Frame for the graph
        
        self.graph_frame = ttk.Frame(root)
        self.graph_frame.grid(row = 1, column = 1)
        
        # Create and embed the graph
        self.create_graph_X()
        self.create_graph_Y()
        self.create_graph_Z()
        self.create_graph_Tot()

        
    def create_graph_X(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([0, 1, 2, 3], [0, 1, 4, 9])
        ax.set_title("X Field")
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)
        
    def create_graph_Y(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([0, 1, 2, 3], [0, 1, 4, 9])
        ax.set_title("Y Field")
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1)

    def create_graph_Z(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([0, 1, 2, 3], [0, 1, 4, 9])
        ax.set_title("Z Field")
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)

    def create_graph_Tot(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([0, 1, 2, 3], [0, 1, 4, 9])
        ax.set_title("Total Field")
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1)

if __name__ == "__main__":
    RootGUI()
