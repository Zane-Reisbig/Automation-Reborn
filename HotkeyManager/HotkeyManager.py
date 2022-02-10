import keyboard
from HotkeyManager.Hotkey import Hotkey


class HotkeyManager:
    """
        Controls the state and behavior of the hotkey modules passed
        Allows on the fly switching for hotkeys modules
    """

    keyMaps = {}
    keyMapBindings = {}
    persistantHotkeys = []

    def __init__(self, cycleBindingsMaster: str) -> None:
        self.currentMapping = None
        self.currentMappingAlias = None
        self.cycleBindingsMaster = cycleBindingsMaster
        self.isFinalized = False

    def ADDMAPPING(self, alias: str, reference: dict[str:Hotkey]) -> None:
        for i in reference:
            if type(reference[i]) != Hotkey:
                raise TypeError("reference must be a Hotkey object")

        referenceHotkeys = []
        for key,i in enumerate(reference.items()):
            referenceHotkeys.append([f"{i[1].getHotkey()}", key])
        
        self.keyMapBindings.update({alias: referenceHotkeys})
        self.keyMaps.update({alias: reference})

    def LISTMAPPINGS(self, alias=None) -> None:
        if alias == None:
            for i in self.keyMaps.items():
                for ii in i:
                    if type(ii) == str:
                        print("Alias:", ii)
                    if type(ii) == dict:
                        for iii in ii.items():
                            print(iii[1].getUnion())
        else:
            for i in self.keyMaps[alias].items():
                print(i[1].getUnion())

    def SETMAPPING(self, alias: str, suppressError=False) -> None:
        if not self.isFinalized:
            raise ValueError("HotkeyManager not finalized\nCall FINALIZE()")

        if alias in self.keyMaps:
            self.currentMapping = self.keyMaps[alias]
            self.currentMappingAlias = alias
        else:
            if not suppressError:
                print("Alias not found")
            else:
                raise KeyError("Alias not found")

        self.LISTMAPPINGS(alias)
        self.__registerHotKeys()

    def ADDPERSISTANT(self, reference: Hotkey) -> None:
        if type(reference) != Hotkey:
            raise TypeError("reference must be a Hotkey object")
        
        self.persistantHotkeys.append(reference)

    def FINALIZE(self) -> None:
        self.isFinalized = True

        persistantHotkeysBinds = []
        for i in self.persistantHotkeys:
            persistantHotkeysBinds.append([i.getHotkey(), i.getCallbackName()])

        for i in self.keyMapBindings.items():
            for ii in i[1]:
                for iii in i[1]:
                    if ii[1] != iii[1]:
                        if ii[0] == iii[0]:
                            hotKeyOffending = ii[0]
                            position1 = ii[1] + 1
                            position2 = iii[1] + 1
                            raise Exception(f"Hotkey conflict\n{hotKeyOffending} is bound to both items at positions {position1} and {position2} in mapping: {i[0]}")
                        if ii[0] == self.cycleBindingsMaster:
                            hotKeyOffending = ii[0]
                            position = ii[1] + 1
                            raise Exception(f"Hotkey conflict\n{hotKeyOffending} is bound to item at position {position} in mapping: {i[0]} and Master Hotkey")
                        for item in persistantHotkeysBinds:
                            for key in item:
                                if key == ii[0]:
                                    hotKeyOffending = ii[0]
                                    position = ii[1] + 1
                                    raise Exception(f"Hotkey conflict\n{hotKeyOffending} is bound to item at position {position} in mapping: {i[0]} and persistant hotkey: {item[1]}")
                                if key == self.cycleBindingsMaster:
                                    hotKeyOffending = self.cycleBindingsMaster
                                    raise Exception(f"Hotkey conflict\n{hotKeyOffending} is bound to persistant hotkey: {item[1]} and Master Hotkey")

        print("HotkeyManager finalized")

    def cycleMappings(self) -> None:
        if not self.isFinalized:
            raise ValueError("HotkeyManager not finalized\nCall FINALIZE()")

        choice = ""
        while True:
            if choice.lower() in ["exit", "e", "-1"]:
                break
            elif choice in self.keyMaps:
                self.SETMAPPING(choice)
                break
            else:
                print("Invalid choice")

            print("\nCurrent mapping:", self.currentMappingAlias)
            print("\nAvailable mappings:")
            for i in self.keyMaps:
                print(i)

            choice = input("\nEnter alias to set mapping, or 'exit' to exit: ")

    def __registerHotKeys(self) -> None:
        keyboard.unhook_all()

        for i in self.currentMapping.items():
            keyboard.add_hotkey(
                i[1].getHotkey(),
                i[1].getCallback(),i[1].getArgs(),
            )
        
        for i in self.persistantHotkeys:
            keyboard.add_hotkey(
                i.getHotkey(),
                i.getCallback(),i.getArgs(),
            )
        
        keyboard.add_hotkey(self.cycleBindingsMaster, self.cycleMappings)

        print("Hotkeys registered\n")
