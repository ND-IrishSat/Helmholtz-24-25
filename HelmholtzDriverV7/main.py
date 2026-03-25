from Mode_GUI import RootGUI, ModeGui
from Graph_GUI import GraphGui
from Serial_Ctrl import SerialCtrl

RootMaster = RootGUI()

MySerial = SerialCtrl()
ModeMaster = ModeGui(RootMaster.root, MySerial)
GraphMaster = GraphGui(RootMaster.root, MySerial)

#def on_closing():
#    GraphMaster.plt.close('all')
#    RootMaster.root.destroy()
    
#RootMaster.root.protocol("WM_DELETE_WINDOW", on_closing)

RootMaster.root.mainloop()

# POTENTIAL UPDATE FIX(ES)