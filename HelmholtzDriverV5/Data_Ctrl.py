
class DataMaster():
    def __init__(self):
        '''
        Method to initialize the Data class
        This classes will manage data transformation within the whole program 
        '''
        # Program Logic to interface with MCU
        self.sync = "#?#\n"
        self.sync_ok = "!"
        self.StartStream = "#A#\n"
        self.StopStream = "#S#\n"
        self.SynchChannel = 0
        self.msg = []
        # Build the Ydata
        self.YData = []
        self.XData = []

    def DecodeMsg(self):
        '''
            Method used to get the message coming from UART and converted to a python string
            it is also used to get defferent type of messages based on the Message protocol
            '''
        temp = self.RowMsg.decode('utf8')
        if len(temp) > 0:
            if "#" in temp:
                self.msg = temp.split("#")
                # print(self.msg)
                del self.msg[0]

    def GenChannels(self):
        '''
        Mehtod to Generate the list of Channels to be used for the selection
        '''
        self.Channels = [f"Ch{ch}" for ch in range(self.SynchChannel)]

    def buildYdata(self):
        '''
            Message to get the right size of the data to be inputted into the Y data
            '''
        for _ in range(self.SynchChannel):
            self.YData.append([])

    def ClearData(self):
        '''
        Mehtod used to clear the data after each new serial updload
        '''
        self.RowMsg = ""
        self.msg = []
        self.YData = []


if __name__ == "__main__":
    DataMaster()