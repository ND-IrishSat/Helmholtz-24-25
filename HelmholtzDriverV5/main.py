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
            continue
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
['-', 'zeroed.csv', 'magFieldsOut.csv', 'desired_field.csv', 'runZeroed.csv', 'runPySolReal.csv']
Generate Simulation mode selected
zeroed.csv
STATUS: gen_sim starting: zeroed.csv
Serial read error: device reports readiness to read but returned no data (device disconnected or multiple access on port?)
ERROR: gen_sim failed: SerialException('device reports readiness to read but returned no data (device disconnected or multiple access on port?)')
'''