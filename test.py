import keyboard
from HotkeyManager.Hotkey import Hotkey
from HotkeyManager.HotkeyManager import HotkeyManager
from HotkeyModules.SendKeys import KeySender
from HotkeyModules.AssertTopWindow import AssertTopWindow
from HotkeyModules.ActivateWindow import activateWindow


def printExample():
    print("This is an example")


def controlNotepad(toWrite: str, keySender: KeySender):
    keySender.sendKeys([  # Example format for sending keys and using inline functions
        "$activate,Notepad",
        "$assert,Notepad",
        "$write,{}".format(toWrite),
        "$print,Done"
    ])


def main():
    assertTop = AssertTopWindow(exact=False)
    # Controls the switching and storing of hotkeys modules

    manager = HotkeyManager("ctrl+alt+c")
    # a key combo is *required* to change the module being used

    keySender = KeySender(  # The keySender object is used to send keys to the active window
        inlineCallables={
            # The functions available to the user to call inline when sending keys
            # Functions can be passed with or without arguments
            #   - if arguments are provided in this section, and inline arguments are *also* provided, the inline arguments will be used
            #   - this allows for default arguments to be set, but also override them if needed

            "print": (print, ()),
            # Functions can be passed with no arguments

            "printHello": (print, ("Hello",)),
            # Arguments can be passed as a tuple

            "activate": (activateWindow, ()),
            # Functions will be called using the alias, not the function name itself

            "assert": (assertTop.assertTopWindow, ()),
            # Will be called with "assert" not "assertTop.assertTopWindow"
        }
    )

    manager.ADDPERSISTANT(Hotkey("ctrl+alt+v", printExample, ()))
    # Adds a persistant hotkey, which will be added to the hotkey manager
    # This will persist through module changes

    # Example of a hotkey object
    #               Key combo                  Callback                      Args
    # Hotkey(hotkey="ctrl+alt+n", callback=assertTop.assertTopWindow, args=("Notepad",))
    manager.ADDMAPPING(  # Add a mapping to the hotkey manager
        "notePad1",  # Alias for the hotkey module
        {
            "print1": Hotkey("alt+1", controlNotepad, ("One notePad1 Yea\n", keySender,)),
            "print2": Hotkey("alt+3", controlNotepad, ("Two Notepad2 Yea\n", keySender,)),
        }
    )

    # When adding a mapping only one dictionary can be passed
    # Use multiple ADDMAPPING calls to add multiple hotkey modules to the same manager
    manager.ADDMAPPING(
        "notePad2",
        {
            "print2": Hotkey("alt+2", controlNotepad, ("Two Yea\n", keySender,)),
        }
    )

    # Finalize will check the mappings for any duplicate hotkeys and warn the user
    # Also does a few more things that aren't really important to the user
    manager.FINALIZE()

    # Set the starting module after finalizing using the alias defined
    manager.SETMAPPING("notePad1")
    keyboard.wait()  # kb.wait sets the main loop for the program


if __name__ == "__main__":
    main()
