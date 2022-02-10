from _99helperFunctions import *
from _99universalFunctions import *
import keyboard as kb
import os
import pyperclip
import re

hcpcsLines = []
dxLines = []

def getHCPCS():
    amount = input("How Many Lines: ")
    print("Open line items\nThen Press Shift")
    catch("shift", hard=True)

    pressKeyList([
        "esc",
        "ctrl+down",
        "ctrl+up",
        "tab,4"
    ])
    
    activateWindow("facets")

    dataItem = []
    for _ in range(int(amount)):
        dataItem = []
        pressKeyList([
            "shift+f10",
            "a",
            "ctrl+c"
        ],allDelay=0.2)
        dataItem.append(pyperclip.paste())

        pressKeyList([
            "tab,2",
            "ctrl+c"
        ],allDelay=0.2)
        dataItem.append(pyperclip.paste())

        pressKeyList([
            "tab,2",
            "ctrl+c"
        ],allDelay=0.2)
        dataItem.append(pyperclip.paste())

        pressKey("tab", 4, 0)

        hcpcsLines.append(dataItem)
        system("cls")
        print(f"Last HCPCS Line\n{hcpcsLines[-1]}")

    print("--HCPCS Lines--")
    for i in hcpcsLines: print(i)


def getDxCodes():
    global dxLines
    print("Open Diagnosis Code list and put cursor at the end of the first DX\nThen Press Shift")
    catch("shift", hard=True)
    pyperclip.copy("")

    for _ in range(8):
        pressKeyList([
            "ctrl+a",
            "ctrl+c,2"
        ])
        dxLines.append(pyperclip.paste())
        pressKeyList([
            "tab,2"
        ])
        sleep(0.3)
        system("cls")
        print(f"Last DX: {dxLines[-1]}")
        
    
    print("--DX Lines--")
    for i in dxLines: print(i)

def enterHCPCS():
    for i in hcpcsLines:
        pressKeyList([
            f"-1,{i[1]}",
            "tab",
            f"-1,{i[2]}",
            "tab,4",
            "-1,{}".format(i[0].replace("/", "")),
            "tab,5"
        ])

def enterDxCodes():
    newDx = dxLines[1:]

    for i in newDx:
        pressKeyList([
            f"-1,{i}",
            "down"
        ])

def enterBasicInfo():
    activateWindow("code")
    types = {
        "Home Health" : 1
    }
    typeMethods = {
        1 : homeHealth
    }

    for i,value in enumerate(types):
        print(i + 1,":",value)


    type = input("Info Type: ")
    typeMethods[int(type)]()


def homeHealth():
    useLast = input("Use Last (Y/[N]): ")
    if(useLast != ""):
        with open("_5CMSFILE.txt", "r") as file:
            fileLines = file.read()
            fileLines = fileLines.split("\n")
            fileLines = [item for item in fileLines if item != ""]

        npi = fileLines[0]
        facilityID = fileLines[1]
        claimNumber = fileLines[2]
        fromThru = fileLines[3]
        sex = fileLines[4]
        age = fileLines[5]
        dStat = fileLines[6]
        totalCharge = fileLines[7]

    else:
        npi = input("Enter NPI: ")
        facilityID = input("Facility ID: ")
        claimNumber = input("Claim Number: ")
        fromThru = input("From-Thru (CSV): ")
        sex = input("Sex: ")
        age = input("Age: ")
        dStat = input("D-Stat: ")
        totalCharge = input("Total Charge: ")
        with open("_5CMSFILE.txt", "w") as file:
            file.write(npi + "\n" + facilityID  + "\n" + claimNumber  + "\n" + fromThru  + "\n" + sex  + "\n" + age  + "\n" + dStat  + "\n" + totalCharge)

    print("Press ctrl to continue")
    catch("ctrl", True)

    pressKeyList([
        "-1,7",
        "tab,2",
        f"-1,{npi}",
        "tab,3",
        f"-1,{facilityID}",
        "tab",
        "-1,9",
        "tab",
        f"-1,{claimNumber}",
        "tab,2",
        "-1,{}".format(fromThru.split(",")[0]),
        "tab",
        "-1,{}".format(fromThru.split(",")[1]),
        "tab,7",
        f"-1,{sex}",
        "tab",
        f"-1,{age}",
        "tab,3",
        f"-1,{dStat}",
        "tab",
        "-1,0329",
        "tab",
        f"-1,{totalCharge}"
    ], allDelay=0.3)
    print("Done")



Hotkey("alt+1", enterBasicInfo)
Hotkey("alt+2", getDxCodes)
Hotkey("alt+3", getHCPCS)
Hotkey("alt+4", enterHCPCS)
Hotkey("alt+5", enterDxCodes)
os.system("cls")
print("Loaded")
kb.wait("f3")