from win32gui import GetWindowText
from win32gui import EnumWindows, ShowWindow, SetForegroundWindow

import typing
from time import sleep


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, GetWindowText(hwnd)))


def activateWindowBack(name):
    try:
        top_windows = []
        EnumWindows(windowEnumerationHandler, top_windows)
        for i in top_windows:
            if name in i[1].lower():
                ShowWindow(i[0], 5)
                SetForegroundWindow(i[0])
                break
        print("Window Activation Confirmed")
        return True
    except:
        print("Error in activating Window")
        return False


# When passed a string name this function will activate that window
# and prepare it to handle keystrokes

def activateWindow(name: str) -> bool:
    """
        Brings the window to the front and sets the focus
        name: The name of the window to activate, the window name must contain the passed name
    """
    x = False
    counter = 0

    print(f"Activating Window: {name}")

    while x == False:
        counter += 1
        x = activateWindowBack(name.lower())
        sleep(0.03)

        if counter == 100:
            print("Window Activation Failed")
            return False
