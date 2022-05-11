import sys
sys.path.append("..")

import re
import pyperclip
import win32gui
import threading
from time import sleep
from keyboard import *
from HotkeyModules.AssertTopWindow import AssertTopWindow
from HotkeyModules.SendKeys import KeySender
from HotkeyModules.Catch import hardCatch, softCatch
from HotkeyModules.ActivateWindow import activateWindow


class UniversalFunctions:
    """
    A set of functions to help process claims
    """
    def __init__(self, doF3:bool):
        self.currentDate = ""
        self.old_data = ""
        self.storedState = ""
        self.claimNumber = ""
        self.isFacility = False
        self.doF3 = doF3

        assertTop = AssertTopWindow(
            "",
            exact=False
        )
        assertExactRemote = AssertTopWindow(
            " - \\\\Remote",
            exact=True
        )
        self.sender = KeySender(
            {
                "assertFacets" : (assertTop.assertTopWindow, ("Facets",)),
                "assertEOB" : (assertExactRemote.assertTopWindow, ("EOB Explanation",)),
                "assertClaimOverride" : (assertExactRemote.assertTopWindow, ("Claim Overrides",)),
                "assertLineOverride" : (assertExactRemote.assertTopWindow, ("Line Item Overrides",)),

            },
        )

        threading.Thread(target=self._parseFacility, daemon=True)
    
    def _getWindowName(self):
        return (
            win32gui.GetWindowText(
                win32gui.GetForegroundWindow()
            )
        )
    
    def _checkAndSetClipboard(self):
        if self.storedState in ["\r\n", "\r", "\n", " ", ""]:
            print("System Paused, No contents on clipboard\nPress shift to continue")
            hardCatch("shift")
        elif re.search("\w\s+\w", self.old_data) != None:
            print("There is a space on the clipboard\nPress shift to continue.")
            hardCatch("shift")
        
        self.storedState - self.storedState.replace("\n", "")
        self.storedState = pyperclip.paste()
    
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
    
    def waitForAdj(self):
        self.sender.sendKeys([
            "alt+b",
            "$assertEOB",
            "$wait,0.5",
            "esc"
        ])
    
    def openClaim(self):
        self.old_data = pyperclip.paste()
        self.sender.sendKeys(["ctrl+c,2"])
        self._checkAndSetClipboard()

        activateWindow("Facets")

        self.sender.sendKeys([
            "enter,2",
            "ctrl+o",
            "$assertFacets",
            f"$write,{self.storedState}",
            "enter",
            "ctrl+down",
            "f3,{}".format("1" if self.doF3 else "0")
        ])

    def overridePCO(self):
        activateWindow("facets")

        self.sender.sendKeys([
            "alt+o",
            "-3,assertTopWindow,Line Item Override",
            "alt+c",
            "-3,assertTopWindow,Claim Overrides",
            "tab,{},0".format(14 + 1 if self.isFacility else 0),
            "space",
            "tab",
            "-1,PCO",
            "enter,2",
            "-2,0.6"
        ])

    def openClaimOverride(self):
        self.sender.sendKeys([
            "alt+a",
            "o",
            "c",
            "$assertClaimOverride"
        ])
    
    def openLineOverride(self):
        self.sender.sendKeys([
            "alt+o",
            "$assertLineOverride"
        ])
    
    def cycleTabs(self):
        windowText = self._getWindowName()
        searchTab = "Medical" if self.isFacility else "Hospital"

        while True:
            windowText = self._getWindowName()
            regex = re.search(f"Unassigned|Inquiry|{searchTab}", windowText)
            if not regex:
                break
            self.sender.sendKeys(["ctrl+shift+tab"])
            sleep(0.3)

        