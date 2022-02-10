from _99helperFunctions import *
from _99universalFunctions import *
import pyautogui
import re
import os
os.system("cls")

class NoMatchError(Exception):
    """Raised When No Regex Is Found"""
    pass

mainArr = {
    "memberID" : "",
    "provID" : "",
    "receviedDate" : "",
    "identifier" : "",
    "serviceLines" : "",
    "principal" : "",
    "dxCodesAdditonal" : "",
    "receivedDate" : "",
    "originalNumber" : ""
}

def copyEDI():
    pyautogui.moveRel(300, 100)
    pyautogui.click()
    pressKeyList([
        "shift+f10",
        "a",
        "shift+f10",
        "c"
    ])

    catch("shift", hard=True)
    pyautogui.moveRel(300, 100)

    pressKeyList([
        "shift+f10",
        "down,4",
        "enter",
        "ctrl+s",
        "f",
        "f",
        "g",
        "g"
    ])

def regexCustom(prefix, regex, lines, findAll=False, snipPrefix=True, allowNone=False):
    for line in lines:
        if re.search(f"{prefix}{regex}", line):
            if not findAll:
                if snipPrefix:
                    return re.search(f"{prefix}{regex}", line).group(0)[len(prefix):]
                else:
                    return re.search(f"{prefix}{regex}", line).group(0)
            else:
                if snipPrefix:
                    return [line[len(prefix):] for line in re.findall(f"{prefix}{regex}", " ".join(lines))]
                else:
                    return re.findall(f"{prefix}{regex}", " ".join(lines))

    if allowNone:
        return None
    else:
        raise NoMatchError

def enterData():
    pressKeyList([
        "-1,{}".format(mainArr["memberID"]),
        "tab,3",
        "-1,{}".format(mainArr["provID"]),
        "tab,2",
        "-1,{}".format(mainArr["receivedDate"]),
        "tab"
    ])

    kb.write(mainArr["principal"])
    pressKey("tab", delay=0)

    total = 12
    if mainArr["dxCodesAdditonal"] != None:
        for i in mainArr["dxCodesAdditonal"]:
            kb.write(i)
            pressKey("tab")
            total -= 1
    
    pressKey("tab", total + 4, 0)

    kb.write(mainArr["identifier"])

    totalCharge = 0
    for i in mainArr["serviceLines"]:
        line = i.split(" ")
        totalCharge += float(line[6].replace("$", ""))

    pressKeyList([
        "ctrl+down",
        "tab",
        f"-1,{totalCharge}",
        "tab,2"
    ])

    for i in mainArr["serviceLines"]:
        line = i.split(" ")
        date = line[-1].replace("/", "")
        pos = line[2]
        proc = line[3]
        charge = line[6].replace("$", "")
        units = line[7]
        
        pressKeyList([
            f"-1,{date}",
            "tab",
            f"-1,{date}",
            "tab",
            f"-1,{pos}",
            "tab,2",
            f"-1,{proc}",
            "tab,2",
            f"-1,{charge}",
            "tab",
            f"-1,{units}",
            "enter,{}".format(0 if len(mainArr["serviceLines"]) else 1),
            "ctrl+down",
            "alt+e",
            "a",
            "-3,assertTopWindow,Note Attachment",
            "-1,Original Claim Number {}".format(mainArr["originalNumber"]),
            "tab",
            "-1,Per Inq {} ok to enter claim".format(inqNumber),
            "tab",
            "enter",
            "ctrl+up",
            "f3"
        ])

    
def getData():
    global mainArr

    with open("_3items.txt", "r") as file:
        fileLines = file.readlines()
        fileLines = [item.replace("\n", "").replace("\\n", "").strip() for item in fileLines]
        file.close()
    
    with open("_3items.txt", "w") as file:
        file.write("")
        file.close()


    mainArr["memberID"] = regexCustom("ID: ", "\d*", fileLines)
    mainArr["provID"] = regexCustom("NPI: ", "\d*", fileLines)
    mainArr["receivedDate"] = "Get from EDI"
    mainArr["identifier"] = regexCustom("ifier: ", "[A-Z\d]*", fileLines)
    mainArr["serviceLines"] = re.findall("Line \d* \d* .*", " ".join(fileLines))
    mainArr["principal"] = regexCustom("Principal DX ", "[A-Z\d]*", fileLines)
    mainArr["dxCodesAdditonal"] = regexCustom("Diagnosis Code: ", "[A-Z\d]*", fileLines, True, allowNone=True)
    mainArr["originalNumber"] = regexCustom("#: ", "\d{12}", fileLines)
    print(mainArr["serviceLines"])
    

def main():
    getData()
    enterData()

mainArr["receivedDate"] = "07/30/2021".replace("/", "") # Will Change
inqNumber = "2107307601972"

Hotkey("alt+1", main)
Hotkey("alt+2", copyEDI)
kb.wait("f13")