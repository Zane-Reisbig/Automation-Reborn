from os import system
from time import sleep
from _99universalFunctions import *
from _99helperFunctions import *
import pyautogui
import keyboard as kb

settings        = SettingsFile("_0settingsRep.txt")
amountOfClaims  = settings.readValue("amountOfClaims" , int)

def incrementClaim(operator="+", amountOfClaims=0):
    
    if operator == "+":
        amountOfClaims = settings.changeValue("amountOfClaims", str(amountOfClaims + 1), True, int)
    elif operator == "-":
        amountOfClaims = settings.changeValue("amountOfClaims", str(amountOfClaims - 1), True, int)
    elif operator == "=":
        amountOfClaims = settings.changeValue("amountOfClaims", "0", True, int)
    else:
        raise ArgumentError("Unknown passed")

    os.system("cls")

def incrementClaim(operator="+"):
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

def changeAllowedMode(doZeros):
    amount = 1
    amounts = []

    activateWindow("code")
    pressKey("alt+v, t, backspace, backspace", delay=0)
    lines = input("Line Amount: ")
    if lines == "":
        lines = 2
    else:
        lines = int(lines)
    activateWindow("facets")
    sleep(0.5)

    for i in range(0, lines):

        pressKey("alt+c", delay=0)
        assertTopWindow("Coordination Of Benefits")
        kb.write("C")

        pyautogui.moveTo(556, 311)
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(778, 338, 0.3)
        pyautogui.mouseUp(button="left")
        
        pressKey("tab", 9, delay=0)
        pressKey("f2", delay=0)

        activateWindow("code")
        if not doZeros:
            allowed = input("Allowed: ")
            try:
                amounts.append(float(allowed) if allowed != '' else 0.0)
            except:
                allowed = input(f"Conversion failure on {allowed}: ")
                amounts.append(float(allowed) if allowed != '' else 0.0)
        else:
            allowed = 0
            amounts.append(0)

        activateWindow("facets")  

        pressKeyList([
            "f2",
            f"-1,{allowed}",
            "shift+tab",
            "f2",
            f"-1,{allowed}",
            "enter,{}".format("0" if i+1 == lines else "1")
        ])

        sleep(0.4)

        if i == 0:
            pressKeyList(["tab,4"])
        
        pressKeyList([f"down,{i + 1}"])

        amount += 1

    pressKey("shift+tab", 11 if not isFacility else 7, delay=0)
    total = 0
    for item in amounts:
        total += item

    system("cls")
    print("Total:", round(total, 3))
    pressKey("f2", delay=0)
    kb.write(str(round(total, 3)))
    kb.send("tab")
    pressKey("f2", delay=0)
    kb.write(str(round(total, 3)))

def singleLiner():

    activateWindow("code")
    pressKey("alt+v, t, backspace, backspace", delay=0)
    amount = input("Amount: ")
    activateWindow("facets")
    activateWindow("facets")

    pressKeyList([
        "alt+c,2",
        "-3,assertTopWindow,Coordination Of Benefits",
        "-1,C",
        "tab",
        "f2",
        "-1,{}".format(amount),
        "tab",
        "f2",
        "-1,{}".format(amount),
        "tab",
        "enter"
    ])

def changeFacility():
    global isFacility

    isFacility = not isFacility
    print(f"Facility Value: {isFacility}")


clickTypesArr = [ClickOptions.BiLaunch, ClickOptions.Excel, ClickOptions.Default]
openClaimArgs = {
    "hotkey" : "f13",
    "reprocess" : False,
    "click" : clickTypesArr[settings.readValue("click", int)],
    "f3" : True,
    "suffix" : 1,
    "moveToWindow" : True,
    "highlight" : False
}

isFacility = False
CLAIM_AMOUNT = settings.readMath("totalClaims")

Hotkey("alt+1", openClaim, openClaimArgs)
Hotkey("alt+2", singleLiner)
Hotkey("alt+3", changeAllowedMode)
Hotkey("ctrl+3", changeAllowedMode, (True,))
Hotkey("]", changeFacility)
kb.add_hotkey("f4", incrementClaim)
kb.add_hotkey("=", incrementClaim)
kb.add_hotkey("-", incrementClaim, ("-",))
kb.add_hotkey("shift+=", incrementClaim, ("=",))
system("cls")
print("Loaded")
kb.wait("f13")

