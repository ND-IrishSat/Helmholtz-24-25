from GUI_Master import RootGUI, ModeGui, GraphGui

RootMaster = RootGUI()

ModeMaster = ModeGui(RootMaster.root)

GraphMaster = GraphGui(RootMaster.root)

RootMaster.root.mainloop()