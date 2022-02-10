import winsound
import os
import re
import pyautogui
import pyperclip
import threading
from keyboard import *
from ._99helperFunctions import *
from ._99universalFunctions import *
from ._99settingsFile import *

# class MacroBuilt():
#     def __init__(self, callBack, WindowTarget) 

#Init
activateWindow("facets")
#External Settings
settings        = SettingsFile(r"C:\Users\zaned\Desktop\Currently Working On\Current Projects\Python\__Automation Rebuilt\WorkHotkeys\_0settingsRep.txt")
amountOfClaims  = settings.readValue("amountOfClaims" , int)
incrementNext   = settings.readValue("incrementNext"  , bool)
replaceOriginal = settings.changeValue("replaceOriginal", "True", True, bool)

#Internal Settings
currentDate = ""
old_data    = ""
claimNumber = ""
currentSearch = "Subscriber ID"
lastCommand = None
isFacility = None
pauseAfter = False

#Functions
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
    global pauseAfter
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
    
    pauseAfter = False


def switcher(toSwitch):
    global incrementNext, replaceOriginal

    if toSwitch == "incrementNext":
        incrementNext = settings.changeValue("incrementNext", not incrementNext, True, bool)
        os.system("cls")
        print("incrementNext: {}".format(incrementNext))
    elif toSwitch == "replaceOriginal":
        replaceOriginal = settings.changeValue("replaceOriginal", not replaceOriginal, True, bool)
        os.system("cls")
        print("replaceOriginal: {}".format(replaceOriginal))

def transferOut(other=False):
    global currentDate, old_data, incrementNext
    activateWindow("facets")

    print(currentTransferType["name"])
    
    #Get Date
    if not other:        
        pressKeyList([
            "ctrl+down",
            "ctrl+up",
            "tab,5",
            "ctrl+home",
            "shift+f10",
            "a"
        ])
    else:
        pressKeyList([
            "shift+f10",
            "a"
        ])

    old_data = pyperclip.paste()
    pressKey("ctrl+c")
    currentDate = pyperclip.paste()
    pyperclip.copy(old_data)

    if isFacility:
        down = currentTransferType["downAmountFacility"]
    else:
        down = currentTransferType["downAmountMedical"]

    amount = currentTransferType["inqTabAmount"]

    pressKeyList([
        "alt+t",
        "c",
        "enter",
        "down,{}".format(down),
        "enter"
    ])

    #Open in Claims Inquiry
    assertTopWindow("Claims Inquiry")

    if other:
         pressKeyList([
            "tab,{}".format(amount + 1),
            "-1,{}".format(currentDate),
            "shift+tab"
        ])
    else:    
        pressKeyList([
            "tab,{}".format(amount),
            "-1,{}".format(currentDate),
            "tab",
            "-1,{}".format(currentDate),
            "tab,1,0.8",
            "alt+r",
            "alt+y"
        ])

def putDate():
    pressKeyList([
        "-1,{}".format(currentDate),
        "tab",
        "-1,{}".format(currentDate),
    ])

def getDate():
    global old_data, currentDate

    old_data = pyperclip.paste()
    pressKeyList([
        "shift+f10",
        "a",
        "shift+f10",
        "c"
    ])

    currentDate = pyperclip.paste()
    pyperclip.copy(old_data)

def replaceClaim():
    activateWindow("facets")

    if replaceOriginal:
        replaceOriginalFunc()
    else:
        replaceRequestedFunc()

def replaceOriginalFunc():
    activateWindow("facets")
    global replaceOriginal, incrementNext, amountOfClaims

    print(isFacility)
    pressKeyList([
        "alt+t",
        "{},{}".format("H" if isFacility else "M", "3" if isFacility else "4"),
        "enter"
    ])
    
    waitForAdj()

    pressKeyList([
        "ctrl+down,2",
        "alt+e",
        "a",
        "-3,assertTopWindow,Note Attachment",
        "-1,See Replacment Claim: {}".format(pyperclip.paste()),
        "-2,0.6",
        "enter",
        "ctrl+up",
        "-2,0.6",
        "alt+o",
        "alt+c",
        "-3,assertTopWindow,Claim Overrides",
        "shift+tab,{}".format(10 if isFacility else 9),
        "space",
        "tab",
        "-1,OX6"
    ])

    old_data = pyperclip.paste()
    pressKeyList([
        "shift+f10",
        "a",
        "shift+f10",
        "c"
    ], 0.3)
    
    clipboardContents = pyperclip.paste()
    if clipboardContents == "OER":
        pressKeyList([
            "shift+tab",
            "space",
            "shift+tab",
            "space",
            "tab",
            "-1,OX6"
        ])
        pressKeyList([
            "shift+f10",
            "a",
            "shift+f10",
            "c"
        ], 0.3)

        if(pyperclip.paste() != "OX6"): 
            winsound.Beep(2500, 500)
            print("OX6 Not Found\nCorrect and press CTRL")
            catch("ctrl", hard=True)

    elif clipboardContents != "OX6":
        winsound.Beep(2500, 500)
        print("OX6 Not Found\nCorrect and press CTRL")
        catch("ctrl", hard=True)

    pyperclip.copy(old_data)

    pressKeyList([
        "enter,2",
        "ctrl+o",
        "right",
        "space",
        "ctrl+c"
    ])

    pressKeyList([
        "esc",
        "alt+b,1,1.5",
        "-3,assertTopWindow,EOB Explanation",
        "-1,K33",
        "enter",
        "tab",
        "enter",
        "f3"
    ])
    waitForAdj()

    os.system("cls")
    print("Last Command: Replaced Original Claim")
    print("Press Shift to continue")
    pressKey("f4", 1)
    replaceOriginal = settings.changeValue("replaceOriginal", "False", True, bool)
    incrementClaim()

    windowText = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    y = "Medical" if isFacility else "Hospital"
    while True:
        windowText = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        regex = re.search(f"Unassigned|Inquiry|{y}", windowText)
        if not regex:
            break
        pressKey("ctrl+shift+tab", delay=0.2)
        sleep(0.5)

    replaceRequestedFunc()

