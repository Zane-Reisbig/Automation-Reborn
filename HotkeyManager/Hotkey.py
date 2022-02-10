from threading import Thread
import types

class Hotkey:
    """
        Holds a hotkey key combo
        Holds the callback
        Holds the arguments
        Calls the callback when triggered in a new thread as to not crash the main thread
        Holds information for the hotkey manager
    """
    def __init__(self, hotkey:str, callback:types.FunctionType, args:tuple|dict=()):
        self.hotkey = hotkey
        self.callback = callback
        self.args = args
        self.useKwargs = True if type(args) == dict else False

    def triggerCallback(self) -> None:
        if self.useKwargs:
            thread = Thread(
                target=self.callback,
                kwargs=(self.args),
                name=str(self.callback.__name__),
            )
        else:
            thread = Thread(
                target=self.callback,
                args=(self.args),
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
