import threading
import win32gui
import re
from _99helperFunctions import *
from _99universalFunctions import *

def pressButton():
    if not isFacility:
        pressKeyList([
            "ctrl+up",
            "tab,1",
            "shift+tab,7",
            "space"
        ])
    else:
        pressKeyList([
            "ctrl+up"
        ])

    print("Shift to go back...")
    catch("shift", hard=True)

    pressKeyList([
        "tab",
        "down",
        "enter",
        "ctrl+down"
    ])


def parseFacilityLoc():
    global isFacility
    isFacilityLoc = None
    while True:
        isFacility = parseFacility()
        if isFacility == None:
            isFacility = isFacilityLoc
            continue

        isFacilityLoc = isFacility

def parseFacility():
    isFacility = None

    x = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    if re.search("Medical", x):
        isFacility = False
    elif re.search("Hospital", x):
        isFacility = True
    else:
        return isFacility

    return isFacility



threading.Thread(target=parseFacilityLoc, name="FacilityParse", daemon=True).start()
Hotkey("alt+1", pressButton)
kb.wait()