def replaceRequestedFunc():
    global replaceOriginal, replacedLastClaimAuto
    activateWindow("facets")

    pressKeyList([
        "ctrl+o",
        "enter",
        "ctrl+down",
        "f3",
        "-3,waitForAdj",
        "ctrl+down",
        "alt+e",
        "a,1,0.6",
        "-3,assertTopWindow,Note Attachment",
        "-1,Replaced Claim: {}".format(pyperclip.paste()),
        "enter",
        "ctrl+up"
    ])

    overRidePCA(isFacility, False)
    os.system("cls")
    print("Last Command: Replaced Requested Claim")
    print("Waiting for F4")

    print(f"Pause After: {pauseAfter}")
    key = catch("shift", exitKey="ctrl", time=1)
    if pauseAfter: key = "shift"

    # check if getting new claim
    if key != "shift":
        pressKey("f4", delay=0)

        if openClaimArgs["click"] == ClickOptions.Excel:
            incrementClaim(getNewClaim=True)
        else:
            incrementClaim()

    replaceOriginal = settings.changeValue("replaceOriginal", "True", True, bool)


def overRidePCALoc(arg2, arg3):
    global isFacility

    overRidePCA(arg2, arg3)

def incrementClaim(operator="+", getNewClaim=None):
    global claimNumber, amountOfClaims, pauseAfter
    
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
        print("Percentage Done:", str(round((amountOfClaims / CLAIM_AMOUNT) * 100, 2)) + "%")
        time =  round(amountOfClaims / 23, 2)
        hours = int(time)
        minutes = int((time * 60) % 60)
        print(f"Time Completed: {hours}:{minutes}")
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
        pauseAfter = False

def oneOff():
    waitForRelease("alt+7")
    activateWindow("facets")
    
    pressKeyList([
        "alt+o",
        "alt+c",
        "tab,15",
        "space",
        "tab",
        "-1,PCO",
        "tab",
        "space",
        "tab",
        "-1,098",
        "enter,2",
        "f3"
    ])

def voidClaim(claimNumberLoc=None):
    global isFacility

    if claimNumberLoc == None:
        activateWindow("code")
        claimNumberLoc = input("Claim Number: ")
    
    while len(claimNumberLoc) != 12:
        claimNumberLoc = input("Invalid Claim Number\nClaim Number: ")
        if claimNumberLoc == "-1": return


    activateWindow("facets")

    # Requested Claim
    pressKeyList([
        "ctrl+tab",
        "ctrl+o",
        "-3,assertTopWindow,Open",
        f"-1,{claimNumberLoc}",
        "enter",
        "ctrl+down",
        "alt+o",
        "alt+c",
        "-3,assertTopWindow,Claim Overrides",
        "shift+tab,{}".format("10" if isFacility else "9"),
        "space",
        "tab",
        "-1,OX6",
        "enter,2",
        "alt+b",
        "-3,assertTopWindow,EOB Explanation",
        "-1,K39",
        "enter",
        "tab",
        "enter",
        "ctrl+down",
        "alt",
        "e",
        "a",
        "-3,assertTopWindow,Note Attachment",
        f"-1, Void Per Claim: {pyperclip.paste()}",
        "enter",
        "ctrl+o",
        "alt+n",
        "ctrl+c",
        "esc",
        "f3",
        "-3,waitForAdj",
        "ctrl+up"
    ])

    print("Press Shift to continue")
    catch("shift", hard=True)

    pressKey("f4")
    incrementClaim()

    # Original Claim
    pressKeyList([
        "ctrl+shift+tab",
        "ctrl+o",
        "enter",
        "f3",
        "-3,waitForAdj",
        "ctrl+down,2",
        "alt",
        "e",
        "a",
        "-3,assertTopWindow,Note Attachment",
        f"-1, Voided Claim: {pyperclip.paste()}",
        "enter",
        "f3",
        "-3,waitForAdj",
        "alt",
        "f",
        "s",
        "c",
        "-1,{}".format("C423" if isFacility else "C424"),
    ])

