from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from typing import Dict
from pathlib import Path 
import csv
import numpy as np
import threading

from generateSimulation import gen_sim
from runSimulation import run_sim

#CageON = False

def run_cage(file_name, runTime, runSpeed, startPos):
    #if(CageON):
    print("RUNNING CAGE")
    run_sim(file_name, runTime, runSpeed, startPos)
      
      #CageON = False
        
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
        # Initialize instance attributes
        self.root = root
        self.serial = serial
        self.runEntry = ["runTime", "runSpeed", "startPos"]
        self.entry_data: Dict[str, StringVar] = {}
        self.fields = ["Bx","By", "Bz"]
        self.default_field = "0"
        self.entry_field_data: Dict[str, StringVar] = {}
        self.file_select = "zeroed.csv"
        self.graphs = None
        
        # Optional Graphic parameters
        self.padx = 10
        self.pady = 5

        ### Program main frames
        # Mode selection frame - TOP LEFT (row=0, column=0)
        self.frame = LabelFrame(root, text="Select Manuel or Auto", padx=5, pady=5, bg="white")
        self.label_Mode = Label(self.frame, text="Mode: ", bg="white", width=15, anchor="w")
        # Input frame - BELOW mode selection (row=1, column=0)
        self.input_frame = LabelFrame(root, text="Input Desired PWM/Field Values", padx=5, pady=5, bg="white")
        
        # Create input widgets (must happen AFTER StringVar init)
        self._create_run_widgets()
        self._create_sim_widgets()
        
        # Setup the Drop option menu and the button
        self.ModeOptionMenu()
        self.btn_Gen_Sim = Button(self.frame, text="Generate Sim", width=15, state="disabled", command=self._run_gen_sim)

        # Layout the main frames on the root window
        # Mode frame at TOP LEFT (row=0, column=0)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        
        # Input frame BELOW mode frame (row=1, column=0)
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        # Layout the widgets inside the mode frame (TOP LEFT)
        self.label_Mode.grid(column=0, row=0, sticky="w", padx=5, pady=5)
        self.btn_Gen_Sim.grid(column=0, row=1, columnspan=2, pady=10)
        self.drop_Mode.grid(column=1, row=0, padx=5, pady=5)
        
        # Set initial input state to Manual
        self._hide_input_widgets()
        self.publish_run()
        
    def _create_run_widgets(self):
        # We should implement a function for this as when changing mode i.e. Manual, Generate Sim, Run Sim.
        # They will not use the literals x, y, z but their desired magnetic field while only manual requiring
        # literal x, y, z. (Literals is a variable and it's negative: for example: x, -x)
        self._init_runSim_field()

        self.run_widgets_maps = {
            'runTime': 'Run Time:',
            'runSpeed': 'Run Speed:', 
            'startPos': 'Start Position:'
        }

        self.run_widgets: Dict[str, tuple] = {}

        for key, text in self.run_widgets_maps.items(): 
            label = Label(self.input_frame, text=text, bg="white", width=15, anchor="w")
            entry = Entry(self.input_frame, textvariable=self.entry_data[key], width=20)
            self.run_widgets[key] = (label, entry)

        # Set instance attributes for the old code to still work (_run_gen_sim uses these)
        self.label_runTime, self.entry_runTime = self.run_widgets['runTime']
        self.label_runSpeed, self.entry_runSpeed = self.run_widgets['runSpeed']
        self.label_startPos, self.entry_startPos = self.run_widgets['startPos']


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

    def _hide_input_widgets(self):
        for widgets in self.input_frame.winfo_children():
            # basically widget do not get deleted it just becomes invisible and loses its position and can be retrieve 
            widgets.grid_forget()

    def _init_runSim_field(self):
        self.entry_data["runTime"] = StringVar()
        self.entry_data["runTime"].set(40000)
        
        self.entry_data["runSpeed"] = StringVar()
        self.entry_data["runSpeed"].set(100)
        
        self.entry_data["startPos"] = StringVar()
        self.entry_data["startPos"].set(0)


    def publish_run(self):
        '''
        Method to display all the Widget of the main frame
        LEFT COLUMN LAYOUT (column=0)
        '''              
        # Internal layout for input frame
        self.label_runTime.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_runTime.grid(row=0, column=1, padx=5, pady=5)

        self.label_runSpeed.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_runSpeed.grid(row=1, column=1, padx=5, pady=5)
        
        self.label_startPos.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_startPos.grid(row=2, column=1, padx=5, pady=5)
    

    def ModeOptionMenu(self):
        '''
        Method to Get the available modes and list them into the drop menu
        '''
        # Generate the list of available modes
        # via the new requirement we will still need the mannuel mode, the zero is an addition, which should be easy
        # the generate sim will just be connecting to pysol
        modes: list[str] = ["-", "Run Simulation", "Zero", "Generate Simulation"]

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
                print("Generate Simulation mode selected")
                # Hides the existing input widgets to change
                self._hide_input_widgets()
                # Places the .csv drop box used to be self.public_sim() 
                self.drop_file.grid(column=0, row=0, padx=5, pady=5)
            elif "Zero" in self.clicked_Mode.get():
                print("Zero mode selected")
                self._hide_input_widgets()
                self.publish_run()
                
                self.entry_runTime.focus()
                
            elif "Run Simulation" in self.clicked_Mode.get():
                # Put on the grid all the elements
                self._hide_input_widgets()
                self.publish_run()

                self.entry_runTime.focus()
                print("Run Simulation mode selected")

            self.btn_Gen_Sim["state"] = "active"

        # Create graphs if they don't exist
        if self.graphs is None:
            self.graphs = GraphGui(self.root, self.serial)
            
    def file_ctrl(self):
        self.file_select = self.clicked_file.get()
        print(self.file_select)

    def _run_gen_sim(self):
        # If in "Generate Simulation" mode, you likely want to use the B-field entries (self.entry_Bx, etc.)
        
        current_mode = self.clicked_Mode.get()
    

        if "Generate Simulation" in current_mode:
            
            if self.graphs is not None:
                self.graphs.paused_serial = True
                self.serial.serial_close()
            
            print("simulation started")
            totalMagOutput, totalSimOut, realTimeVector = gen_sim(self.file_select)
            print("simulation complete")
            print(f"first item in totalMagOutput : {totalMagOutput[0]}")
            
            self.graphs.set_graph(totalMagOutput, totalSimOut, realTimeVector)
                
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
                    
            return
        elif "Run Simulation" in current_mode:
            print("Running PySol Sim")
            
            runTime = int(self.entry_runTime.get())
            runSpeed = int(self.entry_runSpeed.get())
            startPos = int(self.entry_startPos.get())
            print("Run Time (s): ", runTime/1000)
            print("Run Speed (ms/): ", runSpeed)
            print("Start Position: ", startPos)
            
            threading.Thread(target=run_cage, args=("runPySolReal.csv", runTime, runSpeed, startPos,), daemon=True).start()
            
        # Zero mode can also be handled if needed, but we'll stick to the provided structure for now
        elif "Zero" in current_mode:
            print("Zeroing field")
            runTime = 20000
            runSpeed = 100
            startPos = 0
            
            #CageON = True
            threading.Thread(target=run_cage, args=("runZeroed.csv", runTime, runSpeed, startPos,), daemon=True).start()
            
            
            


