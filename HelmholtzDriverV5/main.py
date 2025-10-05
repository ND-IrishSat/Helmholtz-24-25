from GUI_Master_1 import RootGUI,  ModeGui, GraphGui, ConnGUI
from Data_Ctrl import DataMaster
from Serial_Ctrl import SerialCtrl

RootMaster = RootGUI()

MyData = DataMaster()
MySerial = SerialCtrl()
ModeMaster = ModeGui(RootMaster.root, MySerial, MyData)
GraphMaster = GraphGui(RootMaster.root, MySerial, MyData)
ComMaster = ConnGUI(RootMaster.root, MySerial, MyData)

RootMaster.root.mainloop()