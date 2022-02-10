import os
from keyboard import add_hotkey as addHotkey, wait
from pyautogui import click, hotkey
from win32gui import error
from _99settingsFile import *
from _99helperFunctions import *
from _99universalFunctions import *

settings = SettingsFile("_1settingsConf.txt")
red = [3, 0, 4]     #default [3, 0, 4] 
yellow = [3, 0, 2]  #default [3, 0, 2]
green = [3, 0, 0]   #default [3, 0, 0]
                    #         u  r  l
autoWaitTime = 10

#                       #
#   Helper Functions    #
#                       #

def errorOut(color="", note="", modup=0, modright=0, modleft=0):

    #highlightExcel(color=color)
    highlightExcel(customColor=True, modUp=modup, modLeft=modleft, modRight=modright, note=note)
    sleep(0.5)
    pressKey("down")
    openClaim(click=False)

def console():
    waitForRelease(consoleBind)
    activateWindow("code")
    commands = ["rc", "reset claims", "hc"]

    command = input("Command: ").lower()
    while command[0:2] not in commands:
        command = input("Command not recognized: ").lower()

    try:
        if command in ["reset claims", "rc"]:
            claimAdj(settings, "claimNumber", 'r')
        elif command[0:2] == "hc":
            functions = command.split("/")
            errorMode(functions[1].strip(), functions[2].strip())
        elif command == "exit":
            return
    except:
        print("Command Failed, check paramaters.")
        console()
        

def errorMode(color, note):

    if color.lower() == "red":
        activateWindow("facets")
        errorOut(True, note, red[0], red[1], red[2])
    elif color.lower() == "yellow":
        activateWindow("facets")
        errorOut(True, note, yellow[0], yellow[1], yellow[2])

#                       #
#   Working Functions   #
#                       #


def eobAndNote():

    pressKeyList([
        "esc",
        "alt+b,1,0.7",
        "-3,assertTopWindow,EOB Explanation",
        "-1,{}".format(settings.readValue("eobCode").replace("\n", "")),
        "enter,1,0.7",
        "tab",
        "enter,1",
        "-2,0.8",
        "ctrl+down",
        "alt+e",
        "a",
        "-3,assertTopWindow,Note Attachment",
        "-1,Config Log: {}".format(settings.readValue("note")),
        "tab",
        "-1,{}".format(settings.readValue("noteBody")),
        "-1,\nEOB: {}".format(settings.readValue("eobCode")),
        "tab",
        "enter",
        "f3"
    ])
    waitForAdj()

    pressKey("f4")
    key = catch("ctrl", time=0.7)
    if  key == "" or "ctrl":
        sleep(0.7)
        getNewClaim()
    

def getNewClaim(highlight = True):

    #highlightExcel(color=color)
    if highlight:
        highlightExcel(customColor=True, modUp=green[0], modRight=green[1], modLeft=green[2])
    else:
        activateWindow("excel")

    pressKey("down")

    repro = settings.readValue("repro", bool)

    ###Change F3
    openClaim(click=False, moveToWindow=True, reprocess=repro)


def doClaim():
    claimNumber = settings.readValue("claimNumber", int)
    while True:
        claimDoneFlag = False

        altFlag = False
        ctrlFlag = False


        pressKeyList([
            "ctrl+down",
            "ctrl+up",
            "tab,4",
            "ctrl+home",
            "tab,4"
        ])

        sleep(0.3)

        for i in range(15):
            pressKey("down")
            sleep(0.3)
            if kb.is_pressed("alt"):
                waitForRelease("alt")
                altFlag = True
                break
            elif kb.is_pressed("ctrl"):
                waitForRelease("ctrl")
                ctrlFlag = True
                break

        pressKeyList([
            "shift+tab",
            "-2,0.3",
            "tab"
        ])
        
        print("CTRL to mark green and continue\nALT to skip and not mark\nSHIFT to mark RED still denying")
        if not altFlag and not ctrlFlag:
            catch("ctrl", exitKey="shift", exitKey2="alt", hard=True) if not altFlag else "alt"
        elif altFlag:
            key = "alt"
        elif ctrlFlag:
            key = "ctrl"

        if key == "ctrl":
            claimDoneFlag = True
            eobAndNote()
        elif key == "shift":
            errorOut("red", "still Denying")
        else:
            getNewClaim(False)

        os.system("cls")

        if claimDoneFlag:
            claimNumber = settings.readValue("claimNumber", int)
            claimNumber = claimNumber + 1
            settings.changeValue("claimNumber", claimNumber)

        print("Claim Amount", claimNumber)

        if claimNumber >= 50:
            print("50 Claims reached")
            catch("ctrl", hard=True)
            settings.changeValue("claimNumber", 0)
            claimNumber = 0


openClaimArgs = {
    "hotkey" :"f13", 
    "reprocess" : False,
    "click" : True,
    "clickAmount" : 1,
    "f3" : True,
    "suffix" : 1,
    "moveToWindow" : True
}

errorOut1Args = {
    "color" : "",
    "note" : "",
    "modup" : 0,
    "modright" : 0,
    "modleft" : 0 
}

errorOut2Args = {
    "color" : "",
    "note" : "",
    "modup" : 0,
    "modright" : 0,
    "modleft" : 0 
}

Hotkey("alt+1", openClaim, openClaimArgs, True)
Hotkey("alt+2", doClaim)
Hotkey("alt+3", eobAndNote)
Hotkey("alt+4", getNewClaim)

Hotkey("alt+9", errorOut, errorOut1Args, True)
Hotkey("alt+0", errorOut, errorOut2Args, True)

consoleBind =        "ctrl+shift+0"; addHotkey(consoleBind, console)
incrementClaimBind = "=" ; addHotkey(incrementClaimBind, claimAdj, (settings, "claimNumber", "+"))
incrementClaimBind = "-" ; addHotkey(incrementClaimBind, claimAdj, (settings, "claimNumber", "-"))
os.system("cls")
os.system("cls")

print("loaded")
wait("f1")