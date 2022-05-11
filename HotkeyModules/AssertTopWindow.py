import time
import win32gui
import os

class AssertTopWindow:
    """
        Checks the topmost active window for a certain window name, when that name is found it will return and the thread will continue
        addedSuffix:str -> Will be appended to the passed window name every time function is called
        interval:int -> The interval in which the the program will refresh window reminders
        exact:bool -> Whether or not the window name must be an exact match
            - True: The window name must be an exact match
            - False: The title of the window must contain the passed window name, will match the whole word
    """
    def __init__(self, addedSuffix:str="", interval:int=2, exact=True):
        self.addedSuffix = addedSuffix # Sometimes a constant suffix is added to the window name, so you don't have to type it every time
        self.interval = interval # The interval in which the the program will refresh window reminders
        self.exact = exact

    def assertTopWindow(self, windowName:str) -> bool:
        """
            Checks the topmost active window for a certain window name, when that name is found it will return and the thread will continue
            windowName:str -> The name of the window to activate
        """

        loopAmount = 0 # The amount of times the loop has run, for the interval calculations
        while True:
            currentWindowText = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if currentWindowText == windowName + self.addedSuffix and self.exact == True:
                break
            
            if windowName + self.addedSuffix in currentWindowText:
                break
            
            if loopAmount % self.interval == 0:
                loopAmount = 0
                os.system("cls")
                print("Current window: " + currentWindowText)
                print("Waiting for window: " + windowName + self.addedSuffix)

            time.sleep(0.2)
            loopAmount += 1
        
        os.system("cls")
        print("Window Confirmed: " + currentWindowText)
        print("Continuing Thread...")
        return True