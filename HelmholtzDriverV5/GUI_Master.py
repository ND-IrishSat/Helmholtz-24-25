from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from typing import Dict
import csv
import numpy as np


class RootGUI():
    def __init__(self):
        '''Initializing the root GUI and other comps of the program'''
        self.root = Tk()
        self.root.title("GOAT HELMHOLTZ CAGE")
        self.root.geometry("1200x700")
        self.root.config(bg="white")
        
        # Configure grid weights for better resizing
        self.root.grid_columnconfigure(0, weight=0)  # Left column (controls) - fixed width
        self.root.grid_columnconfigure(1, weight=1)  # Right column (graphs) - expandable
        self.root.grid_rowconfigure(0, weight=1)


# Manuel/Auto Selection
class ModeGui():
    def __init__(self, root, serial):
        '''
        Initialize the mode selection GUI
        '''
        # Initializing the Widgets
        self.root = root
        self.serial = serial
        
        # Mode selection frame - TOP LEFT (row=0, column=0)
        self.frame = LabelFrame(root, text="Select Manuel or Auto", padx=5, pady=5, bg="white")
        self.label_Mode = Label(self.frame, text="Mode: ", bg="white", width=15, anchor="w")
        
        # Input frame - BELOW mode selection (row=1, column=0)
        self.input_frame = LabelFrame(root, text="Input Desired PWM/Field Values", padx=5, pady=5, bg="white")
        
        # Setup the Drop option menu
        self.ModeOptionMenu()
        
        # Mode frame at TOP LEFT (row=0, column=0)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        
        # Internal layout for mode frame
        self.label_Mode.grid(column=0, row=0, sticky="w", padx=5, pady=5)
        self.drop_Mode.grid(column=1, row=0, padx=5, pady=5)
        self.btn_Gen_Sim.grid(column=0, row=1, columnspan=2, pady=10)

        # Input frame BELOW mode frame (row=1, column=0)
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")
        
        
        self.axises = ["x_pos", "x_neg", "y_pos", "y_neg", "z_pos", "z_neg"]
        self.default_pwm = "000"
        # Typing warning; imported Dict from typing to type annotate entry_data as a diction with key: str and values: StringVar
        self.entry_data: Dict[str, StringVar] = {}
        self.initialize_magnetic_field()
        
        self.fields = ["Bx","By", "Bz"]
        self.default_field = "0"
        self.entry_field_data: Dict[str, StringVar] = {}
        self.initialize_desired_field()

        self._create_manual_widgets()
        self._create_sim_widgets()
        self._hide_input_widgets()
        self.publish_manual()
        
        

        # Add the control buttons for refreshing the COMs & Connect
        self.btn_Gen_Sim = Button(self.frame, text="Generate Sim", width=15, state="disabled", command=self.Gen_Sim_ctrl)

        # Optional Graphic parameters
        self.padx = 10
        self.pady = 5
        
        self.graphs = None

    def _create_manual_widgets(self):
        # We should implement a function for this as when changing mode i.e. Manual, Generate Sim, Run Sim.
        # They will not use the literals x, y, z but their desired magnetic field while only manual requiring
        # literal x, y, z. (Literals is a variable and it's negative: for example: x, -x)
       
        self.manual_widgets_maps = {
            'x_pos': 'X+:', 'x_neg': 'X-:', 
            'y_pos': 'Y+:', 'y_neg': 'Y-:', 
            'z_pos': 'Z+:', 'z_neg': 'Z-:'
        }

        self.manual_widgets: Dict[str, tuple] = {}

        for key, text in self.manual_widgets_maps.items(): 
            label = Label(self.input_frame, text=text, bg="white", width=15, anchor="w")
            entry = Entry(self.input_frame, textvariable=self.entry_data[key], width=20)
            self.manual_widgets[key] = (label, entry)

        # Set instance attributes for the old code to still work (Gen_Sim_ctrl uses these)
        self.label_x_p, self.entry_x_p = self.manual_widgets['x_pos']
        self.label_x_n, self.entry_x_n = self.manual_widgets['x_neg']
        self.label_y_p, self.entry_y_p = self.manual_widgets['y_pos']
        self.label_y_n, self.entry_y_n = self.manual_widgets['y_neg']
        self.label_z_p, self.entry_z_p = self.manual_widgets['z_pos']
        self.label_z_n, self.entry_z_n = self.manual_widgets['z_neg']

    def _create_sim_widgets(self):
        """Creates the 3 Label/Entry pairs for Simulation Mode (B-field inputs)."""
        # Mapping from internal B-field name to external label text
        sim_widgets_map = {
            'Bx': 'Desired Bx:', 
            'By': 'Desired By:', 
            'Bz': 'Desired Bz:'
        }

        self.sim_widgets: Dict[str, tuple] = {}
        
        for key, text in sim_widgets_map.items():
            label = Label(self.input_frame, text=text, bg="white", width=15, anchor="w")
            entry = Entry(self.input_frame, textvariable=self.entry_field_data[key], width=20)
            self.sim_widgets[key] = (label, entry)
        
        # Set instance attributes for Bx, By, Bz entries for Gen_Sim_ctrl if needed
        self.label_Bx, self.entry_Bx = self.sim_widgets['Bx']
        self.label_By, self.entry_By = self.sim_widgets['By']
        self.label_Bz, self.entry_Bz = self.sim_widgets['Bz']

    def _hide_input_widgets(self):
        for widgets in self.input_frame.winfo_children():
            # basically widget do not get deleted it just becomes invisible and loses its position and can be retrieve 
            widgets.grid_forget()

    def publish_manual(self):
        '''
        Method to display all the Widget of the main frame
        LEFT COLUMN LAYOUT (column=0)
        '''
                
        # Internal layout for input frame
        self.label_x_p.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_x_p.grid(row=0, column=1, padx=5, pady=5)

        self.label_x_n.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_x_n.grid(row=1, column=1, padx=5, pady=5)
        
        self.label_y_p.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_y_p.grid(row=2, column=1, padx=5, pady=5)
        
        self.label_y_n.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_y_n.grid(row=3, column=1, padx=5, pady=5)
        
        self.label_z_p.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.entry_z_p.grid(row=4, column=1, padx=5, pady=5)
        
        self.label_z_n.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.entry_z_n.grid(row=5, column=1, padx=5, pady=5)
        
    def public_sim(self):
        '''
        Method to display all the Widget of the main frame
        LEFT COLUMN LAYOUT (column=0)
        '''
     
        # Internal layout for input frame
        self.label_Bx.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_Bx.grid(row=0, column=1, padx=5, pady=5)

        self.label_By.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_By.grid(row=1, column=1, padx=5, pady=5)
        
        self.label_Bz.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_Bz.grid(row=2, column=1, padx=5, pady=5)

    def ModeOptionMenu(self):
        '''
        Method to Get the available modes and list them into the drop menu
        '''
        # Generate the list of available modes
        # via the new requirement we will still need the mannuel mode, the zero is an addition, which should be easy
        # the generate sim will just be connecting to pysol
        modes: list[str] = ["-", "Manuel", "Zero", "Generate Simulation"]

        self.clicked_Mode = StringVar()
        self.clicked_Mode.set(modes[0])
        self.drop_Mode = OptionMenu(
            self.frame, self.clicked_Mode, *modes, command=self.mode_ctrl)

        self.drop_Mode.config(width=15)

    def mode_ctrl(self):
        """
        Method to keep the connect button disabled if all the
        conditions are not cleared.
        """
        if "-" in self.clicked_Mode.get():
            self.btn_Gen_Sim["state"] = "disabled"
        else:
            if "Generate Simulation" in self.clicked_Mode.get():
                self._hide_input_widgets()

                self.public_sim()

                print("Generate Simulation mode selected")
            elif "Zero" in self.clicked_Mode.get():
                self.initialize_magnetic_field()
                print("Zero mode selected")
            elif "Manuel" in self.clicked_Mode.get():
                # Put on the grid all the elements
                self._hide_input_widgets()

                self.publish_manual()

                self.entry_x_p.focus()
                print("Manual mode selected")

            self.btn_Gen_Sim["state"] = "active"

        # Create graphs if they don't exist
        if self.graphs is None:
            self.graphs = GraphGui(self.root, self.serial)

    def Gen_Sim_ctrl(self):
        with open("desired_field.csv", mode ="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["","Bx","By","Bz"])
            writer.writerow([0, self.entry_x_p.get(), self.entry_y_p.get(), self.entry_z_p.get()])
        print("Generate csv")

    def initialize_magnetic_field(self):
        for axis in self.axises:
            self.entry_data[axis] = StringVar()
            self.entry_data[axis].set(self.default_pwm)
    
    def initialize_desired_field(self):
        for field in self.fields:
            self.entry_field_data[field] = StringVar()
            self.entry_field_data[field].set(self.default_field)

class GraphGui():
    def __init__(self, root, serial):
        '''
        Graph GUI - RIGHT SIDE of the window
        All graphs placed in column=1 (right column)
        '''
        self.root = root
        self.serial = serial
        
        # Container frame for all graphs - RIGHT SIDE (row=0, column=1)
        self.container_frame = Frame(root, bg="white")
        self.container_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")
        
        # Frame for the graphs
        self.frames = []
        self.figs = []
        self.ControlFrames = []
        self.totalframes = 0
        
        # Value Arrays
        self.time = []
        self.xmag = []
        self.ymag = []
        self.zmag = []
        self.tot = []
        
        # Add the first chart automatically
        self.AddChannelMaster()
        
        # Update Chart
        self.update_plot()

    def AddChannelMaster(self):
        '''Add a complete chart with controls'''
        self.AddMasterFrame()
        self.AddGraph()
        self.AddBtnFrame()

    def AddMasterFrame(self):
        '''Create a new frame for a chart'''
        self.frames.append(LabelFrame(self.container_frame, 
                                      text=f"Display Manager-{len(self.frames)+1}",
                                      pady=5, padx=5, bg="white"))
        self.totalframes = len(self.frames) - 1
        
        # Stack graphs vertically in the container
        self.frames[self.totalframes].grid(row=self.totalframes, column=0, 
                                          padx=5, pady=5, sticky="nsew")
        
        # Configure container to expand graphs
        self.container_frame.grid_rowconfigure(self.totalframes, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)

    def AddGraph(self):
        '''Setup the figure and plot for the current frame'''
        self.figs.append([])
        
        # Initialize figure
        self.figs[self.totalframes].append(plt.Figure(figsize=(8, 4), dpi=80))
        
        # Initialize the plot
        self.figs[self.totalframes].append(
            self.figs[self.totalframes][0].add_subplot(111))
        
        # Initialize the canvas
        self.figs[self.totalframes].append(FigureCanvasTkAgg(
            self.figs[self.totalframes][0], master=self.frames[self.totalframes]))

        # Place the canvas - graph on the right (column=1)
        self.figs[self.totalframes][2].get_tk_widget().grid(
            column=1, row=0, sticky="nsew")
        
        # Configure grid weights for resizing
        self.frames[self.totalframes].grid_columnconfigure(1, weight=1)
        self.frames[self.totalframes].grid_rowconfigure(0, weight=1)

    def AddBtnFrame(self):
        '''Add control buttons for the chart'''
        btnH = 2
        btnW = 4
        
        self.ControlFrames.append([])
        
        # Control frame on the left side of the graph (column=0)
        self.ControlFrames[self.totalframes].append(
            LabelFrame(self.frames[self.totalframes], pady=5, bg="white", text="Controls"))
        self.ControlFrames[self.totalframes][0].grid(
            column=0, row=0, padx=5, pady=5, sticky="n")

        # Add button
        self.ControlFrames[self.totalframes].append(
            Button(self.ControlFrames[self.totalframes][0], text="+",
                   bg="white", width=btnW, height=btnH))
        self.ControlFrames[self.totalframes][1].grid(
            column=0, row=0, padx=5, pady=5)
        
        # Remove button
        self.ControlFrames[self.totalframes].append(
            Button(self.ControlFrames[self.totalframes][0], text="-",
                   bg="white", width=btnW, height=btnH))
        self.ControlFrames[self.totalframes][2].grid(
            column=0, row=1, padx=5, pady=5)
        
    def update_plot(self):
        
        value = self.serial.read_value()
        if value is not None:
            try:
                self.xmag.append(value[0])
                self.ymag.append(value[1])
                self.zmag.append(value[2])
            except:
                self.xmag.append(self.xmag[len(self.xmag) - 1])
                self.ymag.append(self.ymag[len(self.ymag) - 1])
                self.zmag.append(self.xmag[len(self.zmag) - 1])
            self.time.append(len(self.time) * 0.1)
            self.tot.append( np.sqrt((self.xmag[len(self.xmag) - 1]**2) + (self.ymag[len(self.ymag) - 1]**2) + (self.zmag[len(self.zmag) - 1]**2)   ) )
            print(value)
            
            # Creates a window size of 100 points on the graph
            # Keep only last 100 points
            # does not work!!! do not uncomment
            # if len(self.time) > 100:
            #    self.time.pop(0)
            #    self.xmag.pop(0)
            #    self.ymag.pop(0)
            #    self.zmag.pop(0)
            #    self.tot.pop(0)

            # Show Data on graph
            self.figs[self.totalframes][1].clear()
            self.figs[self.totalframes][1].plot(self.time, self.xmag, color='green', label='X Field')
            self.figs[self.totalframes][1].plot(self.time, self.ymag, color='red', label='Y Field')
            self.figs[self.totalframes][1].plot(self.time, self.zmag, color='blue', label='Z Field')
            self.figs[self.totalframes][1].plot(self.time, self.tot, color='black', label='Total Field')
            self.figs[self.totalframes][1].legend(loc ='upper left')
            self.figs[self.totalframes][2].draw()            

        self.root.after(100, self.update_plot)

if __name__ != "__main__":
    pass