import re

def getItems(input, output=None):
    file = open(input,"r")
    fileLines = file.readlines()
    file.close()

    fileLines = "".join(fileLines).split("\n")
    fileLinesSanitized = []

    for i in fileLines:
        string = i.split("*")
        string = [item.strip().replace("~", "") for item in string if re.search("\s+", item) or item != ""]
        fileLinesSanitized.append(string)

    if output != None:
        with open(output, "w") as out:
            for i in fileLinesSanitized:
                out.write(str(i) + "\n")
    
    return fileLinesSanitized