def ediCopy():
    waitForRelease("ctrl+c")

    if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Viewer Printer":
        pressKeyList([
            "shift+f10",
            "c"
        ])

def transferToEdi():
    activateEDI()
    pyautogui.doubleClick(77, -994)
    pressKey("ctrl+v", delay=0)
    pressKey("enter", delay=0)
    pressKey("tab", delay=0)
    sleep(0.3)
    pressKey("space", delay=0)

def console():
    global lastCommand, pauseAfter
    args = ()
    command = ""
    activateWindow("code")
    pressKey("alt+v, t, backspace, backspace")

    command = input("Command: ")
    if ";" in command:
        args = command.split(";")
        args = args[1:]
        args = "".join(args).split(",")

    command = command.split(";")[0] if ";" in command else command

    funcDict = {
        "void" : voidClaim,
        "oneOff": oneOff,
        "replaceReq": replaceRequestedFunc,
        "replaceOrig": replaceOriginalFunc,
        "switch" : switcher,
        "l" : listAmount,
        "list" : listAmount,
    }
    if command.strip() in ["q", "quit", " ", ""]:
        return
    elif command.strip() in ["info", "i"]:
        try:
            print(funcDict[args[0]].__code__.co_varnames)
            return
        except:
            print("Requested function does not exist")
    elif command.strip() == ".":
        command = lastCommand
    elif command.strip() in ["stopAfter", "sa", "pauseAfter", "pa"]:
        pauseAfter = True
        print(f"Pause After claim complete: {pauseAfter}")
        return


    try:
        funcDict[command.strip()](*args)
        lastCommand = command.strip()
    except:
        print("Command Not Recognized")

def listAmount():
    print(f"Amount of Claims: {amountOfClaims}")

def switchMode():
    global currentTransferType
    
    i = 0
    types = ["subscriberID", "memberID", "serviceProvider"]
    while True:
        system("cls")
        print(f"Transfer Type: {types[i]} : {transferType[types[i]]}\nPress Shift to cycle thru\nPress Ctrl to exit")
        key = catch("shift", True, exitKey="ctrl")
        if key == "shift":
            i = i+1 if i != 2 else 0
        else:
            break

    currentTransferType = transferType[types[i]]
    print(f"Selected Type: {types[i]} : {transferType[types[i]]}")

def switchMode2():
    global isFacility
    isFacility = not isFacility
    print("{}".format("Hospital Claim" if isFacility == True else "Medical Claim"))

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

transferType = {
    "subscriberID" : {
        "name" : "Subscriber",
        "lineTabAmount" : 5,
        "downAmountFacility" : 0,
        "downAmountMedical" : 1,
        "inqTabAmount" : 5,
    },

    "memberID" : {
        "name" : "Member",
        "lineTabAmount" : 5,
        "downAmountFacility" : 2,
        "downAmountMedical" : 1,
        "inqTabAmount" : 5,
    },

    "serviceProvider" : {
        "name" : "Service Prov",
        "lineTabAmount" : 5,
        "downAmountFacility" : 2,
        "downAmountMedical" : 1,
        "inqTabAmount" : 6,        
    }
}

currentTransferType = transferType["memberID"]
CLAIM_AMOUNT = settings.readMath("totalClaims")

Hotkey("alt+1", openClaimLoc, openClaimArgs)

Hotkey("alt+2", transferOut)
Hotkey("ctrl+alt+2", transferOut, (True,))
Hotkey("shift+alt+2", transferToEdi)

Hotkey("alt+3", replaceClaim)

Hotkey("alt+4", overRidePCALoc, (isFacility, True))
Hotkey("ctrl+alt+4", overRidePCALoc, (isFacility, False))

Hotkey("alt+6", putDate)
Hotkey("alt+ctrl+6", getDate)

Hotkey("alt+7", oneOff)

Hotkey("ctrl+shift+:", console)
Hotkey("]",  switcher, ("replaceOriginal",))
Hotkey("\\", switchMode)
Hotkey("alt+\\", switchMode2)

add_hotkey("f4", incrementClaim)
add_hotkey("=", incrementClaim)
add_hotkey("-", incrementClaim, ("-",))
add_hotkey("shift+ctrl+=", incrementClaim, ("=",))
add_hotkey("ctrl+c", ediCopy)

threading.Thread(target=parseFacilityLoc, name="FacilityParse", daemon=True).start()

os.system("cls")
print("Loaded")
print(currentSearch)
print("Hospital" if isFacility else "Medical" + " Claim")