from tkinter import *

from typing import Dict
from pathlib import Path 
import csv
from multiprocessing import Process

from generateSimulation import gen_sim
from runSimulation import run_sim
from Graph_GUI import GraphGui


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

        # Default Parameters for Gen Sim
        self.pidTries = 30
        self.pidDelay = 100

        self.graphs = None
        self.widget_width = 20
        self.widget_pady = self.widget_padx = 5
        self.padx = 10
        self.pady = 5

        ### Program main frames
        # Mode selection frame - TOP LEFT (row=0, column=0)
        self.frame = LabelFrame(root, text="Select Manuel or Auto", padx=5, pady=5, bg="white")
        self.label_Mode = Label(self.frame, text="Mode: ", bg="white", width=15, anchor="w")
        # Input frame - BELOW mode selection (row=1, column=0)
        self.input_frame = LabelFrame(root, text="Input Desired PWM/Field Values", padx=5, pady=5, bg="white")
        
        # Create input widgets (must happen AFTER StringVar init)
        self._init_input_fields()
        self._create_run_widgets()
        self._create_sim_widgets()
        
        # Setup the Drop option menu and the button
        self.ModeOptionMenu()
        self.btn_Gen_Sim = Button(self.frame, text="Execute", width=15, state="disabled", command=self._run_gen_sim)

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
    
    def _init_input_fields(self):
        self.entry_data["runTime"] = StringVar()
        self.entry_data["runTime"].set(10000)
        
        self.entry_data["runSpeed"] = StringVar()
        self.entry_data["runSpeed"].set(1000)
        
        self.entry_data["startPos"] = StringVar()
        self.entry_data["startPos"].set(0)

        self.entry_data["pidTries"] = StringVar()
        self.entry_data["pidTries"].set(30)
        
        self.entry_data["pidDelay"] = StringVar()
        self.entry_data["pidDelay"].set(100)
        
    def _create_run_widgets(self):
        # Goes to current working directory and find all the .csv in `run_csv/`
        self.run_csv_files = list((Path.cwd() / "run_csv").glob("*.csv"))
        self.run_file_list = ["-"]
        for file in self.run_csv_files:
            self.run_file_list.append(file.name)

        # Tinkter Objects for the interactables
        self.clicked_runfile = StringVar()
        self.clicked_file.set(self.run_file_list[0])

        self.drop_file_label = Label(self.input_frame, text="Run Sim File (csv)", bg="white", width=self.widget_width, anchor="w")
        self.drop_runfile = OptionMenu(self.input_frame, self.clicked_runfile, *self.run_file_list, command=lambda *_: self.run_file_ctrl())
        self.drop_runfile.config(width=self.widget_width)

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

        # Goes to current working directory and find all the .csv in `gen_csv/`
        self.csv_files = list((Path.cwd() / "gen_csv").glob("*.csv"))
        # Drop down file list
        self.file_list = ["-"]
        for file in self.csv_files:
            self.file_list.append(file.name)      
        # Tinkter Objects for the interactables
        self.clicked_file = StringVar()
        self.clicked_file.set(self.file_list[0])

        self.drop_file_label = Label(self.input_frame, text="Gen Sim File (csv)", bg="white", width=self.widget_width, anchor="w")
        self.drop_file = OptionMenu(self.input_frame, self.clicked_file, *self.file_list, command=lambda *_: self.gen_file_ctrl())
        self.drop_file.config(width=self.widget_width)

        self.pid_tries_label = Label(self.input_frame, text="PID Attempts (#)", bg="white", width=self.widget_width, anchor="w")
        self.pid_tries_entry = Entry(self.input_frame, textvariable=self.entry_data['pidTries'], width=self.widget_width)

        self.pid_delay_label = Label(self.input_frame, text="PID Delay (mS)", bg="white", width=self.widget_width, anchor="w")
        self.pid_delay_entry = Entry(self.input_frame, textvariable=self.entry_data['pidDelay'], width=self.widget_width)

    def gen_file_ctrl(self):
        parent = "gen_csv/"
        data = self.clicked_file.get()
        self.file_select = parent + data
        print(self.file_select)    

    def _hide_input_widgets(self):
        for widgets in self.input_frame.winfo_children():
            # basically widget do not get deleted it just becomes invisible and loses its position and can be retrieve 
            widgets.grid_forget()

    def _init_genSim_fields(self):
        pass

    def publish_run(self):
        ''' Internal layout for run simulation input frame '''
        self.input_frame.config(text="Running Simulation Parameters")

        # Internal layout for input frame
        self.label_runTime.grid(row=0, column=0, sticky="w", padx=self.widget_padx, pady=self.widget_pady)
        self.entry_runTime.grid(row=0, column=1, padx=self.widget_padx, pady=self.widget_pady)

        self.label_runSpeed.grid(row=1, column=0, sticky="w", padx=self.widget_padx, pady=self.widget_pady)
        self.entry_runSpeed.grid(row=1, column=1, padx=self.widget_padx, pady=self.widget_pady)
        
        self.label_startPos.grid(row=2, column=0, sticky="w", padx=self.widget_padx, pady=self.widget_pady)
        self.entry_startPos.grid(row=2, column=1, padx=self.widget_padx, pady=self.widget_pady)
        
        self.drop_runfile.grid(row=3, column=0, padx=self.widget_padx, pady=self.widget_pady)
    
    def publish_gen(self):
        '''Internal Layout for generate simulation input frame '''
        self.input_frame.config(text="Generate Simulation Parameters")

        self.pid_tries_label.grid(row=1, column=0, padx=self.widget_padx, pady=self.widget_pady)
        self.pid_tries_entry.grid(row=1, column=1, padx=self.widget_padx, pady=self.widget_pady)

        self.pid_delay_label.grid(row=2, column=0, padx=self.widget_padx, pady=self.widget_pady)
        self.pid_delay_entry.grid(row=2, column=1, padx=self.widget_padx, pady=self.widget_pady)

        self.drop_file.grid(row=3, column=0, padx=self.widget_padx, pady=self.widget_pady)

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
                # print("Generate Simulation mode selected")
                self._hide_input_widgets() # Places the .csv drop box used to  self.public_sim() 
                self.publish_gen() # self.drop_file.grid(column=0, row=0, padx=5, pady=5)

            elif "Zero" in self.clicked_Mode.get():
                # print("Zero mode selected")
                self._hide_input_widgets()
                self.publish_run()

                self.entry_runTime.focus()
            elif "Run Simulation" in self.clicked_Mode.get():
                # print("Run Simulation Mode Selected")
                self._hide_input_widgets()
                self.publish_run()

                self.entry_runTime.focus()
            self.btn_Gen_Sim["state"] = "active"

        # Create graphs if they don't exist
        if self.graphs is None:
            self.graphs = GraphGui(self.root, self.serial)
        
    def run_file_ctrl(self):
        parent = "run_csv/"
        data = self.clicked_runfile.get()
        self.file_select = parent + data
        print(self.file_select)

    def _run_gen_sim(self):
        # If in "Generate Simulation" mode, you likely want to use the B-field entries (self.entry_Bx, etc.)
        current_mode = self.clicked_Mode.get()

        if "Generate Simulation" in current_mode:
            # if the graph is displaying something, pause it and close the serial connection`
            # if self.graphs is not None:
            #    self.graphs.paused_serial = True
            #    self.serial.serial_close()
            
            if self.graphs is not None:
                self.graphs.paused_serial = True
            if self.serial is not None:
                self.serial.serial_close()

            '''
            runTime = int(self.entry_runTime.get())
            runSpeed = int(self.entry_runSpeed.get())
            startPos = int(self.entry_startPos.get())
            '''
            print("simulation started")
            totalMagOutput, totalSimOut, realTimeVector = gen_sim(self.file_select, pidTries=1, pidDelay=30) # file_select is updated as user choose an item from the drop down menu 
            print("simulation complete")
            # print(f"first item in totalMagOutput : {totalMagOutput[0]}")
            
            self.graphs.set_graph(totalMagOutput, totalSimOut, realTimeVector)
            
            # Write to CSV only if data is available,
            with open("run_csv/new_data.csv", mode ="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # if using generate simulation mode, the headers should match the B-field data
                writer.writerow(["","Bx","By","Bz"])
                writer.writerow([0, totalMagOutput[0], totalMagOutput[1], totalMagOutput[2]])
                print(f"Generate csv in {current_mode} mode with values: {totalMagOutput[0], totalMagOutput[1], totalMagOutput[2]}")
                    
            self.serial.serial_open()
            
        elif "Run Simulation" in current_mode:
            self.graphs.paused_serial = False
            print("Running Run Sim")
            print("Serial Flag: " , self.graphs.paused_serial)
            
            runTime = int(self.entry_runTime.get())
            runSpeed = int(self.entry_runSpeed.get())
            startPos = int(self.entry_startPos.get())
            print("Run Time (s): ", runTime/1000)
            print("Run Speed (ms/): ", runSpeed)
            print("Start Position: ", startPos)
            # copied from above - run_sim(file_name, runTime, runSpeed, startPos)
            p = Process(target=run_sim, args=(self.file_select, runTime, runSpeed, startPos))
            p.start()
            
        # Zero mode can also be handled if needed, but we'll stick to the provided structure for now
        elif "Zero" in current_mode:
            print("Zeroing field")
            runTime = 20000
            runSpeed = 100
            startPos = 0
