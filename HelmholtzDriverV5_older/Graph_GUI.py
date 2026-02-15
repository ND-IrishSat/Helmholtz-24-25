from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import threading
import numpy as np     
import time

class GraphGui():
    def UI_contrl(self):
        next_time = time.time()
        while True:
            # Check if Paused_Serial is True
            if not self.paused_serial:
                self.update_plot()
                
            # Loop function every 100 ms
            next_time += 0.1
            sleep_time = next_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                next_time = time.time()

    
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
        self.previous_magnetic_field = None
        self.xmag = []
        self.ymag = []
        self.zmag = []
        self.tot = []
        
        # Sliding window size (number of points to display)
        self.window_size = 500
        
        # Add the first chart automatically
        self.AddMasterFrame()
        self.AddGraph()
        
        # Start UI_Contr Thread
        threading.Thread(target=self.UI_contrl, daemon=True).start()

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
        print(f"update plot: {value}")
        
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
            current_magnetic_field = np.sqrt((self.xmag[len(self.xmag) - 1]**2) + (self.ymag[len(self.xmag) - 1]**2) + (self.zmag[len(self.xmag) - 1]**2))
            
            # 2/12 attempt to filter
            if len(self.tot) - 10 > 1:
                self.previous_magnetic_field = self.tot[len(self.tot) - 1]
            else:
                self.previous_magnetic_field = current_magnetic_field
            
            if abs(current_magnetic_field) < abs(self.previous_magnetic_field) - 30 or abs(current_magnetic_field) > abs(self.previous_magnetic_field) + 30:
                print("jump occured: {current_magnetic_field} vs {previous_magnetic_field}")
                current_magnetic_field = self.previous_magetic_field
                
            self.tot.append(current_magnetic_field)
            print(f"\t\t\tupdate plot: {current_magnetic_field}")
            # keep all data but only plot the last window_size points
            start_idx = max(0, len(self.time) - self.window_size)
            time_window = self.time[start_idx:]
            xmag_window = self.xmag[start_idx:]
            ymag_window = self.ymag[start_idx:]
            zmag_window = self.zmag[start_idx:]
            tot_window = self.tot[start_idx:]

            # Show Data on graph (only last window_size points)
            self.figs[self.totalframes][1].clear()
            self.figs[self.totalframes][1].set_ylabel("Magnetic Field (uT)")
            self.figs[self.totalframes][1].set_xlabel("Time (S)")
            self.figs[self.totalframes][1].set_ylim(25, 55)
            #self.figs[self.totalframes][1].plot(time_window, xmag_window, color='green', label='X Field')
            #self.figs[self.totalframes][1].plot(time_window, ymag_window, color='red', label='Y Field')
            #self.figs[self.totalframes][1].plot(time_window, zmag_window, color='blue', label='Z Field')
            self.figs[self.totalframes][1].plot(time_window, tot_window, color='black', label='Total Field')
            #self.figs[self.totalframes][1].plot(self.time, self.tot, color='black', label='Total Field')

            self.figs[self.totalframes][1].legend(loc ='upper left')
            self.figs[self.totalframes][2].draw()
        else:
            # Appends the last object in the list
            print ("print value was None")
            
            self.xmag.append(self.xmag[len(self.xmag) - 1])
            self.ymag.append(self.ymag[len(self.ymag) - 1])
            self.zmag.append(self.zmag[len(self.zmag) - 1])
            self.time.append(len(self.time) * 0.1)
            self.tot.append(self.tot[len(self.tot) - 1])

            # keep all data but only plot the last window_size points
            start_idx = max(0, len(self.time) - self.window_size)
            time_window = self.time[start_idx:]
            xmag_window = self.xmag[start_idx:]
            ymag_window = self.ymag[start_idx:]
            zmag_window = self.zmag[start_idx:]
            tot_window = self.tot[start_idx:]
                
            self.figs[self.totalframes][1].clear()
            self.figs[self.totalframes][1].set_ylabel("Magnetic Field (uT)")
            self.figs[self.totalframes][1].set_xlabel("Time (S)")
            self.figs[self.totalframes][1].set_ylim(25, 55)
            self.figs[self.totalframes][1].plot(time_window, tot_window, color='black', label='Total Field')
            self.figs[self.totalframes][1].legend(loc ='upper left')
            self.figs[self.totalframes][2].draw()
        
    
            
    def set_graph(self, totalMag, simMag, timeVector):
        # Show Data on graph (only last window_size points)
        self.figs[self.totalframes][1].clear()
        self.figs[self.totalframes][1].set_ylabel("Magnetic Field (uT)")
        self.figs[self.totalframes][1].set_xlabel("Time (mS)")
        self.figs[self.totalframes][1].plot(timeVector, totalMag, color='green', label='Total Mag Field')
        self.figs[self.totalframes][1].plot(timeVector, simMag, color='red', label='Simulated Field')
        self.figs[self.totalframes][1].legend(loc ='upper left')
        self.figs[self.totalframes][2].draw()
