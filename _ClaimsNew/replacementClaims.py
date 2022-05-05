import sys
sys.path.append("..")

import winsound
import os
import re
import pyautogui
import pyperclip
import threading
import win32gui
from keyboard import *
from HotkeyModules.AssertTopWindow import AssertTopWindow
from HotkeyModules.SendKeys import KeySender
from HotkeyModules.Catch import hardCatch, softCatch
from HotkeyModules.ActivateWindow import activateWindow

from universalFunctions import UniversalFunctions

class ReplacementClaims:    

    def __init__(self):
        self.isFacility = None
        self.clipboardData = ""
        self.replaceOriginal = False
        self.assertRemote = AssertTopWindow(" - \\\\Remote")
        self.assertTop = AssertTopWindow()
        self.universalF3 = UniversalFunctions(True)
        self.universal = UniversalFunctions()
        self.sender = KeySender(
            {
                "assertRemote" : (self.assertRemote.assertTopWindow, ()),
                "assertTop" : (self.assertTop.assertTopWindow, ()),
                "waitForAdj" : (self.universal.waitForAdj, ())
            }
        )
        threading.Thread(target=self._parseFacility, daemon=True)
   
    def _parseFacility(self):
        while True:
            windowName = self._getWindowName()
            if re.search("Medical", windowName):
                self.isFacility = False
            elif re.search("Hospital"):
                self.isFacility = True
            else:
                return self.isFacility

            return self.isFacility
   
    def setClipboard(self):
        self.clipboardData = pyperclip.paste()
    
    def setSystemClipboard(self, item:str="", useOld:bool=True):

        if not useOld:
            pyperclip.copy(item)
        else:
            pyperclip.copy(self.clipboardData)
    
    def getOldClipboard(self) -> str:
        return self.clipboardData
    
    def getCurrentClipboard(self) -> str:
        return pyperclip.paste()

    def transferOut(self, JSONAttr:dict, alt:bool=False):
        currentDate = ""
        downAmountFacility = JSONAttr["downAmountFacility"]
        downAmountMedical = JSONAttr["downAmountMedical"]
        lineTabAmount = JSONAttr["lineTabAmount"]
        activateWindow("facets")

        if not alt:
            self.sender.sendKeys([
                "ctrl+down",
                "ctrl+up",
                "tab,5",
                "ctrl+home",
                "shift+f10",
                "a"
            ])
        else:
            self.sender.sendKeys([
                "shift+f10",
                "a"
            ])
        
        self.setClipboard()
        self.sender.sendKeys(["ctrl+c"])

        currentDate = self.getCurrentClipboard()
        self.setSystemClipboard()

        self.sender.sendKeys([
            "alt+t",
            "c",
            "enter",
            "down,{}".format(downAmountFacility if self.isFacility else downAmountMedical ),
            "enter",
            "$assertRemote,Claims Inquiry",
        ])

        if alt:
            self.sender.sendKeys([
                f"tab,{lineTabAmount}",
                f"$write,{currentDate}",
                "shift+tab"
            ])
        else:
            self.sender.sendKeys([
                "tab,{}".format(lineTabAmount),
                "-1,{}".format(currentDate),
                "tab",
                "-1,{}".format(currentDate),
                "tab,1,0.8",
                "alt+r",
                "alt+y"
            ])
    
    def replaceDecider(self):
        if self.replaceOriginal:
            self.replaceOrginal
        else:
            self.replaceNew

    def replaceOriginal(self):
        self.sender.sendKeys([
            "alt+t",
            "{},{}".format("H" if self.isFacility else "M", "3" if self.isFacility else "4"),
            "enter",
            "$waitForAdj",
            "ctrl+down,2",
            "alt+e",
            "a",
            "$assertRemote,Note Attachment",
            "$write,See Replacment Claim: {}".format(pyperclip.paste()),
            "enter",
            "ctrl+up",
            "alt+o",
            "alt+c",
            "$assertRemote,Claim Overrides",
            "shift+tab,{}".format(10 if self.isFacility else 9),
            "space",
            "tab",
            "$OX6"
        ])

        self.setClipboard()

        self.sender.sendKeys([
            "shift+f10",
            "a",
            "shift+f10",
            "c"
        ])

