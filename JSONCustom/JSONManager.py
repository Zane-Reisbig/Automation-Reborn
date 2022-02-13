from .JSONLoader import JSON, JSONTypes
import os

# The abstraction for the JSONLoader module
# This is used to load and keep track of JSON files
# Handles support for multiple files and file switching

# Main Class for JSONLoader
# Point by point comments above the function delcarations
# Finer details on lines as needed
class JSONManager:
    """
        Manages JSON files and allows switching between them on the fly
        Adds in a typing system as well
        When returning a value, it will return the value as the type specified by the type parameter
    """
    JSONFiles = {}

    def __init__(self, fileName: str = None) -> None: 
        self.flags = {"logVar": False, "returnType": None} # Flags for the JSONManager

        self.settings = None
        self.currentFile = None

        if fileName != None: # If a file is specified, load it
            self.loadFile(fileName)

    # Loads a JSON file to the JSONFiles dictionary
    # If the file is already loaded, it will not be loaded again
    # The fileName is the key for the JSONFiles dictionary
    # The key is determented by the fileName without the extension
    def loadFile(self, fileName: str) -> None:
        """
            Loads a JSON file to the JSONFiles dictionary
            The key for this file is the base name of the file with no extension
            fileName: The file name to load
        """
        baseFileName = os.path.basename(fileName)[
            0 : os.path.basename(fileName).index(".")
        ]
        self.JSONFiles[baseFileName] = JSON(fileName)

    # Grabs a value from the currently loaded JSON file
    # Returns the value as the type specified by the type parameter
    def getFromCurrent(self, value: list[str], typeOf:object=None) -> object:
        """
            Grabs a value from the currently loaded JSON file
            value: The value to grab, uses an array instead of the commonly used dictionary syntax
            typeOf: The type to return the value as
        """
        typeOf = typeOf if typeOf != None else self.flags["returnType"]

        # The actual call to the JSONLoader module
        return self.currentFile.get(
            value,
            typeOf,
            self.flags["logVar"]
        )

    # Sets the current file to the file specified by the fileName/alias
    def SETCURRENTFILE(self, fileName: str) -> None:
        """
            Sets the current file to the file specified by the fileName/alias
            fileName: The file name to set as the current file uses the base name of the file without the extension
        """
        self.currentFile = self.JSONFiles[fileName]

    # Sets the global flags for the JSONManager
    # Raises an error if the flag is not recognized
    def SETFLAGS(self, flag: str, value: bool) -> None:
        """
            Sets the debug flags for the JSONManager
            Flags:
                logVar: If True, will print information about the value being returned
                returnType: The type to return the value as
        """
        found = False
        for key in self.flags:
            if key == flag:
                self.flags[key] = value
                found = True
                break

        if not found:
            raise Exception("Invalid flag")

        self.flags[flag] = value
