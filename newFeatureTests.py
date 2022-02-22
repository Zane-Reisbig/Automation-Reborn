import keyboard
from HotkeyManager.Hotkey import Hotkey
from HotkeyManager.HotkeyManager import HotkeyManager
from HotkeyModules.SendKeys import KeySender
from HotkeyModules.AssertTopWindow import AssertTopWindow
from HotkeyModules.ActivateWindow import activateWindow

sender = KeySender(
    usedModules={
        "activate" : (activateWindow, ()),
    },
    recursionLimit=10
)
sender.addSnippet("writeNotePad", ["$write,Hello World", "%writeNotePad"])

sender.sendKeys(
    [
        "$activate,notepad",
        "%writeNotePad"
    ]
)
