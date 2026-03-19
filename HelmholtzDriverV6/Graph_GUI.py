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
        
        # Matplotlib Objects 
        self.fig = plt.Figure(figsize=(8,4), dpi =80)
        self.container_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.container_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Value Arrays
        self.previous_magnetic_field = None
        self.xmag, self.ymag, self.zmag = [], [], []
        self.time, self.sim, self.tot = [], [], []
        self.window_size = 500  # Sliding window size (number of points to display)
        
        # Start UI_Contr Thread
        threading.Thread(target=self.UI_contrl, daemon=True).start()
        
    def update_plot(self):
        value = self.serial.read_value()
        print(f"update plot: {value}")
        
        if value is not None:
            try:
                self.xmag.append(value[0])
                self.ymag.append(value[1])
                self.zmag.append(value[2])
                self.sim.append(value[3])
            except:
                print("UP. Could not append new values")
                self.xmag.append(self.xmag[len(self.xmag) - 1])
                self.ymag.append(self.ymag[len(self.ymag) - 1])
                self.zmag.append(self.zmag[len(self.zmag) - 1])
                self.sim.append(self.sim[len(self.sim) - 1])
            
            current_magnetic_field = np.sqrt((self.xmag[len(self.xmag) - 1]**2) + (self.ymag[len(self.xmag) - 1]**2) + (self.zmag[len(self.xmag) - 1]**2))
            
            # 2/12 attempt to filter
            if len(self.tot) - 10 > 1:
                self.previous_magnetic_field = self.tot[len(self.tot) - 1]
            else:
                self.previous_magnetic_field = current_magnetic_field
            
            if abs(current_magnetic_field) < abs(self.previous_magnetic_field) - 30 or abs(current_magnetic_field) > abs(self.previous_magnetic_field) + 30:
                print("jump occured: {current_magnetic_field} vs {previous_magnetic_field}")
                current_magnetic_field = self.previous_magnetic_field
                
            self.tot.append(current_magnetic_field)
            self.time.append(len(self.time) * 0.1)

            # keep all data but only plot the last window_size points
            start_idx = max(0, len(self.time) - self.window_size)
            time_window = self.time[start_idx:]
            sim_window  = self.sim[start_idx:]
            tot_window  = self.tot[start_idx:]

            # Show Data on graph (only last window_size points)
            self.ax.clear()
            self.ax.set_ylabel("Magnetic Field (uT)")
            self.ax.set_xlabel("Time (S)")
            self.ax.set_ylim(-5, 45)

            self.ax.plot(time_window, tot_window, color='black', label='Total Field')
            self.ax.plot(time_window, sim_window, color='red', label='Simulated Field')
            self.ax.legend(loc='upper left')
            
            # Final Render
            self.canvas.draw()

    def cleanup(self):
        """Standard cleanup for the single graph"""
        plt.close(self.fig)
        self.canvas.get_tk_widget().destroy()
            
    def set_graph(self, totalMag, simMag, timeVector):
        # Recalculate the window
        start_idx = max(0, len(self.time) - self.window_size)
        
        time_window = self.time[start_idx:]
        sim_window  = self.sim[start_idx:]
        tot_window  = self.tot[start_idx:]

        # Show Data on graph (only last window_size points)
        self.ax.clear()
        self.ax.set_ylabel("Magnetic Field (uT)")
        self.ax.set_xlabel("Time (S)")
        self.ax.plot(time_window, tot_window, color='black', label='Total Field')
        self.ax.plot(time_window, sim_window, color='red', label='Simulated Field')
        self.ax.legend(loc='upper left')
        self.canvas.draw()
