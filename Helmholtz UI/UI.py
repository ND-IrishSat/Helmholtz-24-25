import tkinter as tk

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

root.columnconfigure([0,1,2], weight=1)

# Functions
def toggle_PID(): 
    if button.config('text')[-1] == "Power On":
        button.config(text="Power Off")
    else:
        button.config(text="Power On")

def update_field():
    # Once we get a function to read the magnetic field from the magnetometer, we need to change the global b_field_i to read directly form that
    global b_field_i
    b_field_i+=100
    display_b_field.set(f"Magnetic Field: {b_field_i}") 
    root.after(1000,update_field)

# Variables
b_field_i = 1000
display_b_field = tk.StringVar()
display_b_field.set(f"Magnetic Field: {b_field_i}")

# Header
header = tk.Label(root, text="GoatLab Helmhotlz Cage", bg="#0c2340", fg="#c99700", font=("Arial", 24), pady=10) 
header.grid(row=0,column=0,columnspan=3,sticky="ew") #sticky="ew" - fill the available horizontal space

# Display the an Updating Magnetic Field
fieldDisplay = tk.Label(root, textvariable=display_b_field,fg="#0c2340",font=("Arial",12), padx=10,pady=10)
fieldDisplay.grid(row=1,column=1,sticky="ew")

# Start the magnetic field update loop
root.after(0,update_field)

# Main Application Loop
root.mainloop()
