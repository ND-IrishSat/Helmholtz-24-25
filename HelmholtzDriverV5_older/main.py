from GUI_Master import RootGUI,  ModeGui, GraphGui
from Serial_Ctrl import SerialCtrl

RootMaster = RootGUI()

MySerial = SerialCtrl()
ModeMaster = ModeGui(RootMaster.root, MySerial)
GraphMaster = GraphGui(RootMaster.root, MySerial)

RootMaster.root.mainloop()