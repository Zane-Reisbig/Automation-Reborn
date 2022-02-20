import keyboard
from HotkeyManager.Hotkey import Hotkey
from HotkeyManager.HotkeyManager import HotkeyManager
from HotkeyModules.SendKeys import KeySender
from HotkeyModules.AssertTopWindow import AssertTopWindow
from HotkeyModules.ActivateWindow import activateWindow

assertTop = AssertTopWindow(addedSuffix="- Remote")
manager = HotkeyManager("ctrl+alt+c") # Controls the switching and storing of hotkeys modules
                                      # a key combo is required to change the module being used
keySender = KeySender( # The keySender object is used to send keys to the active window
    usedModules={ # The functions available to the user to call inline when sending keys 
        "print" : (print, ()), # Functions can be passed with or without arguments
        "printHello" : (print, ("Hello",)), # Arguments can be passed as a tuple, if arguments are passed inline arguments are ignored
        "activate" : (activateWindow, ()), # Functions will be called using the alias, not the function name itself
        "assert" : (assertTop.assertTopWindow, ()), # Will be called with "Assert" not "assertTop.assertTopWindow"
    }
)

keySender.addSnippet("openMenu", ["alt+o", "alt+c", "$assertTop,Menu"])
# Able to be called inline with the % prefix as %openMenu

def controlNotepad(toWrite: str):
    keySender.sendKeys([ # Example format for sending keys and using inline functions
        "$activate,.*Notepad",
        "$write,{}".format(toWrite),
        "$print,Done"
    ])


# Example of a hotkey object
#               Key combo                  Callback                      Args
Hotkey(hotkey="ctrl+alt+n", callback=assertTop.assertTopWindow, args=("Notepad",)) # Not used for anything, just for example

def openClaim():
    print("This is an example")

manager.ADDPERSISTANT(Hotkey("ctrl+alt+c", openClaim, ())) # Adds a persistant hotkey, which will be added to the hotkey manager
                                                      # This will persist through module changes

manager.ADDMAPPING( # Add a mapping to the hotkey manager
    "notePad1", # Alias for the hotkey module
    {   
        "print1" : Hotkey("alt+1", controlNotepad, ("One notePad1 Yea\n",)),
        "print2" : Hotkey("alt+3", controlNotepad, ("Two Notepad2 Yea\n",)),
    }
)

# When adding a mapping only one dictionary can be passed
# Use multiple ADDMAPPING calls to add multiple hotkey modules to the same manager
manager.ADDMAPPING(
    "notePad2",
    {
        "print2" : Hotkey("alt+2", controlNotepad, ("Two Yea\n",)),
    }
#  Will not work    
#  "Alias2" :
#   {
#       "print3" : Hotkey("alt+3", controlNotepad, ("Three Yea\n",)),
#   }
)

# Finalize will check the mappings for any duplicate hotkeys and warn the user
# Also does a few more things that aren't really important to the user 
manager.FINALIZE()

manager.SETMAPPING("notePad1") # Set the starting module after finalizing
keyboard.wait() # kb.wait sets the main loop for the program