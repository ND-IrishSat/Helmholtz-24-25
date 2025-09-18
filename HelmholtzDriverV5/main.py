from GUI_Master import RootGUI, ModeGui

RootMaster = RootGUI()

ModeMaster = ModeGui(RootMaster.root)

RootMaster.root.mainloop()