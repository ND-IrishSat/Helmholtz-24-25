import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Requirements
# PID vs Manuel  
# # PID:
# # # Input Desired Value
# # Manuel:
# Be able to input [x_1,x_2,y_1,y_2,z_1,z_2] values
    # Enter the values individual -> Combine into a string 
# Power switch

# Window Set Up
root = tk.Tk()

root.title("Helmholtz Cage")
root.geometry("800x800")

# root.rowconfigure(2, weight=1)
root.columnconfigure([0,1,2], weight=1)

# # Functions
# PID vs Manuel Functions (WIP)
# def toggle_PID(): 
#     if button.config('text')[-1] == "Power On":
#         button.config(text="Power Off")
#     else:
#         button.config(text="Power On")

def update_field():
    # Once we get a function to read the magnetic field from the magnetometer, we need to change the global b_field_i to read directly form that
    global b_field_i
    b_field_i+=100
    display_b_field.set(f"Magnetic Field: {b_field_i}") 
    root.after(1000,update_field)

def toggle_PID_Manual(mode):
    if mode == "PID":
        print("Pressed to PID mode")

    elif mode == "Manual":
        print("Pressed Manual")

# Variables
b_field_i = 1000
display_b_field = tk.StringVar()
display_b_field.set(f"Magnetic Field: {b_field_i}")

# Header
header = tk.Label(root, text="GoatLab - Helmhotlz Cage", bg="#0c2340", fg="#c99700", font=("Arial", 24), pady=10) 
header.grid(row=0,column=0,columnspan=3,sticky="ew") #sticky="ew" - fill the available horizontal space

# Display the Updating Magnetic Field
fieldDisplay = tk.Label(root, textvariable=display_b_field, fg="#0c2340", font=("Arial", 12), padx=10, pady=10)
fieldDisplay.grid(row=1, column=0,columnspan=3,sticky="ew")

labelframe1 = tk.LabelFrame(root, text="PID or Manual", bg="#0c2340", fg="#c99700", padx=10, pady=10)

labelframe1.grid(row=2, column=0,sticky="ew")
labelframe1.columnconfigure([0], weight=1)

# Create buttons inside the LabelFrame
PIDButton = tk.Button(labelframe1, text="PID", fg="#0c2340")
PIDButton.config(command=lambda: toggle_PID_Manual("PID"))
PIDButton.grid(row=0, sticky="ew")

ManualButton = tk.Button(labelframe1, text="Manual", fg="#0c2340")
ManualButton.config(command=lambda: toggle_PID_Manual("Manual"))
ManualButton.grid(row=1, sticky="ew")

# # Frame for the Matplotlib plot
frame = ttk.Frame(root)
frame.grid(row=2, column=1, columnspan=2, sticky="nsew")  # Span columns 1 to 2

fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])  # Example plot
ax.set_title("Magnetic Field (μT) vs. Time")
ax.set_ylabel("Magnetic Field (μT)")


# # Embed the Matplotlib figure in the frame
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()

canvas_widget.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="nsew")

# Start the magnetic field update loop
root.after(0,update_field)

# Main Application Loop
root.mainloop()