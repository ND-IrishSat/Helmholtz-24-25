import threading
from pathlib import Path
from tkinter import *

from cage_hardware import CageHardware
from generateSimulation import gen_sim
from Graph_GUI import GraphGui
from runSimulation import run_sim


class RootGUI:
    def __init__(self):
        '''Initializing the root GUI and other comps of the program'''
        self.root = Tk()
        self.root.title("HELMHOLTZ CAGE")
        self.root.geometry("1200x700")
        self.root.config(bg="white")
        
        # Configure grid weights for better resizing
        self.root.grid_columnconfigure(0, weight=0)  # Left column (controls) - fixed width
        self.root.grid_columnconfigure(1, weight=1)  # Right column (graphs) - expandable
        self.root.grid_rowconfigure(0, weight=1)

# Manuel/Auto Selection
class ModeGUI:
    def __init__(self, root: RootGUI, cage: CageHardware):
        '''Initialize the mode selection GUI.'''
        self.root = root
        self.cage = cage

        # Active worker tracking (fresh event created per task)
        self._worker_thread: threading.Thread | None = None
        self._stop_event: threading.Thread | None = None

        self.runEntry = ["runTime", "runSpeed", "startPos"]
        self.entry_data: dict[str, StringVar] = {}
        self.fields = ["Bx","By", "Bz"]
        self.default_field = "0"
        self.entry_field_data: dict[str, StringVar] = {}
        self.file_select = "zeroed.csv"

        # Default Parameters for Gen Sim
        self.pidTries = 30
        self.pidDelay = 100
        
        self.run_clicked_file = StringVar()
        self.clicked_file = StringVar()

        self.graphs = None
        self.widget_width = 20
        self.widget_pady = self.widget_padx = 5
        self.padx = 10
        self.pady = 5

        # Program Main Frames - TOP LEFT (row=0, column=0)
        self.frame          = LabelFrame(self.root, text="Select Manuel or Auto", padx=5, pady=5, bg="white")
        self.label_Mode     = Label(self.frame,     text="Mode: ", bg="white", width=15, anchor="w")
        # Input frame - BELOW mode selection (row=1, column=0)
        self.input_frame    = LabelFrame(self.root, text="Input Desired PWM/Field Values", padx=5, pady=5, bg="white")
        
        # Create input widgets (must happen AFTER StringVar init)
        self._init_input_fields()
        self._create_run_widgets()
        self._create_sim_widgets()
        
        # Setup the Drop option menu and the button
        self.ModeOptionMenu()
        self.btn_Gen_Sim    = Button(self.frame, text="Execute", width=12, state="disabled", command=self._execute_mode)
        self.btn_Stop_Sim   = Button(self.frame, text="Stop", width=12, state="disabled", command=self.stop_active_task)

        # Layout the main frames on the root window
        # Mode frame at TOP LEFT (row=0, column=0)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        
        # Layout the main frames on the root window
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        # Layout the widgets inside the mode frame
        self.label_Mode.grid(column=0, row=0, sticky="w", padx=5, pady=5)
        self.drop_Mode.grid(column=1, row=0, padx=5, pady=5)
        self.btn_Gen_Sim.grid(column=0, row=1, pady=10, padx=5)
        self.btn_Stop_Sim.grid(column=1, row=1, pady=10, padx=5)

        # Ensure clean shutdown when window closes
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set initial input state to Manual
        self._hide_input_widgets()
        self.publish_run()

    #############################
    # Worker Threads Management #
    #############################

    def stop_active_task(self) -> None:
        """Signals only the active worker thread to exit; CageHardware stays open."""
        if self._stop_event is not None:
            self._stop_event.set()
        if self._worker_thread is not None and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=2.0)

        self._stop_event = None
        self._worker_thread = None
        self.btn_Stop_Sim["state"] = "disabled"
        if "-" not in self.clicked_Mode.get():
            self.btn_Gen_Sim["state"] = "active"

    def _launch_worker(self, target, args: tuple, kwargs: dict | None = None) -> None:
        """Stops any running task, allocates a fresh Event, and starts a daemon thread."""
        self.stop_active_task()

        stop_event = threading.Event()
        worker = threading.Thread(
            target=target,
            args=(self.cage, stop_event, *args),
            kwargs=kwargs or {},
            daemon=True,
        )
        self._stop_event = stop_event
        self._worker_thread = worker
        self.btn_Stop_Sim["state"] = "active"
        worker.start()

    def on_close(self) -> None:
        """Stops active simulation workers and closes hardware ports cleanly."""
        self.stop_active_task()
        self.cage.shutdown()
        self.root.destroy()

    #############################
    # UI Setup & Mode Switching #
    #############################
    
    def _hide_input_widgets(self):
        ''' To not have to waste resources on recreating widget, to hide widgets we can unmap them temporarily '''
        for widgets in self.input_frame.winfo_children():
            widgets.grid_forget()
            
    def _init_input_fields(self):
        self.entry_data["runTime"]  = StringVar(value="10000")
        self.entry_data["runSpeed"] = StringVar(value="1000")
        self.entry_data["startPos"] = StringVar(value="0")
        self.entry_data["pidTries"] = StringVar(value="30")
        self.entry_data["pidDelay"] = StringVar(value="100")
        
    def _get_gen_file_path(self):
        data = self.clicked_file.get()
        self.file_select = f"gen_csv/{data}"
        print(f"[Mode_GUI/_get_gen_file_path]: {self.file_select}")
    
    def _get_run_file_path(self):
        data = self.run_clicked_file.get()        
        self.file_select = f"run_csv/{data}"
        print(f"[Mode_GUI/_get_run_file_path]: {self.file_select}")
        
    def _create_run_widgets(self):
        ''' Goes to curr. wd and retrives every csv file in `run_csv/` '''
        self.run_csv_files = list((Path.cwd() / "run_csv").glob("*.csv"))
        self.run_file_list = ["-"] + [file.name for file in self.run_csv_files]
        self.run_clicked_file.set('-')

        self.drop_runfile_label = Label(
            self.input_frame, text="Run Sim File (csv)", bg="white", width=self.widget_width, anchor="w"
        )
        self.drop_runfile = OptionMenu(
            self.input_frame, self.run_clicked_file, *self.run_file_list, command=lambda *_: self._get_run_file_path()
        )
        self.drop_runfile.config(width=self.widget_width)
        
        self.run_widgets_maps = {
            'runTime': 'Run Time:',
            'runSpeed': 'Run Speed:', 
            'startPos': 'Start Position:'
        }

        self.run_widgets: dict[str, tuple] = {}
        for key, text in self.run_widgets_maps.items(): 
            label = Label(self.input_frame, text=text, bg="white", width=15, anchor="w")
            entry = Entry(self.input_frame, textvariable=self.entry_data[key], width=20)
            self.run_widgets[key] = (label, entry)

        # Set instance attributes for the old code to still work (_run_gen_sim uses these)
        self.label_runTime,  self.entry_runTime = self.run_widgets['runTime']
        self.label_runSpeed, self.entry_runSpeed = self.run_widgets['runSpeed']
        self.label_startPos, self.entry_startPos = self.run_widgets['startPos']

    def _create_sim_widgets(self):
        ''' Goes to curr. wd and retrives every csv file in `gen_csv/` '''
        self.csv_files = list((Path.cwd() / "gen_csv").glob("*.csv"))
        self.file_list = ["-"] + [file.name for file in self.csv_files]
        self.clicked_file.set('-')

        self.drop_file_label = Label(
            self.input_frame, text="Gen Sim File (csv)", bg="white", width=self.widget_width, anchor="w"
        )
        self.drop_file = OptionMenu(
            self.input_frame, self.clicked_file, *self.file_list, command=lambda *_: self._get_gen_file_path()
        )
        self.drop_file.config(width=self.widget_width)
        # Additional Information for Simulation Configurations
        self.pid_tries_label = Label(
            self.input_frame, text="PID Attempts (#)", bg="white", width=self.widget_width, anchor="w"
        )
        self.pid_tries_entry = Entry(
            self.input_frame, textvariable=self.entry_data['pidTries'], width=self.widget_width
        )
        self.pid_delay_label = Label(
            self.input_frame, text="PID Delay (ms, min 65) ", bg="white", width=self.widget_width, anchor="w"
        )
        self.pid_delay_entry = Entry(
            self.input_frame, textvariable=self.entry_data['pidDelay'], width=self.widget_width
        )

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

        self.drop_runfile_label.grid(row=3, column=0, padx=self.widget_padx, pady=self.widget_pady)
        self.drop_runfile.grid(row=3, column=1, padx=self.widget_padx, pady=self.widget_pady)
    
    def publish_gen(self):
        '''Internal Layout for generate simulation input frame '''
        self.input_frame.config(text="Generate Simulation Parameters")

        self.pid_tries_label.grid(row=1, column=0, padx=self.widget_padx, pady=self.widget_pady)
        self.pid_tries_entry.grid(row=1, column=1, padx=self.widget_padx, pady=self.widget_pady)

        self.pid_delay_label.grid(row=2, column=0, padx=self.widget_padx, pady=self.widget_pady)
        self.pid_delay_entry.grid(row=2, column=1, padx=self.widget_padx, pady=self.widget_pady)

        self.drop_file_label.grid(row=3, column=0, padx=self.widget_padx, pady=self.widget_pady)
        self.drop_file.grid(row=3, column=1, padx=self.widget_padx, pady=self.widget_pady)

    def ModeOptionMenu(self):
        '''
        Method to Get the available modes and list them into the drop menu. 
        Generate the list of available modes via the new requirements we 
        will still need the manual mode, the zero is an addition, which 
        should be easy, the generate sim will just be connecting to PySol
        '''
        modes: list[str] = ["-", "Run Simulation", "Zero", "Generate Simulation"]
        self.clicked_Mode = StringVar(value=modes[0])

        self.drop_Mode = OptionMenu(self.frame, self.clicked_Mode, *modes, command=lambda *_: self.mode_ctrl())
        self.drop_Mode.config(width=15)      

    def mode_ctrl(self):
        """
        Method to keep the connect button disabled if all the
        conditions are not cleared.
        """
        self.stop_active_task()
        selected = self.clicked_Mode.get()
        if "-" in selected:
            self.btn_Gen_Sim["state"] = "disabled"
        else:
            # Places the .csv drop box used to  self.public_sim() 
            self._hide_input_widgets()
            if "Generate Simulation" in selected:
                self.publish_gen() 
            elif "Zero" in selected or "Run Simulation" in selected:
                self.publish_run()
                self.entry_runTime.focus()

            self.btn_Gen_Sim["state"] = "active"

        # Create graphs if they don't exist
        if self.graphs is None:
            self.graphs = GraphGui(self.root, self.cage)

    #############################
    # Task Execution            #
    #############################

    def _execute_mode(self):
        current_mode = self.clicked_Mode.get()

        if "Generate Simulation" in current_mode:
            pidTries = int(self.pid_tries_entry.get())
            pidDelay = max(65, int(self.pid_delay_entry.get())) # We claim on the button that 65 should be the minimum

            print(f"Starting Generate Simulation | PID Tries: {pidTries}, PID Delay: {pidDelay}")

            self._launch_worker(
                target=gen_sim,
                args=(self.file_select, "run_csv/new_data.csv"),
                kwargs={"pid_tries": pidTries, "pid_delay": pidDelay},
            )
        elif "Run Simulation" in current_mode:
            runTime = int(self.entry_runTime.get())
            runSpeed = int(self.entry_runSpeed.get())
            startPos = int(self.entry_startPos.get())

            print(f"Starting Run Simulation | Time: {runTime/1000}s, Speed: {runSpeed}ms, Start: {startPos}")
            self._launch_worker(
                target=run_sim,
                args=(self.file_select,),
                kwargs={"runTime_In": runTime, "runSpeed_In": runSpeed, "startPos_In": startPos},
            )

        elif "Zero" in current_mode:
            print("Zeroing field")
            self._launch_worker(
                target=run_sim,
                args=("run_csv/zeroed.csv",),
                kwargs={"runTime_In": 20000, "runSpeed_In": 100, "startPos_In": 0},
            )
