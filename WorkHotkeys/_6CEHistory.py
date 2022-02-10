import os
import re
import pyautogui
import pyperclip
import threading
from keyboard import *
from _99helperFunctions import *
from _99universalFunctions import *
from _99settingsFile import *

#External Settings
settings        = SettingsFile("_0settingsRep.txt")
amountOfClaims  = settings.readValue("amountOfClaims" , int)
incrementNext   = settings.readValue("incrementNext"  , bool)
replaceOriginal = settings.changeValue("replaceOriginal", "True", True, bool)

#Internal Settings
currentDate = ""
old_data    = ""
claimNumber = ""
currentSearch = "Subscriber ID"
lastCommand = None

def incrementClaim(operator="+", getNewClaim=None):
    global claimNumber, amountOfClaims
    
    if operator == "+":
        amountOfClaims = settings.changeValue("amountOfClaims", str(amountOfClaims + 1), True, int)
    elif operator == "-":
        amountOfClaims = settings.changeValue("amountOfClaims", str(amountOfClaims - 1), True, int)
    elif operator == "=":
        amountOfClaims = settings.changeValue("amountOfClaims", "0", True, int)
    else:
        raise ArgumentError("Unknown passed")

    os.system("cls")

    if amountOfClaims != CLAIM_AMOUNT:
        print("Amount of Claims:", amountOfClaims)
        print("Amount Left:", CLAIM_AMOUNT - amountOfClaims)
        print(f"Percentage Done:", str(round((amountOfClaims / CLAIM_AMOUNT) * 100, 2)) + "%")
    else:
        activateWindow("code")
        print("{} Claims reached".format(CLAIM_AMOUNT))
        input("Press enter to continue")
        activateWindow("facets")
    
    if getNewClaim:
        openClaimLoc(openClaimArgs["hotkey"],
                     openClaimArgs["reprocess"],
                     openClaimArgs["click"],
                     openClaimArgs["f3"],
                     openClaimArgs["suffix"],
                     openClaimArgs["moveToWindow"],
                     openClaimArgs["highlight"],
                     openClaimArgs["checkReplacement"])

def parseFacilityLoc():
    global isFacility
    isFacilityLoc = None
    while True:
        isFacility = parseFacility()
        if isFacility == None:
            isFacility = isFacilityLoc
            continue

        isFacilityLoc = isFacility

def openClaimLoc(hotkey="f13", reprocess=False, click=ClickOptions.Default, f3=True, suffix=1, moveToWindow=True, highlight=True, checkReplacement=False): 
    openClaim(hotkey, reprocess, click, f3, suffix, moveToWindow, highlight)
    waitForAdj()

    if checkReplacement:
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

def verifyInput(returnValue, regexMatch):
    while(True):
        if re.search(regexMatch, f"^{returnValue}$"): break
        returnValue = input("Input Does not match: ")
    
    return returnValue

def transferToEdi():
    activateEDI()
    pyautogui.doubleClick(77, -994)
    pressKey("ctrl+v", delay=0)
    pressKey("enter", delay=0)
    pressKey("tab", delay=0)
    sleep(0.3)
    pressKey("space", delay=0)

def doClaims():
    activateWindow("facets")

    # Get first Claim Number
    pressKeyList([
        "ctrl+o",
        "-3,assertTopWindow,Open",
        "ctrl+c",
        "esc"
    ])
    firstClaimNumber = pyperclip.paste()
    print(f"First: {firstClaimNumber}")

    # Open second Claim
    activateWindow("code")
    secondClaimInput = input("Claim Number: ")
    secondClaimNumber = verifyInput(secondClaimInput, "\d{12}")
    print(f"Second: {secondClaimInput}")

    activateWindow("facets")

    pressKeyList([
        "ctrl+tab",
        "ctrl+o",
        "-3,assertTopWindow,Open",
        f"-1,{secondClaimNumber}",
        "enter",
        "ctrl+down",
        "f3"
    ])

    pyperclip.copy(firstClaimNumber)
    transferToEdi()

    while True:
        try:
            pyperclip.copy(secondClaimNumber)
            transferToEdi()
            break
        except:
            sleep(0.3)
            pass
    
    print("Press Shift to continue\nCtrl to cancel")
    key = catch("shift", exitKey="ctrl", exitKey2="alt", hard=True)
    if key == "ctrl":
        return
    elif key == "alt":
        activateWindow("facets")
        pressKeyList([
            "esc",
            "ctrl+tab",
            "ctrl+down",
            "alt+e",
            "a",
            "-3,assertTopWindow,Note Attachment",
            "-1,Claim in Hx is different provider OK to allow",
            "enter"
        ])
        return
    
    startProcess(firstClaimNumber, secondClaimNumber)

def startProcess(firstClaim, secondClaim):

    # Process original Claim
    pressKeyList([
        "ctrl+tab",
        "f3",
        "-3,waitForAdj",
        "-2,0.8",
        "alt+b",
        "-3,assertTopWindow,EOB Explanation",
        "esc",
        "f4",
        "ctrl+tab"
    ])

    # Do Stuff on other claim
    pressKeyList([
        "ctrl+o",
        "enter",
        "ctrl+down",
        "f3",
        "-3,waitForAdj",
        "alt+b",
        "-3,assertTopWindow,EOB Explanation",
        "-1,OKL",
        "enter",
        "tab",
        "enter",
        "ctrl+down",
        "alt+e",
        "a",
        "-3,assertTopWindow,Note Attachment",
        f"-1,Per Clinical Edit on Claim #{firstClaim}"
    ])

    print("Press Shift to continue\nCtrl to cancel")
    key = catch("shift", exitKey="ctrl", hard=True)
    if key != "shift":
        return
    
    # Return to first claim
    pressKeyList([
        "enter",
        "f3",
        "-3,waitForAdj",
        "alt+e",
        "a",
        "-3,assertTopWindow,Note Attachment",
        "esc",
        "f4",
        "ctrl+tab",
        "ctrl+o",
        "-3,assertTopWindow,Open",
        f"-1,{firstClaim}",
        "enter",
        "ctrl+down",
        "f3"
    ])

CLAIM_AMOUNT = settings.readMath("totalClaims")
clickTypesArr = [ClickOptions.BiLaunch, ClickOptions.Excel, ClickOptions.Default]
openClaimArgs = {
    "hotkey" : "f13",
    "reprocess" : False,
    "click" : clickTypesArr[settings.readValue("click", int)],
    "f3" : True,
    "suffix" : 1,
    "moveToWindow" : True,
    "highlight" : False,
    "checkReplacement" : False
}

threading.Thread(target=parseFacilityLoc, name="FacilityParse", daemon=True).start()
Hotkey("alt+1", openClaimLoc, openClaimArgs)
Hotkey("alt+2", doClaims)
Hotkey("alt+3", startProcess)
Hotkey("shift+alt+2", transferToEdi)
add_hotkey("f4", incrementClaim)
add_hotkey("=", incrementClaim)
add_hotkey("-", incrementClaim, ("-",))
add_hotkey("shift+=", incrementClaim, ("=",))

print("Loaded")
kb.wait()