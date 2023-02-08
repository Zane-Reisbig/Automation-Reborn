import subprocess
from HotkeyModules.SendKeys import KeySender
from HotkeyModules.AssertTopWindow import AssertTopWindow
from HotkeyModules.ActivateWindow import activateWindow

assertTop = AssertTopWindow(exact=False)
sender = KeySender(
    inlineCallables={
        "activate": (activateWindow, ()),
        "assertTop": (assertTop.assertTopWindow, ()),
    },
    recursionLimit=1
)
sender.addSnippet("writeNotePad", [
                  "$write,Hello World\n", "$write,Now I dont have to type all this out again to call it!\n"])
# Testing out the recursion limit
# It works
# I'm going to try it out and see if raising an exception is the best way to do it
# or just stop the recursion and continue sending keys


subprocess.Popen(["notepad.exe"], shell=True)

sender.sendKeys(
    [
        "$activate,notepad",
        "$assertTop,Notepad",
        "%writeNotePad",
        "$write,This is written after the snippet is called\n",
        "$wait,0.3",
        "%writeNotePad",
    ]
)


##############################
# Just some thoughts down here
# It could also really screw with complex macros if there was an accidental recursion
# It also restricts the way people can use the program which I don't want to do
# I can't believe that anyone would want to do recursion in a macro but whatever so that makes me feel a little better about it
