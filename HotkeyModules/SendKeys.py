import keyboard as kb
import types
import os
from time import sleep

class KeySender:
    """
        This function is used to type and send keystrokes to the computer
        See example in test.py for example usage
    """
    def __init__(self,
        usedModules:dict[str, tuple[types.FunctionType, tuple|dict]],
        debug:bool=False,
        debugCommands:dict[str, str|int|bool]={}) -> None:

        self.allDelay = None
        self.logAll = False
        self.usedModules = usedModules
        self.debug = debug
        self.debugCommands = debugCommands
        # Current Debugs:
        # Must be passed as a dictionary with the following keys:
        # allDelay:int -> Every action will have this amount of delay
        # logAll:bool -> Every action will be logged to the console

        self.reservedPrefixes = [
            "write",
            "wait",
        ]
        # Functions that can be called inline without importing them

    def _setDebugs(self):
        if len(self.debugCommands) == 0:
            raise Exception("No debug commands were given.")
        
        if "allDelay" in self.debugCommands:
            self.allDelay = self.debugCommands["allDelay"]
        if "logAll" in self.debugCommands:
            self.logAll = self.debugCommands["logAll"]


    def _getPrefix(self, string):
        if "," in string:
            return string[1:string.index(",")]
        else:
            return string[1:]

    def _checkPause(self):
        if kb.is_pressed("pause"):
            sleep(0.4)
            while True:
                if kb.is_pressed("pause"):
                    break
                sleep(0.1)
    
    def _convert(self, value:str, conversion:str) -> str:
        value = value[0:value.index(":")]
        if conversion == "bool":
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
            else:
                raise Exception(f"{repr(value)} is not a valid boolean value.")
        elif conversion == "int":
            return int(value)
        else:
            return value

    def sendKeys(self, keyList:list[str]) -> None:
        if self.debug:
            self._setDebugs()
        
        for key in keyList:
            prefix = None
            handled = False

            if key.startswith("$"):
                prefix = self._getPrefix(key)

            if prefix != None:
                if prefix not in self.reservedPrefixes:
                    function = self.usedModules[prefix][0] 

                    if "," in key:
                        args = (key.split(",")[1:])
                        for i in args:
                            if ":" in i:
                                selectedElement = args.index(i)
                                conversionValue = i[i.index(":")+1:]
                                args[selectedElement] = self._convert(args[selectedElement], conversionValue)
                        args = tuple(args)
                        
                    else:
                        args = self.usedModules[prefix][1]

                    if type(args) == tuple:
                        returnVal = function(*args)
                    elif type(args) == dict:
                        returnVal = function(**args)

                    if returnVal == False:
                        raise Exception(f"Function {function.__name__} returned False. Operation Cancelled.")

                    handled = True
                    if self.logAll:
                        print(f"{repr(prefix)} called using {repr(args)}")
            
            if not handled:
                if prefix == "write":
                    kb.write(key[key.index(",")+1:])
                    handled = True
                    if self.logAll:
                        print(f"{repr(key)} written")
            
            if not handled:
                if prefix == "wait":
                    args = float(key[key.index(",")+1:])
                    if self.logAll:
                        print(f"Waiting for {repr(args)} seconds")

                    sleep(args)
                    handled = True
            
            if not handled:
                inLineArgs = key.split(",")[1:]
                amount = 1
                waitTime = 0.4
                if "," in key:
                    cleanKey = key[0:key.index(",")]
                else:
                    cleanKey = key

                if len(inLineArgs) >= 1:
                    amount = int(inLineArgs[0])
                    if len(inLineArgs) >= 2:
                        waitTime = float(inLineArgs[1])
        
                for _ in range(amount):
                    kb.send(cleanKey)
                    sleep(waitTime)
                
                if self.logAll:
                    print(f"{repr(cleanKey)} sent {repr(amount)} times with {repr(waitTime)} seconds between each")
            
            if kb.is_pressed("end"):
                print("Program Ended")
                os._exit(1)
            
            self._checkPause()