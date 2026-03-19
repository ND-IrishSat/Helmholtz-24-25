from Mode_GUI import RootGUI, ModeGui
from Graph_GUI import GraphGui
from Serial_Ctrl import SerialCtrl

RootMaster = RootGUI()

MySerial = SerialCtrl()
ModeMaster = ModeGui(RootMaster.root, MySerial)
GraphMaster = GraphGui(RootMaster.root, MySerial)
    
RootMaster.root.protocol("WM_DELETE_WINDOW", GraphMaster.cleanup)
RootMaster.root.mainloop()  

# POTENTIAL UPDATE FIX(ES)