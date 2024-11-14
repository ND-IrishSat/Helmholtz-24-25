import tkinter as tk

# Requirements
# Be able to input [x_1,x_2,y_1,y_2,z_1,z_2] values
    # Enter the values individual -> Combine into a string 
# Be able to read the cage's magnetic field
# Power switch

# Set Up
root = tk.Tk()

root.geometry("800x800")
root.title("Helmholtz Cage")

# Toggle Function
def toggle_text(): 
    if button.config('text')[-1] == "Power On":
        button.config(text="Power Off")
    else:
        button.config(text="Power On")

# Header
header = tk.Label(root, text="GoatLab Helmhotlz Cage", bg="#0c2340", fg="#c99700", font=("Arial", 24), pady=10)
header.pack(fill=tk.X)  

# Button
button = tk.Button(root, text="Power On", command=toggle_text)
button.pack(pady=20)

root.mainloop()
