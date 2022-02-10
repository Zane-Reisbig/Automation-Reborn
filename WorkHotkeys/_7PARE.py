import os
import pyautogui
import pyperclip
import threading
from keyboard import *
from _99helperFunctions import *
from _99universalFunctions import *
from _99settingsFile import *

# class MacroBuilt():
#     def __init__(self, callBack, WindowTarget) 

#Init
activateWindow("facets")

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
isFacility = None



def parseFacilityLoc():
    global isFacility
    isFacilityLoc = None
    while True:
        isFacility = parseFacility()
        if isFacility == None:
            isFacility = isFacilityLoc
            continue

        isFacilityLoc = isFacility

def overRidePCALoc(arg2, arg3):
    global isFacility

    overRidePCA(arg2, arg3)
    
def transferOutAlt():
    global currentDate, old_data, incrementNext
    activateWindow("facets")

    print(currentTransferType["name"])
    
    #Get Date
    pressKeyList([
        "ctrl+down",
        "ctrl+up",
        "tab,5",
        "ctrl+home",
        "shift+f10",
        "a"
    ])

    old_data = pyperclip.paste()
    pressKey("ctrl+c")
    currentDate = pyperclip.paste()
    dateSplit = currentDate.split("/")
    dateSplit[-1] = str(int(dateSplit[-1]) - 1)
    currentDate1 = "/".join(dateSplit)
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

    pressKeyList([
        "tab,{}".format(amount),
        "-1,{}".format(currentDate1),
        "tab",
        "-1,{}".format(currentDate),
        "tab,1,0.8",
        "alt+r",
        "alt+y"
    ])

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

def openClaimLoc(hotkey="f13", reprocess=False, click=ClickOptions.Default, f3=True, suffix=1, moveToWindow=True, highlight=True, checkReplacement=False): 
    openClaim(hotkey, reprocess, click, f3, suffix, moveToWindow, highlight)
    waitForAdj()

    if checkReplacement:
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
        print("Percentage Done:", str(round((amountOfClaims / CLAIM_AMOUNT) * 100, 2)) + "%")
        time =  round(amountOfClaims / 23, 2)
        hours = int(time)
        minutes = int((time * 60) % 60)
        print("Time Completed: {} Hours {} Minutes".format(hours, minutes))
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

def paymentLevel():
    pressKeyList([
        "alt+o",
        "-3,assertTopWindow,Line Item Override",
        "tab,24,0",
        "-1,in",
        "tab",
        "-1,PL",
        "tab",
        "enter"
    ])


clickTypesArr = [ClickOptions.BiLaunch, ClickOptions.Excel, ClickOptions.Default]
openClaimArgs = {
    "hotkey" : "f13",
    "reprocess" : False,
    "click" : clickTypesArr[settings.readValue("click", int)],
    "f3" : True,
    "suffix" : 1,
    "moveToWindow" : True,
    "highlight" : False,
    "checkReplacement" : True 
}

transferType = {
    "subscriberID" : {
        "name" : "Subscriber",
        "lineTabAmount" : 5,
        "downAmountFacility" : 0,
        "downAmountMedical" : 2,
        "inqTabAmount" : 5,
    },

    "memberID" : {
        "name" : "Member",
        "lineTabAmount" : 5,
        "downAmountFacility" : 0,
        "downAmountMedical" : 0,
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
threading.Thread(target=parseFacilityLoc, name="FacilityParse", daemon=True).start()


Hotkey("alt+1", openClaimLoc, openClaimArgs)
Hotkey("alt+2", transferOut)
Hotkey("ctrl+alt+2", transferOutAlt)
Hotkey("alt+3", paymentLevel)
Hotkey("alt+4", overRidePCALoc, (isFacility, False))
add_hotkey("f4", incrementClaim)
add_hotkey("=", incrementClaim)
add_hotkey("-", incrementClaim, ("-",))
add_hotkey("shift+ctrl+=", incrementClaim, ("=",))
system("cls")
print("Loaded")
wait()