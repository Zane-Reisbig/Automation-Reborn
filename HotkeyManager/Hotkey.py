import sys
sys.path.append("..")

from threading import Thread
from HotkeyModules.WaitForRelease import waitForRelease
import types


class Hotkey:
    """
        Contains information for the HotkeyManager
        hotkey:str -> the key combination i.e. "Ctrl+Shift+A"
        callback:function -> the function to be called when the hotkey is pressed
        args:tupe|dict -> the arguments to be passed to the callback function
    """
    def __init__(self, hotkey:str, callback:types.FunctionType, args:tuple|dict=()):
        self.hotkey = hotkey
        self.callback = callback
        self.args = args
        self.useKwargs = True if type(args) == dict else False

    def triggerCallback(self, passedArgs=None) -> None:
        print("Waiting For Release")
        waitForRelease(self.hotkey)

        if self.useKwargs:
            thread = Thread(
                target=self.callback,
                kwargs=self.args if passedArgs != None else None,
                name=str(self.callback.__name__),
            )
        else:
            thread = Thread(
                target=self.callback,
                args=self.args if passedArgs != None else None,
                name=str(self.callback.__name__),
            )

        thread.start()
        thread.join()

    def getHotkey(self) -> None:
        return self.hotkey
    
    def getArgs(self) -> None:
        return self.args
    
    def getCallback(self) -> None:
        return self.callback

    def getCallbackName(self) -> None:
        return self.callback.__name__

    def getUnion(self) -> None:
        return f"{self.callback.__name__} -> {self.hotkey}"
