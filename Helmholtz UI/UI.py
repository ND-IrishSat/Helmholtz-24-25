import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import serial
import time

# Port Setup - Automate when connected to PI
ser = serial.Serial(port='COM7',baudrate=115200)
ser.reset_input_buffer()

# Window Set Up
root = tk.Tk()

scn_width = root.winfo_screenwidth()
scn_height = root.winfo_screenheight()

root.title("Helmholtz Cage")
root.geometry("800x800")
root.geometry(f"{scn_width}x{scn_height}")
root.config(background="#0c2340")

root.columnconfigure([0,1,2], weight=1)

# Variables
display_b_field = tk.StringVar()
display_b_field.set(f"Magnetic Field: {ser.readline().decode('utf-8').strip()}")

t_data, x_data, y_data, z_data = [],[],[],[]

# Magnetic Field Graph
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("Magnetic Field (μT) vs. Time")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Magnetic Field (μT)")
line_x, = ax.plot([], [], label="X-axis", color="r")
line_y, = ax.plot([], [], label="Y-axis", color="g")
line_z, = ax.plot([], [], label="Z-axis", color="b")

# &res Note:
# line_z, = some_function_returning_a_tuple()
#   Equivalent Without the Comma
    # lines = ax.plot([], [], label="Z-axis", color="b")
    # line_z = lines[0]  # Extract the first Line2D object
# With the Comma
    # line_z, = ax.plot([], [], label="Z-axis", color="b")

ax.legend()

start_time = time.time()

def update_plot(frame):
    global t_data, x_data, y_data, z_data

    try:
        # Check if data is available
        if ser.in_waiting > 0:
            magnetic_field_string = ser.readline().decode('utf-8').strip().split()
            # Checks for the apprioate length list
            if len(magnetic_field_string) == 3:
                try:
                    x_val = float(magnetic_field_string[0])
                    y_val = float(magnetic_field_string[1])
                    z_val = float(magnetic_field_string[2].rstrip(";"))

                    #. Update display
                    display_b_field.set(f"Magnetic Field: {x_val}, {y_val}, {z_val}")

                    # Add data to arrays
                    t_data.append(time.time() - start_time)
                    x_data.append(x_val)
                    y_data.append(y_val)
                    z_data.append(z_val)

                    # Maintain sliding window
                    max_length = 100
                    if len(t_data) > max_length:
                        t_data = t_data[-max_length:]
                        x_data = x_data[-max_length:]
                        y_data = y_data[-max_length:]
                        z_data = z_data[-max_length:]

                    # Update plot data
                    line_x.set_data(t_data, x_data)
                    line_y.set_data(t_data, y_data)
                    line_z.set_data(t_data, z_data)

                    # Dynamically adjust x and y limits
                    ax.set_xlim(max(0, t_data[-1] - 10), t_data[-1])
                    ax.set_ylim(-100, 100)  # Adjust limits as needed
                except ValueError:
                    print(f"Invalid numeric data: {magnetic_field_string}")
            else:
                print(f"Unexpected data format: {magnetic_field_string}")
    except Exception as e:
        print(f"Error reading serial data: {e}")

    return line_x, line_y, line_z

def toggle_PID_Manual(mode):
    global cage_mode
    if mode == "PID":
        PID_btn.config(background="grey")
        manual_btn.config(background="white")
        cage_mode.set("Mode: PID")
        print("Pressed to PID mode")
    elif mode == "Manual":
        manual_btn.config(background="grey")
        PID_btn.config(background="white")
        cage_mode.set("Mode: Manual")
        print("Pressed Manual")

# Header
header = tk.Label(root, text="GoatLab - Helmhotlz Cage", bg="#0c2340", fg="#c99700", font=("Arial", 24), pady=10) 
header.grid(row=0,column=0,columnspan=3,sticky="ew") #sticky="ew" - fill the available horizontal space

# Display the Updating Magnetic Field
fieldDisplay = tk.Label(root, textvariable=display_b_field, bg="#0c2340",fg="#c99700", font=("Arial", 12), padx=10, pady=10)
fieldDisplay.grid(row=1, column=0,columnspan=3,sticky="ew")

cageMode = tk.LabelFrame(root, text="PID or Manual", bg="#0c2340", fg="#c99700", padx=10, pady=10)
cageMode.grid(row=2, column=0,sticky="ew")
cageMode.columnconfigure([0], weight=1)

cage_mode = tk.StringVar()
cage_mode.set("Mode: Nothing")

# Create buttons inside the LabelFrame
PID_btn = tk.Button(cageMode, text="PID", fg="#0c2340")
PID_btn.config(command=lambda: toggle_PID_Manual("PID"))

manual_btn = tk.Button(cageMode, text="Manual", fg="#0c2340")
manual_btn.config(command=lambda: toggle_PID_Manual("Manual"))

current_mode = tk.Label(cageMode, textvariable=cage_mode, fg="#c99700",bg="#0c2340",font=('calibre',10,'normal'), padx=10, pady=10) 

PID_btn.grid(row=0,columnspan=2, sticky="ew")
manual_btn.grid(row=1,columnspan=2, sticky="ew")
current_mode.grid(row=2,columnspan=2,stick="ew")

# X, Y, Z - Axis
x_1_var = tk.StringVar()
x_2_var = tk.StringVar()
y_1_var = tk.StringVar()
y_2_var = tk.StringVar()
z_1_var = tk.StringVar()
z_2_var = tk.StringVar()

def axisEntry(axis,axis_variable,row_num):
    nth_nth_label = tk.Label(cageMode,text=axis,bg="#0c2340",fg="#c99700")
    nth_nth_entry = tk.Entry(cageMode,textvariable=axis_variable,font=('calibre',10,'normal'))
    nth_nth_label.grid(row=row_num,column=0,stick="ew")
    nth_nth_entry.grid(row=row_num,column=1,stick="ew")

def enter_button():
    x_1 = x_1_var.get()
    x_2 = x_2_var.get()
    y_1 = y_1_var.get()
    y_2 = y_2_var.get()
    z_1 = z_1_var.get()
    z_2 = z_2_var.get()
    print(f"This is {x_1}, {x_2}, {y_1}, {y_2}, {z_1}, {z_2}.")

# Textbook Entries 
axisEntry("x_1",x_1_var,3)
axisEntry("x_2",x_2_var,4)
axisEntry("y_1",y_1_var,5)
axisEntry("y_2",y_2_var,6)
axisEntry("z_1",z_1_var,7)
axisEntry("z_2",z_2_var,8)

enter_btn = tk.Button(cageMode, text="Enter", fg="#0c2340",command=enter_button)
enter_btn.grid(row=9,columnspan=2, sticky="ew")

# Frame for the Matplotlib plot
style = ttk.Style()
style.configure("Custom.TFrame", background="#0c2340")  # Set your desired color
frame = ttk.Frame(root, style="Custom.TFrame")
frame.grid(row=2, column=1, columnspan=2, sticky="nsew")  # Span columns 1 to 2

# # Embed the Matplotlib figure in the frame
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(row=0, column=0, rowspan=3, columnspan=2, sticky="nsew")

# Updates the magnetic field display and plot animation
ani = animation.FuncAnimation(fig, update_plot, interval=50, blit=False,cache_frame_data=False)

# Main Application Loop
root.mainloop()