from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from typing import Dict
from pathlib import Path 
import csv
import numpy as np

from generateSimulation import gen_sim

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
        # 1. Initialize instance attributes
        self.root = root
        self.serial = serial
        self.axises = ["x_pos", "x_neg", "y_pos", "y_neg", "z_pos", "z_neg"]
        self.default_pwm = "000"
        self.entry_data: Dict[str, StringVar] = {}
        self.fields = ["Bx","By", "Bz"]
        self.default_field = "0"
        self.entry_field_data: Dict[str, StringVar] = {}
        self.graphs = None
        
        # Optional Graphic parameters
        self.padx = 10
        self.pady = 5

        # Initialize the StringVars for input fields
        self.initialize_magnetic_field()
        self.initialize_desired_field()
        
        # 2. Create main frames
        # Mode selection frame - TOP LEFT (row=0, column=0)
        self.frame = LabelFrame(root, text="Select Manuel or Auto", padx=5, pady=5, bg="white")
        self.label_Mode = Label(self.frame, text="Mode: ", bg="white", width=15, anchor="w")
        
        # Input frame - BELOW mode selection (row=1, column=0)
        self.input_frame = LabelFrame(root, text="Input Desired PWM/Field Values", padx=5, pady=5, bg="white")
        
        # 3. Create input widgets (must happen AFTER StringVar init)
        self._create_manual_widgets()
        self._create_sim_widgets()
        
        # 4. Setup the Drop option menu and the button
        self.ModeOptionMenu()
        self.btn_Gen_Sim = Button(self.frame, text="Generate Sim", width=15, state="disabled", command=self.Gen_Sim_ctrl)

        # 5. Layout the main frames on the root window
        # Mode frame at TOP LEFT (row=0, column=0)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        
        # Input frame BELOW mode frame (row=1, column=0)
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        # 6. Layout the widgets inside the mode frame (TOP LEFT)
        self.label_Mode.grid(column=0, row=0, sticky="w", padx=5, pady=5)
        self.drop_Mode.grid(column=1, row=0, padx=5, pady=5)
        self.btn_Gen_Sim.grid(column=0, row=1, columnspan=2, pady=10)
        
        # 7. Set initial input state to Manual
        self._hide_input_widgets()
        self.publish_manual()
        
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
        
        self.csv_files = list(Path.cwd().glob("*.csv"))
        
        
        self.file_list = ["-"]
        for file in self.csv_files:
            self.file_list.append(file.name)
        
        print(self.file_list)
        
        self.clicked_file = StringVar()
        self.clicked_file.set(self.file_list[0])
        self.drop_file = OptionMenu(
            self.input_frame, self.clicked_file, *self.file_list, command=lambda *_: self.file_ctrl())

        self.drop_file.config(width=15)
        # Mapping from internal B-field name to external label text
#         sim_widgets_map = {
#             'Bx': 'Desired Bx:', 
#             'By': 'Desired By:', 
#             'Bz': 'Desired Bz:'
#         }
# 
#         self.sim_widgets: Dict[str, tuple] = {}
#         
#         for key, text in sim_widgets_map.items():
#             label = Label(self.input_frame, text=text, bg="white", width=15, anchor="w")
#             entry = Entry(self.input_frame, textvariable=self.entry_field_data[key], width=20)
#             self.sim_widgets[key] = (label, entry)
#         
#         # Set instance attributes for Bx, By, Bz entries for Gen_Sim_ctrl if needed
#         self.label_Bx, self.entry_Bx = self.sim_widgets['Bx']
#         self.label_By, self.entry_By = self.sim_widgets['By']
#         self.label_Bz, self.entry_Bz = self.sim_widgets['Bz']

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
        self.drop_file.grid(column=0, row=0, padx=5, pady=5)

     
        # Internal layout for input frame
#         self.label_Bx.grid(row=0, column=0, sticky="w", padx=5, pady=5)
#         self.entry_Bx.grid(row=0, column=1, padx=5, pady=5)
# 
#         self.label_By.grid(row=1, column=0, sticky="w", padx=5, pady=5)
#         self.entry_By.grid(row=1, column=1, padx=5, pady=5)
#         
#         self.label_Bz.grid(row=2, column=0, sticky="w", padx=5, pady=5)
#         self.entry_Bz.grid(row=2, column=1, padx=5, pady=5)

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
            self.frame, self.clicked_Mode, *modes, command=lambda *_: self.mode_ctrl())

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
                gen_sim( self.file_select )
                
                print("Generate Simulation mode selected")
            elif "Zero" in self.clicked_Mode.get():
                self.initialize_magnetic_field()
                self._hide_input_widgets()
                self.publish_manual()

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
            
    def file_ctrl(self):
        self.file_select = self.clicked_file.get()
        print(self.file_select)

    def Gen_Sim_ctrl(self):
        # NOTE: This method currently uses self.entry_x_p, self.entry_y_p, self.entry_z_p 
        # which are the PWM values from the Manual mode.
        # If in "Generate Simulation" mode, you likely want to use the B-field entries (self.entry_Bx, etc.)
        
        current_mode = self.clicked_Mode.get()
        data_to_write = {}

        if "Generate Simulation" in current_mode:
            gen_sim( self.file_select )
            #data_to_write = {
                #"Bx": self.entry_Bx.get(), 
                #"By": self.entry_By.get(), 
               # "Bz": self.entry_Bz.get()
            #}
        elif "Manuel" in current_mode:
            # testing using a diction to hold data; right now using just manual entries to write when it's manuel mode
            data_to_write = {
                "x_pos": self.entry_x_p.get(),
                "x_neg": self.entry_x_n.get(),
                "y_pos": self.entry_y_p.get(),
                "y_neg": self.entry_y_n.get(),
                "z_pos": self.entry_z_p.get(),
                "z_neg": self.entry_z_n.get()
            }
        # Zero mode can also be handled if needed, but we'll stick to the provided structure for now
        
        # Write to CSV only if data is available
        if data_to_write:
            with open("desired_field.csv", mode ="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # If using Generate Simulation mode, the headers should match the B-field data
                writer.writerow(["","Bx","By","Bz"])
                writer.writerow([0, data_to_write["Bx"], data_to_write["By"], data_to_write["Bz"]])
            print(f"Generate csv in {current_mode} mode with values: {data_to_write}")
        else:
             print("No data to write for selected mode.")

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