class GraphGui():
    def __init__(self, root, serial):
        '''
        Graph GUI - RIGHT SIDE of the window
        All graphs placed in column=1 (right column)
        '''
        self.root = root
        self.serial = serial
        self.paused_serial = False
        
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
        
        # Sliding window size (number of points to display)
        self.window_size = 100
        
        # Add the first chart automatically
        self.AddMasterFrame()
        self.AddGraph()
        
        # Update Chart
        self.update_plot()

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
        
    def update_plot(self):
        value = self.serial.read_value()
        print(value)
        if value is not None:
            try:
                self.xmag.append(value[0])
                self.ymag.append(value[1])
                self.zmag.append(value[2])
            except:
                print("could not append new values")
                self.xmag.append(self.xmag[len(self.xmag) - 1])
                self.ymag.append(self.ymag[len(self.ymag) - 1])
                self.zmag.append(self.zmag[len(self.zmag) - 1])
            self.time.append(len(self.time) * 0.1)
            self.tot.append( np.sqrt((self.xmag[len(self.xmag) - 1]**2) + (self.ymag[len(self.ymag) - 1]**2) + (self.zmag[len(self.zmag) - 1]**2)   ) )
            
            # keep all data but only plot the last window_size points
            start_idx = max(0, len(self.time) - self.window_size)
            time_window = self.time[start_idx:]
            xmag_window = self.xmag[start_idx:]
            ymag_window = self.ymag[start_idx:]
            zmag_window = self.zmag[start_idx:]
            tot_window = self.tot[start_idx:]

            # Show Data on graph (only last window_size points)
            self.figs[self.totalframes][1].clear()
            self.figs[self.totalframes][1].plot(time_window, xmag_window, color='green', label='X Field')
            self.figs[self.totalframes][1].plot(time_window, ymag_window, color='red', label='Y Field')
            self.figs[self.totalframes][1].plot(time_window, zmag_window, color='blue', label='Z Field')
            self.figs[self.totalframes][1].plot(time_window, tot_window, color='black', label='Total Field')
            self.figs[self.totalframes][1].legend(loc ='upper left')
            self.figs[self.totalframes][2].draw()            
        
        if not self.paused_serial:
            self.root.after(100, self.update_plot)
            
    def set_graph(self, totalMag, simMag, timeVector):
        # Show Data on graph (only last window_size points)
        self.figs[self.totalframes][1].clear()
        self.figs[self.totalframes][1].plot(timeVector, totalMag, color='green', label='Total Mag Field')
        self.figs[self.totalframes][1].plot(timeVector, simMag, color='red', label='Simulated Field')
        self.figs[self.totalframes][1].legend(loc ='upper left')
        self.figs[self.totalframes][2].draw()

if __name__ != "__main__":
    pass