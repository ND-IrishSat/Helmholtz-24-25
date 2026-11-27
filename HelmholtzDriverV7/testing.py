#!/usr/bin/env python3

from Graph_GUI import RootGUI, ModeGUI

from generateSimulation import gen_sim
from runSimulation import run_sim

from cage_hardware import CageHardware 
import sys
import threading

def main(args: list[str]=sys.argv[1:]) -> None:
    # Creates the hardware managers
    CageMaster = CageHardware()
    # Creates a stop flag
    gen_stop_event = threading.Event()
    run_stop_event = threading.Event()


    RootMaster = RootGUI()
    ModeMaster = ModeGUI(RootMaster.root, CageMaster, gen_stop_event, run_stop_event)


    print("Start Sim")
        
if __name__ == '__main__':
    main()	

# from Mode_GUI import RootGUI, ModeGui
# from Graph_GUI import GraphGui
# from Serial_Ctrl import SerialCtrl

# RootMaster = RootGUI()
# MySerial = SerialCtrl()

# ModeMaster = ModeGui(RootMaster.root, MySerial)
# GraphMaster = GraphGui(RootMaster.root, MySerial)

# #def on_closing():
# #    GraphMaster.plt.close('all')
# #    RootMaster.root.destroy()
    
# #RootMaster.root.protocol("WM_DELETE_WINDOW", on_closing)

# RootMaster.root.mainloop()
