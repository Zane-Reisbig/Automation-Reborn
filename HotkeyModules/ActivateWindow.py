import win32gui
import typing
from time import sleep

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def activateWindowBack(name):
    try:
        if(__name__ != "__main__"):
            top_windows = []
            win32gui.EnumWindows(windowEnumerationHandler, top_windows)
            for i in top_windows:
                if name in i[1].lower():
                    win32gui.ShowWindow(i[0],5)
                    win32gui.SetForegroundWindow(i[0])
                    break
            print("Window Activation Confirmed")
            return True
    except:
        print("Error in activating Window")
        return False


# When passed a string name this function will activate that window 
# and prepare it to handle keystrokes
 
def activateWindow(name:str) -> bool:
    """
        Brings the window to the front and sets the focus
        name: The name of the window to activate, the window name must contain the passed name
    """
    x = False
    while x == False:
        x = activateWindowBack(name.lower())
        sleep(0.03)