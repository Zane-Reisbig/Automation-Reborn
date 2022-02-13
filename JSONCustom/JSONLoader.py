from io import TextIOWrapper
from enum import Enum
import json

# Handles basic JSON file loading
# This is kind of a pre-processor for JSON files
# Made because I don't like the built-in json module
# Handles support for multiple types not included with JSON such as
#   - Addition
#   - Subtraction
#   - Multiplication
#   - Division


# Included custom object types
class JSONTypes(Enum):
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"

# JSONManager class
# Used for logging
class ValueLogger:
    def __init__(self, value, specialOperations:str=None):
        self.value = value
        self.type = type(value)
        self.specialOperations = specialOperations
    def __str__(self) -> str:
        return (
            f"Value(value={self.value}, type={self.type}, specialOperations={self.specialOperations})"
        )

# Main Class for JSONLoader
# Point by point comments above the function delcarations
# Finer details on lines as needed
class JSON:
    """
        My Version of the JSON library to make it easier to use
        Manages multiple JSON files and allows switching between them on the fly
        Adds in a typing system as well
        When returning a value, it will return the value as the type specified by the type parameter
    """
    def __init__(self, fileName:TextIOWrapper) -> None:
        self.type = None # When set, all values returned will be of this type
        self.data = None # The JSON data
        self.fileName = self.setFile(fileName) # The file name

    # Sets the name of the JSON file
    # Loads the JSON data
    def setFile(self, fileName:TextIOWrapper) -> None:
        """
            Loads a JSON file into the JSON object
        """
        self.fileName = fileName
        with open(self.fileName) as json_file:
                self.data = json.load(json_file)
    
    # Gets the value of the key from the JSON data
    # Returns the value as the type specified by the type parameter
    # If the type is None, the value is returned as the type it is in the JSON data
    # Optionally logs information about the value to the console if logVar is True
    def get(self, value:list[str], returnType:JSONTypes=None, logVar:bool=False) -> object:
        """
            Gets a value from the JSON file
            If the value is a list, it will be treated as a path to the value
            returnType:JSONTypes -> The type to return the value as
            logVar:bool -> If True, will print information about the value being returned
        """        


        currValue = ""
        for (i, val) in enumerate(value):
            if i == 0:
                currValue = self.data[val] # Sets the current value to the first value - only used for the first value
            else:
                currValue = currValue[val] # Iterates through itself based on the values of the array

        specialOperations = None # Used to log the pre-process operations used to get the final value
        if returnType == None:
            returnValue = currValue
        else:
            values = self._getFirstAndSecond(currValue, returnType.value)
            if returnType == JSONTypes.ADDITION:
                returnValue = values[0] + values[1]
                specialOperations = "JSONTypes.ADDITION"
            elif returnType == JSONTypes.SUBTRACTION:
                returnValue = values[0] - values[1]            
                specialOperations = "JSONTypes.SUBTRACTION"
            elif returnType == JSONTypes.MULTIPLICATION:
                returnValue = values[0] * values[1]
                specialOperations = "JSONTypes.MULTIPLICATION"
            elif returnType == JSONTypes.DIVISION:
                returnValue = values[0] / values[1]
                specialOperations = "JSONTypes.DIVISION"
            else:
                raise Exception("Invalid return type\nIf you want the original value, leave returnType as None")
        
        if logVar:
            curVar = ValueLogger(returnValue, specialOperations)
            print(str(curVar))
        
        return returnValue

    # Only used for getting the first and second values when the custom JSON type is used
    def _getFirstAndSecond(self, string:str, splitAt:str)->tuple[float, float]:
        stringSplit = string.split(splitAt)
        return float(stringSplit[0]), float(stringSplit[1])

