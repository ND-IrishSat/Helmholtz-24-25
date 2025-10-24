from GUI_Master import RootGUI,  ModeGui, GraphGui
from Serial_Ctrl import SerialCtrl

RootMaster = RootGUI()
MySerial = SerialCtrl()

def serial_reader_loop(ser_ctrl):
    while True:
        if stop_event.is_set()
            time.sleep(0.02)
        vals = ser_ctrl.read_value()
        if vals is not None:
            msg_q.put(("serial", vals))
            
ModeMaster = ModeGui(RootMaster.root, MySerial)
GraphMaster = GraphGui(RootMaster.root, MySerial)

RootMaster.root.mainloop()