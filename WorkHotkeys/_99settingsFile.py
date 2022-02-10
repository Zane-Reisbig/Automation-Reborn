import re

class SettingsFile:
    def __init__(self, filePath, seperator=":"):
        self.file = filePath     # Specifies the file being read/wrote to
        self.seperator = seperator     # Specifies the seperator used in between keys and values

    # With this you can have only one instance of the class open -
    # and still read and write to multiple files. 
    # Maybe you want two seperate files for some reason, maybe for -
    # whatever reason you don't want two of them with seperate variables - 
    # even though it would make more sense to do it that way.
    def setFile(self, filePath):
        self.file = filePath

    # Writes a new value to the text file
    # Will write a new instance of "valueId" regardless if -
    # the "valueId" is already in the file 
    def writeNewValue(self, valueId, newValue):
        currentFile = open(self.file, "a")
        currentFile.write("{0}{1}{2}\n".format(valueId, self.seperator, newValue))
        currentFile.close()
    
    # Writes a formatted string to a file
    # Does not add any seperators or new lines
    # You do it all baybee
    def writeFormattedValue(self, formattedValue):
        currentFile = open(self.file, "a")
        currentFile.write(formattedValue)
        currentFile.close()

    # Pretty straight forward what this does I think.
    def clearFile(self):
        currentFile = open(self.file, "w")
        currentFile.write("")
        currentFile.close()

    # This will over-write the "valueId" specified with the -
    # "newValue" specifed
    # When the returnValue param is True it will return the value that has just been changed
    # typecasted to the returnType specified.
    # Useful for changing variables that have already been set and need to be re-assigned

    # -- Example --
    # def facilitySwitch():
    #   global isFacility
    #   waitForRelease(switchBind)
    #   isFacility = settings.changeValue("isFacility", not isFacility, True, bool)
    # This example is inverting a boolean in a settings file, and re-assigning a variable in one line
    def changeValue(self, valueId, newValue, returnValue=False, returnType=str):
        valueId = str(valueId)
        newValue = str(newValue)
        
        fileValues = []
        iterable = 0
        currentFile = open(self.file, "r")

        # Append all the lines of the file to an array
        for line in currentFile.readlines():
            fileValues.append(line)
        
        currentFile.close()
        
        # Read thru that array and find the key specified and overrite the valueID -
        # - with the requested value
        for item in fileValues:
            if valueId in item:
                fileValues[iterable] = ("{0}{1}{2}".format(valueId, self.seperator, newValue + "\n"))
                break
            iterable += 1
        else:
            # Don't want to keep going unless you have the correct information
            raise Exception("ValueID not found")

        # Reopen the file for writing and write that array back to the file
        currentFile = open(self.file, "w")
        currentFile.writelines(fileValues)
        currentFile.close()
        
        # If a return value is needed, the input is sanatized and converted to the value
        if returnValue:
            return self.returnTyper(newValue.replace("\n", "").replace("\r", "").strip(), returnType)

    def returnTyper(self, value, typeOf):
        try:
            # Because of the Python bool typecasting you can't just bool(value), you have to do it manually
            if typeOf == bool:
                if value == "True":
                    return True
                return False

            else:
                # Otherwise the input is santized and the type conversion is done
                return typeOf(value.replace("\n", "").replace("\r", "").strip())
        except:
            # Raise an exception if the value you provided cannot be typecasted
            raise ValueError("Could not be converted to {}".format(type))


    # This will read the value of the specifed "valueId" -
    # optional "typeOf" that will return the value in the type that is requested
    # It's kinda helpful because you don't have to worry about python doing some - 
    # wonky stuff with the value.
    # If you specify the type to be returned and the value read cannot be interpreted - 
    # it will raise an error out so you don't use any wrong values
    # You cannot continue the program if the type conversion fails
    def readValue(self, valueId, typeOf=str):
        value = ""
        currentFile = open(self.file, "r")

        for line in currentFile.readlines():
            lineCheck = line[0:line.index(self.seperator)]
            if valueId == lineCheck:
                value = (line[line.index(self.seperator) + 1:len(line)]).strip()
                break

        if value != "":
            return self.returnTyper(value.replace("\n", "").replace("\r", "").strip(), typeOf)
        
        raise ValueError("valueId not found")
    
    def readMath(self, valueID):
        value = ""
        currentFile = open(self.file, "r")

        for line in currentFile.readlines():
            lineCheck = line[0:line.index(self.seperator)]
            if valueID == lineCheck:
                value = (line[line.index(self.seperator) + 1:len(line)]).strip()
                break
        value = value.split(" ")
        return(int(int(value[0]) * int(value[2])))

#
# Debug stuff
#
if __name__ == "__main__":
    settings = SettingsFile("_0settingsRep.txt")

    x = settings.readMath("totalClaims")

    print(x)