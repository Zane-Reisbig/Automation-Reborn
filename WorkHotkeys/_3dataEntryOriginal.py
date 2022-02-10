from os import system
from time import sleep
from _99universalFunctions import *
from _99helperFunctions import *

#HI Diagnosis Code
#CLM*UC Freq
#NM1 MI Member ID
#PHE Subscriber ID
#CLM*UC 3rd Item
#DTP Date Of Claim
#SVD Proc
#SV1 DX Code ?last one
#SV1 Quantity ?last one
#SV1 Amount Paied 2nd

dataEntryLookMedical = ["HI", "CLM", "NM1", "PHE", "DTP", "SVD", "SV1", "REF", "CL1"]
scrubbedData = []

def scrubber():
    waitForRelease("alt+2")
    global scrubbedData

    x = open("_3items.txt", "r").read()
    x = x.strip()
    x = x.replace("*", " ")
    y = x.split("\n")

    for i in y:
        scrubbedData.append(" ".join(i.replace("~", "").split()))


def getFromScrubbedMedical():
    foundItems = []
    delimiter = ":"

    for i in scrubbedData:
        for ii in dataEntryLookMedical:
            if ii in i.split(" "):
                foundItems.append(i)
    
    # [print(i) for i in foundItems]

    dxCodes = []
    dxLine = ""
    for i in foundItems:
        if i[0:2] == "HI":
            dxLine = i.split(" ")
    
    for i in dxLine:
        if i != "HI":
            dxCodes.append(i[4:])

    ###

    provID = ""
    for i in foundItems:
        currentLine = i.split(" ")
        if currentLine[0] == "NM1" and currentLine[1] == "85":
            provID = currentLine[-1]

    ###
    
    freq = ""
    for i in foundItems:
        if i[0:3] == "CLM":
            freq = i
    
    try: 
        freq = freq[freq.index(delimiter, freq.index(delimiter)) + 3]
    except:
        print("Check Delimter")

    ###

    ids = []
    for i in foundItems:
        if i.split(" ")[1] == "IL":
            ids.append(i.split(" ")[-1])

    ###

    total = ""
    for i in foundItems:
        if i[0:3] == "CLM":
            total = i.split(" ")[2]

    ###

    datesStart = []
    datesEnd = []
    for i in foundItems:
        currentLine = i.split(" ")
        if currentLine[0] == "DTP" and currentLine[1] == "472":
            x = currentLine[-1].split("-")[0]
            datesStart.append((x[4:6] + "/" + x[6:8] + "/" + x[0:4]))
            try:
                y = currentLine[-1].split("-")[1]
                datesEnd.append((y[4:6] + "/" + y[6:8] + "/" + y[0:4]))
            except:
                datesEnd.append((x[4:6] + "/" + x[6:8] + "/" + x[0:4]))

    ###
    
    pOS = ""
    for i in foundItems:
        currentLine = i.split(" ")
        if currentLine[0] == "CLM":
            pOS = currentLine[3][0:2]

    ###

    procCodes = []
    for i in foundItems:
        currentLine = i.split(" ")
        if currentLine[0] == "SV1":
            procCodes.append(currentLine[1].replace(delimiter, "").replace("HC", ""))

    ###

    units = []
    for i in foundItems:
        currentLine = i.split(" ")
        if currentLine[0] == "SV1" and currentLine[3] == "UN":
            units.append(currentLine[4])

    ###

    dX = []
    for i in foundItems:
        currentLine = i.split(" ")
        if currentLine[0] == "SV1":
            dX.append(dxCodes[int(currentLine[-1][0]) - 1])

    ###

    amounts = []
    for i in foundItems:
        currentLine = i.split(" ")
        if currentLine[0] == "SV1":
            amounts.append(currentLine[2])
    

    ###

    clmNumber = ""
    for i in foundItems:
        currentLine = i.split(" ")
        if currentLine[0] == "REF" and currentLine[1] == "DD":
            clmNumber = currentLine[2]



    print("Sub and Member ID's:", ids)
    print("Provider ID:", provID)
    print("Recieved Date From SalesForce")
    print("Dx Codes:", dxCodes)
    print("Patient Account Number:", ids)
    print("Frequency:", freq)
    print("Claim Dollar Total:", total)
    print("Line Item Date Start:", datesStart)
    print("Line Item Date End:", datesEnd)
    print("Place Of Service:", pOS)
    print("Procedure Codes Per Line:", procCodes)
    print("Diagnosis Codes Per Line:", dX)
    print("Amounts Per Line:", amounts)
    print("Units Per Line:", units)
    print("Inq Number on SalesForce")
    print("Claim Number Original:", clmNumber)

    inputInfo(ids, provID, dxCodes, freq, total, datesStart, datesEnd, pOS, procCodes, dX, amounts, clmNumber, units)

