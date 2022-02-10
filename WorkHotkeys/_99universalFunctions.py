import pyautogui as pag
import pyperclip
import re
from enum import Enum
from ._99settingsFile import *
from ._99helperFunctions import *
from os import system


class ClickOptions(Enum):
    Default = {"click" : True, "clickAmount" : 2}
    Excel = {"click" : False, "clickAmount" : 0}
    BiLaunch = {"click" : True, "clickAmount" : 3}

# Opens a claim based on what you have highlighted, I.E. 255655654901 if you highlight it and press -
# the hotkey the tab will be switched to Facets and the claim will be opened.
#
# Params:
# hotkey - The hotkey that activates the function.
# reprocess - Whether or not the suffix is changed to passed value.
# click - If the mouse is double-clicked to highlight a string.
# clickAmount - Decides tthe amount of times the mouse is clicked when clicking.
# f3 - Determins if the claim will be f3'd after it is opened
# suffix - if the claim is being reprocesed the claim could end in any number of things.
# moveToWindow - when using the "waitForAdj()" function the mouse needs to be on the facets window - 
#                this will move it to the open facets window

def openClaim(hotkey="f13", reprocess=False, click=ClickOptions.Default, f3=True, suffix=1, moveToWindow=True, highlight=True):
    claimNumber = ""
    
    if click == ClickOptions.Excel:
        highlightExcel()
        pressKeyList([
            "down"
        ])
        sleep(0.8)

    
    if click.value["click"] == True:
        pag.click()
        sleep(0.5)

        pag.click(clicks=click.value["clickAmount"])

    pressKey("ctrl+c", 2, 0.4)

    clipboardContents = pyperclip.paste()

    # Blocks the thread when nothing or a single space is found on the clipboard - 
    # because why would you want that 
    if clipboardContents in ["\r\n", "\r", "\n", " ", ""]:
        print("System Paused, No contents on clipboard\nPress shift to continue")
        catch("shift", hard=True)
        clipboardContents = pyperclip.paste()

    if re.search("\w\s+\w", clipboardContents) != None:
        print("There is a space on the clipboard\nPress shift to continue.")
        catch("shift", hard=True)
        clipboardContents = pyperclip.paste()

    claimNumber =  clipboardContents.replace("\n", "")
  
    activateWindow("facets")

    if moveToWindow:
        pos = getWindowLocation("facets")
        pag.moveTo(pos[2] / 2, pos[3] / 2)

    pressKeyList([
        "enter,2",
        "ctrl+o",
        "-3,assertTopWindow,Open",
        "-1,{}".format(claimNumber)
    ])

    if reprocess:
        sleep(0.5)
        pressKeyList([
            "backspace",
            "-1,{}".format(str(suffix))
        ])

    pressKeyList([
        "enter",
        "ctrl+down",
    ])

    if f3:
        pressKey("f3")

    system("cls")
    print("Claim Opened")


# Parses Facility value based on tab text

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

# This will re-open a claim no matter if changes have been made to it
#
# Params:
# hotkey - the hotkey that call the function
# optional - the keyboard library will crash if 2 params are not supplied when passing arguments

def reopenClaim(hotkey):
    waitForRelease(hotkey)

    pressKeyList([
        "ctrl+o",
        "right",
        "enter",
        "enter",
        "enter",
        "ctrl+down",
        "f3"
    ])



# This integrates with the settingsFile.py to increase, decrease, or reset the amount of claims being tracked
#
# Params:
# settingsFile - a settingsFile class object containg a key with an integer value to be changed
# keyId - the keyID the number changing

def claimAdj(settingsFile, keyID, type):
    initialValue = settingsFile.readValue(keyID, int)

    if type in ["decrement", "dec", "d", "-"]:
        settingsFile.changeValue(keyID, initialValue - 1)
    elif type in ["increment", "inc", "i", "+"]:
        settingsFile.changeValue(keyID, initialValue + 1)
    elif type in ["reset", "res", "r"]:
        settingsFile.changeValue(keyID, 0)
    
    print("Claim Amount:", settingsFile.readValue(keyID))
    return

# This is used for getting and settings the mouse position for the "waitForAdj()" function - 
# Will return X and Y coords of a windows location on the screen
#
# Params:
# window - Name of window to find case insensitive

def getWindowLocation(window):
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)

    for i in top_windows:
        if window in i[1].lower():
            return win32gui.GetWindowRect(i[0])
    else:
        raise NameError("Window Not Found")

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def overRidePCA(facility=False, switchTab=None):
    activateWindow("facets")
    
    if switchTab:
        pressKey("ctrl+shift+tab", 2)
        sleep(0.3)
        parseFacility()

    if facility:
        pca_offset = 1
    else:
        pca_offset = 0

    pressKeyList([
        "alt+o",
        "-3,assertTopWindow,Line Item Override",
        "alt+c",
        "-3,assertTopWindow,Claim Overrides",
        "tab,{},0".format(14 + pca_offset),
        "space",
        "tab",
        "-1,PCO",
        "enter,2",
        "-2,0.6",
        "f3"
    ])

    waitForAdj()
    
    if switchTab:
        print("Press shift to f4")
        catch("shift", hard=True)
        pressKey("f4")

