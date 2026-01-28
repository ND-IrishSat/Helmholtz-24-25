from Mode_GUI import RootGUI, ModeGui
from Graph_GUI import GraphGui
from Serial_Ctrl import SerialCtrl

RootMaster = RootGUI()

MySerial = SerialCtrl()
ModeMaster = ModeGui(RootMaster.root, MySerial)
GraphMaster = GraphGui(RootMaster.root, MySerial)

RootMaster.root.mainloop()

# zero.csv -> runZeroed.csv

# POTENTIAL UPDATE FIX
# Make updating the plot happen inside of a thread
# Make a thread that cycles every 100ms
# Run update_plot only if paused serial is false