def inputInfo(ids, provID, dxCodes, freq, total, datesStart, datesEnd, pOS, procCodes, dX, amounts, clmNumber, units):
    pressKeyList([
        "tab,1",
        "-1,{}".format(ids[0]), #Might have to change
        "tab,3",
        "-1,{}".format(provID),
    ])

    pressKey("tab")
    print("Prov ID Catch")
    key = catch("ctrl", exitKey="alt" ,hard=True)
    if key == "alt":
        waitForRelease("alt")
        pressKey("esc")
        pressKey("enter")
    
    pressKey("tab", 2)
        

    for i in range(0, 11):
        if len(dxCodes) > i:
            pressKeyList([
                "-1,{}".format(dxCodes[i]),
                "tab,1"
            ])
        else:
            pressKey("tab", delay=0.0)
    
    pressKeyList([
        "tab,5",
        "-1,{}".format(ids[0]),
        "tab,5",
        "space",
        "-1,{}".format(freq),
        "enter",
        "ctrl+down",
        "tab,1",
        "f2",
        "-1,{}".format(total),
        "tab,2"
    ])

    for i in range(0, len(datesEnd)):
        pressKeyList([
            "-1,{}".format(datesStart[i]),
            "tab,1",
            "-1,{}".format(datesEnd[i]),
            "tab",
            "-1,{}".format(pOS),
            "tab,2",
            "-1,{}".format(procCodes[i][0:5]),
            "tab,1",
            "-1,{}".format(dX[i]),
            "tab,1",
            "-1,{}".format(amounts[i]),
            "tab",
            "-1,{}".format(units[i]),
            "enter,{}".format("0" if i == (len(datesEnd) - 1) else "1")
        ])

    pressKeyList([
        "ctrl+down",
        "alt+e",
        "a",
        "-1,ORIGINAL CLAIM: {}".format(clmNumber),
        "tab",
        "-1,Per Inquiry: {}".format("Inquiry # Goes Here"),
        "tab",
        "enter"
    ])


def parseLineEDI(check, returnIndex, split = False, splitIndex = 1, delim = ":"):
    foundItems = []

    for i in scrubbedData:
        for ii in dataEntryLookMedical:
            if ii in i.split(" "):
                foundItems.append(i)

    returnLines = []
    splitLines = []
    for i in foundItems:
        currentLine = i.split(" ")

        if len(check) == 6:
            if currentLine[check[0]] == check[1] and currentLine[check[2]] == check[3] and  currentLine[check[4]] == check[5]:
                returnLines.append(currentLine[returnIndex])
        elif len(check) == 4:
            if currentLine[check[0]] == check[1] and currentLine[check[2]] == check[3]:
                returnLines.append(currentLine[returnIndex])
        else:
            if currentLine[check[0]] == check[1]:
                returnLines.append(currentLine[returnIndex])
    
    if split:
        for i in returnLines:
            splitLines.append(i.split(delim)[splitIndex])


    return returnLines if not split else splitLines
            
                


# system("cls")
# system("cls")
# system("cls")

scrubber()

x = parseLineEDI([0, "NM1", 1, "IL"], -1)
print(x)
print(parseLineEDI([0, "NM1", 1, "IL"], -1)[0][-2:])
print(parseLineEDI([0, "PHE"], 3)[0])
print("Date Got From The One Thing TM")
print(parseLineEDI([0, "HI"], 1, True)[:-1])
print("".join(parseLineEDI([0, "CLM"], 3, True, 0) + parseLineEDI([0, "CLM"], 3, True, 2)))
print("".join(parseLineEDI([0, "CLM"], 3, True, 2)))
dateStart = "".join(parseLineEDI([0, "DTP", 1, "434"], 3, True, 0, "-"))
dateEnd = "".join(parseLineEDI([0, "DTP", 1, "434"], 3, True, 1, "-"))
dateStart = dateStart[4:6] + "/" + dateStart[6:8] + "/" + dateStart[0:4]
dateEnd = dateEnd[4:6] + "/" + dateEnd[6:8] + "/" + dateEnd[0:4]
print(dateStart)
print(dateEnd)
print(dateStart)
print("find hours")
print("".join(parseLineEDI([0, "CL1"], 1)))
print("".join(parseLineEDI([0, "CL1"], 2)))
print("".join(parseLineEDI([0, "CL1"], 3)))
print("Ask About Procedure Codes")
print(x[0])
print("Ask About OTher Providers")
print("".join(parseLineEDI([0, "CLM"], 2)))
print("Ask about VALUE CODITION OCCURANCE")

# print("loaded")
# kb.wait("f1")