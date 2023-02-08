import keyboard as kb
import types
import os
from time import sleep


class KeySender:
    """
        This function is used to type and send keystrokes to the computer
        See example in test.py for example usage
        usedModules:dict[str, tuple[function, tuple]] -> Callbacks to be able to be called inline when sending keys
            - When modules are passed, they can have default args and kwargs
            - If a module is passed without any args, the args will be gotten from the inline args, see the function description for more info on how the inline system works

        debug:bool -> When True will read in the passed dictionary and set the debugs

        debugCommands:dict[str, any] -> Dictionary of commands to be used when debugging
            - allDelay:int -> Every action will have this amount of delay
            - logAll:bool -> Every action will be logged to the console
    """

    def __init__(self,
                 inlineCallables: dict[str,
                                       tuple[types.FunctionType, tuple | dict]] = {},
                 debug: bool = False,
                 debugCommands: dict[str, str | int | bool] = {},
                 recursionLimit: int = 1,
                 exitKey="end") -> None:

        self.allDelay = None
        self.logAll = False
        self.usedModules = inlineCallables
        self.debug = debug
        self.debugCommands = debugCommands
        self.recursionLevel = 0
        self.recursionLimit = recursionLimit
        self.exitKey = exitKey
        # Current Debugs:
        # Must be passed as a dictionary with the following keys:
        # allDelay:int -> Every action will have this amount of delay
        # logAll:bool -> Every action will be logged to the console

        self.snippets = {

        }

        self.reservedPrefixes = [
            "write",
            "wait",
            "print",
        ]

        self.reservedDebugs = {
            "allDelay",
            "logAll"
        }
        # Functions that can be called inline without importing them

    def _setDebugs(self):
        if len(self.debugCommands) == 0:
            raise Exception("No debug commands were given.")

        for key in self.debugCommands:
            if key not in self.reservedDebugs:
                raise Exception(f"{key} is not a valid debug command.")
            else:
                if key == "allDelay":
                    self.allDelay = self.debugCommands[key]
                elif key == "logAll":
                    self.logAll = self.debugCommands[key]

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
                sleep(0.3)

    def _convert(self, value: str, conversion: str) -> str:
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
        elif conversion == "float":
            return float(value)
        else:
            return value

    def addSnippet(self, alias: str, snippet: list[str]) -> None:
        """
            Adds a snippet to be able to be called inline
            Snippets are called inline using the "%" prefix
            Ex: %snippetName
            name:str -> The name of the snippet
            snippet:list[str] -> A list of strings that will be parsed
            The snippet will be parsed just as if it were sent using the sendKeys function
            There are no arguments that can be passed
            You are able to call a snippet in a snippet as well.
            This function is recursive, so beware about calling the same snippet within a snippet
        """
        self.snippets.update({alias: snippet})

    def sendKeys(self, keyList: list[str]) -> None:
        """
            Interprets the passed list of keys and sends them to the computer
            keyList: list of keys to send
            $ is the prefix for an inline command
            default commands are:
                - write:str -> Writes the passed string to the console
                - wait:int -> Waits for the passed amount of seconds, args are converted to float automatically
                - print:str -> Prints the passed string to the console

            Passed modules can be passed args by just adding a comma after the command is called, kwargs are not supported
            example: $write,"Hello World"

            Args can be passed a type with a colon after the command and the type of the arg
            example: $print,5:int
            Args will be defaulted to str if no type is given

        """
        if self.debug:
            self._setDebugs()

        for key in keyList:
            prefix = None
            handled = False

            if key.startswith("$"):
                prefix = self._getPrefix(key)
            elif key.startswith("%"):
                if self.recursionLevel < self.recursionLimit:
                    prefix = key[1:]
                    self.recursionLevel += 1
                    self.sendKeys(self.snippets[prefix])
                    handled = True
                    self.recursionLevel -= 1
                    continue
                else:
                    raise Exception(
                        "Recursion level exceeded, program terminated.")

            if prefix != None:

                if prefix not in self.reservedPrefixes:
                    function = self.usedModules[prefix][0]

                    if "," in key:
                        args = (key.split(",")[1:])
                        for i in args:
                            if ":" in i:
                                selectedElement = args.index(i)
                                conversionValue = i[i.index(":")+1:]
                                args[selectedElement] = self._convert(
                                    args[selectedElement], conversionValue)
                        args = tuple(args)

                    else:
                        args = self.usedModules[prefix][1]

                    returnVal = None
                    if type(args) == tuple:
                        returnVal = function(*args)
                    elif type(args) == dict:
                        returnVal = function(**args)

                    if returnVal == False:
                        raise Exception(
                            f"Function {function.__name__} returned False. Operation Cancelled.")

                    handled = True
                    if self.logAll:
                        print(f"{repr(prefix)} called using {repr(args)}")

                elif prefix in self.snippets:
                    handled = True
                    self.sendKeys(self.snippets[prefix])
                    if self.logAll:
                        print(f"{repr(prefix)} called from snippet")

            if not handled:
                if prefix == "write":
                    kb.write(key[key.index(",")+1:])
                    handled = True
                    if self.logAll:
                        print(f"{repr(key)} written")

            if not handled:
                if prefix == "wait":
                    handled = True
                    args = float(key[key.index(",")+1:])
                    if self.logAll:
                        print(f"Waiting for {repr(args)} seconds")

                    sleep(args)

            if not handled:
                if prefix == "print":
                    handled = True
                    args = key[key.index(",")+1:]
                    print(args)
                    if self.logAll:
                        print(f"{repr(args)} printed")

            if not handled:
                handled = True
                inLineArgs = key.split(",")[1:]
                amount = 1
                waitTime = self.allDelay if self.allDelay != None else 0.3
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
                    print(
                        f"{repr(cleanKey)} sent {repr(amount)} times with {repr(waitTime)} seconds between each")

            if kb.is_pressed(self.exitKey):
                print("Program Ended")
                os._exit(1)

            if not handled:
                print(f"{repr(cleanKey)} not found")
                raise ValueError

            self._checkPause()
