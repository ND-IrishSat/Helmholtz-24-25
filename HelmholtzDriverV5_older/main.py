from Mode_GUI import RootGUI, ModeGui
from Graph_GUI import GraphGui
from Serial_Ctrl import SerialCtrl

RootMaster = RootGUI()

MySerial = SerialCtrl()
ModeMaster = ModeGui(RootMaster.root, MySerial)
GraphMaster = GraphGui(RootMaster.root, MySerial)

RootMaster.root.mainloop()

# POTENTIAL UPDATE FIX
# actual and simulated values