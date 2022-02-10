import time
import win32gui
import os

class AssertTopWindow:
    """
        Checks the topmost active window for a certain window name
        If the window name is the same as the one passed in, the function returns
        This is used to make sure the window is the one you want to interact with -
            By blocking the Thread until it returns
    """
    def __init__(self, addedSuffix:str="", interval:int=2):
        self.addedSuffix = addedSuffix # Sometimes a constant suffix is added to the window name, so you don't have to type it every time
        self.interval = interval # The interval in which the the program will refresh window reminders

    def assertTopWindow(self, window_name:str):
        loopAmount = 0 # The amount of times the loop has run, for the interval calculations
        while True:
            currentWindowText = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if currentWindowText == window_name + self.addedSuffix:
                break
            
            if loopAmount % self.interval == 0:
                loopAmount = 0
                os.system("cls")
                print("Current window: " + currentWindowText)
                print("Waiting for window: " + window_name + self.addedSuffix)

            time.sleep(0.2)
            loopAmount += 1