import queue, threading, time
from GUI_Master import RootGUI,  ModeGui, GraphGui
from Serial_Ctrl import SerialCtrl

msg_q = queue.Queue()
stop_event = threading.Event()

RootMaster = RootGUI()
MySerial = SerialCtrl()

def serial_reader_loop(ser_ctrl: SerialCtrl):
    while True:
        if stop_event.is_set():
            time.sleep(0.02)
        vals = ser_ctrl.read_value()
        if vals is not None:
            msg_q.put(("serial", vals))

# Start background serial reader (daemon=true so it doesn't block app closing)
serial_thread = threading.Thread(target=serial_reader_loop, args=(MySerial,), daemon=True)
serial_thread.start()
            
ModeMaster = ModeGui(RootMaster.root, MySerial, msg_q=msg_q, stop_event=stop_event)
GraphMaster = GraphGui(RootMaster.root, MySerial, msg_q=msg_q)

def on_close():
    stop_event.set()
    try:
        MySerial.close()
    except:
        pass
    RootMaster.root.destroy()

RootMaster.root.protocol("WM_DELETE_WINDOW", on_close)
RootMaster.root.mainloop()

'''
Traceback (most recent call last):
  File "/usr/lib/python3.11/tkinter/__init__.py", line 1948, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
  File "/home/irishsat/Helmholtz-24-25/HelmholtzDriverV5/GUI_Master.py", line 261, in Gen_Sim_ctrl
    gen_sim( self.file_select, self.serial)
  File "/home/irishsat/Helmholtz-24-25/HelmholtzDriverV5/ui_genSim.py", line 123, in gen_sim
    magnetometerOutput = nanoSer.readline().decode('utf-8').strip().split()
                         ^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/serial/serialposix.py", line 595, in read
    raise SerialException(
serial.serialutil.SerialException: device reports readiness to read but returned no data (device disconnected or multiple access on port?)
'''