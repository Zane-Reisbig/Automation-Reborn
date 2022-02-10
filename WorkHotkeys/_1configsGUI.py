from tkinter.constants import END
import mouse
from tkinter import Label, Entry, Button, StringVar, Tk
from _99universalFunctions import *

class MainGui:
    def __init__(self, master):
        self.master = master
        self.startup(self.master, 315, "Easy Buttons")

        self.label_commandLabel = Label(self.master, text="Command Output")
        self.label_commandLabel.grid(
            row = 1,
            column = 0
        ) 

        self.strVar_commandInput = StringVar()
        self.input_commandBox = Entry(self.master, width=50, textvariable=self.strVar_commandInput)
        self.input_commandBox.grid(
            row = 2,
            column = 0,
            columnspan = 2,
            pady = (0, 5)
        )

        self.btn_openClaim = self.easyButton(self.master, "Open Claim", lambda: self.loc_openClaim(self.strVar_commandInput, "Waiting for click to open Claim"))
        self.styler(self.btn_openClaim, 3, 0)
        
        self.btn_overridePCA = self.easyButton(self.master, "Override PCA", lambda: self.loc_overridePCA(self.strVar_commandInput, "Overriding PCO"))
        self.styler(self.btn_overridePCA, 3, 1)

    def loc_openClaim(self, entryInstance, entrymsg):
        entryInstance.set(entrymsg)
        openClaim()
        
    def loc_overridePCA(self, entryInstance, entrymsg):
        entryInstance.set(entrymsg)
        overRidePCA() 

    def startup(self, master, size, title):
        master.minsize(size, size)
        master.maxsize(size, size)
        master.title(title)
        
    def easyButton(self, master, text, command):
        easyButton = Button(
            master,
            text = text,
            command = command,
        )

        return easyButton

    def styler(self, element, row, column):
        element.grid(
            column = column,
            row = row,
            padx = (10, 10),
            pady = (10, 10),
        )

        element.config(
            height = 1,
            width = 18
        )


master = Tk()
main = MainGui(master)
master.mainloop()