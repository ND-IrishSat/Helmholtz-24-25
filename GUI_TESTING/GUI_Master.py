from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading
import matplotlib

class RootGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Serial Connection")
        self.root.geometry("360x120")
        self.root.config(bg="white")
        
        
class ComGui():
    def __init__(self,root):
        self.root = root
        self.frame = LabelFrame(root, text = "Com Manger",
                                padx=5, pady=5, bg="white")
        self.label_com = Label(
            self.frame, text="Available Port(s): ", bg="white", width=15, anchor="w")
        self.label_bd = Label(
            self.frame, text= "Baude Rate: ", bg="white", width=15, anchor="w")
        self.ComOptionMenu()
        self.BaudOptionMenu()
        
        self.btn_refresh = Button(self.frame, text="Refresh",
                                  width = 10)
        self.btn_connect = Button(self.frame, text="Connect",
                                  width = 10, state="disabled")
        self.padx = 20
        self.pady = 5
        self.publish()
    
    def ComOptionMenu(self):
        coms = ["-", "COM3", "COM2", "COM6"]
        self.clicked_com = StringVar()
        self.clicked_com.set(coms[0])
        self.drop_com = OptionMenu(
            self.frame, self.clicked_com, *coms, command=self)
        self.drop_com.config(width=10)
        
    def BaudOptionMenu(self):
        self.clicked_bd = StringVar()
        bds = ["-", "300", "600", "1200"]
        self.drop_bd = OptionMenu(
            self.frame, self.clicked_bd, *bds)
        self.clicked_bd.set(bds[0])
        self.drop_bd.config(width=10)
        
    def publish(self):
        self.frame.grid(row=0, column=0, rowspan=3,
                        columnspan=3, padx=5, pady=5)
        
        self.label_com.grid(column=1, row=2, padx=self.padx, pady=self.pady)
        self.drop_com.grid(column=2, row=2)
        self.label_bd.grid(column=1, row=3)
        self.drop_bd.grid(column = 2, row = 3)
        
        self.btn_refresh.grid(column=3, row=2)
        self.btn_connect.grid(column=3, row=3)
        
    def connect_crtl(self):
        print("Connect ctrl")
        


if __name__ == "__main__":
    RootGUI()