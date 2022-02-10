from _99universalFunctions import *
from _99helperFunctions import *
from _99settingsFile import *
import keyboard as kb
import re
import pyperclip as clip
import os
import threading

settings = SettingsFile("_0settingsRep.txt")
amountOfClaims = settings.readValue("amountOfClaims" , int)
isFacility = None


def openClaimLoc(hotkey="f13", reprocess=False, click=ClickOptions.Default, f3=True, suffix=1, moveToWindow=True, highlight=True, checkReplacement=False): 
    openClaim(hotkey, reprocess, click, f3, suffix, moveToWindow, highlight)
    waitForAdj()

    pressKey("ctrl+down", delay=0)

def incrementClaim(operator="+"):
    global amountOfClaims

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
        time =  round(amountOfClaims / 23, 2)
        hours = int(time)
        minutes = int((time * 60) % 60)
        print(f"Time Completed: {hours}:{minutes}")

    else:
        activateWindow("code")
        print("{} Claims reached".format(CLAIM_AMOUNT))
        input("Press enter to continue")
        activateWindow("facets")


def doClaim(dragMouse=True):
    if dragMouse:
        pag.moveTo(811, 474)
        pag.dragTo(228, 250)
    
    # Replace Data on clipboard with old value
    x = clip.paste()
    pressKey("ctrl+c", delay=0.3)
    string = clip.paste()
    clip.copy(x) 
    
    amount = "0.00"
    isAmount = True
    
    line = "1"
    isLine = True

    code = "None"
    isCode = True
    codeBypass = False
    bypassAll = False 

    if(x:= re.search("P?p?rocess", string)):
        bypassAll = True
    
    if not bypassAll:
        try:
            amount = re.search("(\$\d+\.\d{2}|deny)", string).group(0)
            if amount == "deny": amount = "0.00"
        except:
            isAmount = False

        try:
            code = re.search("([A-Z]{4}|[A-Z]{3}\d|[A-Z]{3})", string).group(0)
            if len(code) == 3:
                print(f"Code Found: {code}")
                isCode = False
                codeBypass = True
        except:
            isCode = False

        try:
            line = re.search("(\d{2}|\d{1})", re.search("(line \d{2}|line \d{1})", string).group(0)).group(0)
        except:
            isLine = False
        
        activateWindow("code")

        if not isAmount:
            amount = input("Amount not found\nAmount: ")
            if amount == "":
                amount = ""
            else:
                isAmount = True
            print()
        
        if not isCode and not codeBypass:
            code = input("Code not found\nCode: ")
            if code == "":
                code = ""
            else:
                isCode = True
            print()
        
        if not isLine:
            line = input("Line not found\nLine: ")
            if line == "":
                line = "1"

            print()
            
    activateWindow("facets")
    activateWindow("facets")
    work(amount, line, code, isAmount, isCode, codeBypass, bypassAll)

def work(amount, line, code, isAmount, isCode, codeBypass, bypassAll):

    if not bypassAll:
        pressKeyList([
            "ctrl+up",
            "alt+o",
            "-3,assertTopWindow,Line Item Override"
        ])

        if int(line) > 1:
            pressKey("alt+n", int(line) - 1, delay=0)
        else:
            pressKey("tab", delay=0)
        

        if isAmount:
            pressKeyList([
                "-1,{}".format(amount),
                "tab",
                "-1,{}".format(code if codeBypass else "OF5") 
            ])

        if codeBypass:
            pressKeyList([
                "backspace,4",
                f"-1,{code}"
            ])

        
        if isCode and not codeBypass:
            pressKeyList([
                "tab,18,0",
                "-1,{}".format(code),
                "tab",
                "-1,O87"
            ])
    else:
        overRidePCALoc(isFacility)


openClaimArgs = {
    "hotkey" : "f13",
    "reprocess" : False,
    "click" : ClickOptions.Excel,
    "f3" : True,
    "suffix" : 1,
    "moveToWindow" : True,
    "highlight" : False
}

def parseFacilityLoc():
    global isFacility
    isFacilityLoc = None
    while True:
        isFacility = parseFacility()
        if isFacility == None:
            isFacility = isFacilityLoc
            continue

        isFacilityLoc = isFacility

def overRidePCALoc(facility):
    pressKeyList([
        "ctrl+up"
    ])
    overRidePCA(facility)


CLAIM_AMOUNT = settings.readMath("totalClaims")
threading.Thread(target=parseFacilityLoc, name="FacilityParse", daemon=True).start()

Hotkey("alt+1", openClaimLoc, openClaimArgs)
Hotkey("alt+2", doClaim)
Hotkey("alt+3", overRidePCALoc, (isFacility, ))
Hotkey("ctrl+alt+2", doClaim, (False,))
kb.add_hotkey("f4", incrementClaim)
kb.add_hotkey("=", incrementClaim)
kb.add_hotkey("-", incrementClaim, ("-",))
kb.add_hotkey("shift+ctrl+=", incrementClaim, ("=",))
os.system("cls")
print("Loaded...")
kb.wait("f13")