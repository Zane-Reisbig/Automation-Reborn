import os
import pydirectinput as pdi
import keyboard as kb
import win32gui
import threading as t
import pywinauto
import winsound
from re import search
from time import sleep
from os import system

class ArgumentError(Exception):
    """Raised when passing incorrect arguments to a function"""
    pass

#
# Helper Functions Start
#

class Hotkey():
    def __init__(self, hotkey, callback, args=()):
        self.hotkey = hotkey
        self.callback = callback
        self.args = args
        self.useKwargs = True if type(args) == dict else False
        self.initalizeHotkey()

    def initalizeHotkey(self):
        kb.add_hotkey(self.hotkey, self.triggerCallback)

    def triggerCallback(self):
        waitForRelease(self.hotkey)
        if self.useKwargs:
            thread = t.Thread(target=self.callback, kwargs=(self.args), name=str(self.callback.__name__))
        else:
            thread = t.Thread(target=self.callback, args=(self.args), name=str(self.callback.__name__))
        thread.start()
        thread.join()

# Window Activation Start

# Shamelessly stolen from Stack Over Flow
# nonsense
def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def activateWindowBack(name):
    try:
        if(__name__ != "__main__"):
            top_windows = []
            win32gui.EnumWindows(windowEnumerationHandler, top_windows)
            for i in top_windows:
                if name in i[1].lower():
                    win32gui.ShowWindow(i[0],5)
                    win32gui.SetForegroundWindow(i[0])
                    break
            return True
    except:
        return False


# When passed a string name this function will activate that window 
# and prepare it to handle keystrokes
 
def activateWindow(name):
    x = activateWindowBack(name)
    sleep(0.03)

# Window Activation Stop

# Presses a specified key x number of times with some optional params
# Amount: the amount of times the key is pressed
# Offset: the amount of times the key is offset, a string, for console inputs that need to be converted
#         I've used this once, and I need to remove it, but I haven't yet
# The "waitTime" param specifies the amount of time to wait after the key commands have been pressed

def pressKey(key, amount = 1, delay = 1.3, waitTime=0):

    for _ in range(0, int(amount)):
        if(kb.is_pressed("end")):
            rescue()
        
        pauseCheck()

        kb.send(key)
        sleep(delay)

    sleep(waitTime)


# Waits for the hotkey bind keys to be released and then releases itself
# The "hotkeybind" param is the bind on the actual hotkey definition
# Put this as the first thing call in every "Working Function" you make 

def waitForRelease(hotkeyBind):
    keyArr = []
    
    if hotkeyBind.count("+") == 0:
        keyArr.append(hotkeyBind)

    elif hotkeyBind.count("+") == 1:
        keyArr.append(hotkeyBind[0:hotkeyBind.index("+")])
        keyArr.append(hotkeyBind[hotkeyBind.index("+") + 1:len(hotkeyBind)])

    elif hotkeyBind.count("+") == 2:
        keyArr.append(hotkeyBind[0:hotkeyBind.index("+")])
        keyArr.append(hotkeyBind[hotkeyBind.index("+") + 1: hotkeyBind.index("+", hotkeyBind.index("+") + 1)])
        keyArr.append(hotkeyBind[hotkeyBind.index("+", hotkeyBind.index("+") + 1) + 1: len(hotkeyBind)])

    if hotkeyBind.count("+") == 0:
        while kb.is_pressed(keyArr[0]):
            sleep(0.3)
            continue
    elif hotkeyBind.count("+") == 1:
        while kb.is_pressed(keyArr[0]) or kb.is_pressed(keyArr[1]):
            sleep(0.3)
            continue
    elif hotkeyBind.count("+") == 2:
        while kb.is_pressed(keyArr[0]) or kb.is_pressed(keyArr[1]) or kb.is_pressed(keyArr[2]):
            sleep(0.3)
            continue
        
    return


# Pauses the program where it stands, unpauses when pause is pressed again

def pauseCheck():
    if(kb.is_pressed("pause")):
        print("System Paused")
        waitForRelease("pause")
        while True:
            if kb.is_pressed("pause"):
                print("System Unpaused")
                waitForRelease("pause")
                break
            elif kb.is_pressed("end"):
                rescue()
            continue


# Presses a list of keys based on an array.
# Does the same as key list test, with keywords.
# The "objectArr" param is the list of key command to be interpreted
# The "waitTime" command specifies the amount of time to wait after the key commands have been pressed
# With the -1 write you can pass a string into it and it will parse out the new lines with the \n character
# Mostly for use with strings from text files that have \n in them.

def pressKeyList(objectArr, waitTime=0, allDelay=None):
    for i in objectArr:
        case = i.split(",")

        if case[0] == "-1":
            newLineSplit = case[1].split("\\n")
            for i in newLineSplit:
                kb.write(i)
                if len(newLineSplit) > 1: kb.write("\n")
                
                if allDelay != None:
                    sleep(allDelay)
                elif len(case) == 3:
                    sleep(case[2])
            
            continue
        
        if case[0] == "-2":
            sleep(float(case[1]))
            continue

        
        if case[0] == "-3":
            commands = {
                "assertTopWindow" : assertTopWindow,
                "catch" : catch,
                "activateWindow" : activateWindow,
                "waitForAdj" : waitForAdj
            }

            if len(case) == 4:
                commands[case[1]](case[2], case[3])
            elif len(case) == 3:
                commands[case[1]](case[2])
            elif len(case) == 2:
                commands[case[1]]
            else:
                raise ArgumentError("Only Two Arguments can be passed when calling from pressKeyList")
            
            if allDelay != None:
                sleep(allDelay)

            continue
            

        case = i.replace(" ", "").split(",")

        key = case[0]
        delay = 0.06
        amount = 1

        if len(case) >= 2:
            if '=' in case[1]:
                delay = float(case[1][case[1].index("=") + 1:-1])
            else:
                amount = int(case[1])
        
        if len(case) == 3:
            delay = float(case[2])
        
        for _ in range(0, amount):
            if(kb.is_pressed("end")):
                rescue()
            
            pauseCheck()
                
            kb.send(key)
            if allDelay != None:
                sleep(allDelay)
            else:
                sleep(delay)
        
    sleep(waitTime)
    return


# Will catch a key based on a set time and return true or false based on the outcome
# The "time" param specifies the amount of time the program will wait for the key to be pressed
# The "hard" param will hard stop the program until the key is pressed

def catch(key, hard = False, time = 1.5,  exitKey = "f13", exitKey2 = "f14"):
        timePassed = 0

        if hard:
            while(True):
                if(kb.is_pressed(key)):
                    print("{} pressed".format(key.capitalize()))
                    waitForRelease(key)
                    return key

                if(kb.is_pressed(exitKey)):
                    print("{} pressed".format(exitKey.capitalize()))
                    waitForRelease(exitKey)
                    return exitKey

                if(kb.is_pressed(exitKey2)):
                    print("{} pressed".format(exitKey2.capitalize()))
                    waitForRelease(exitKey2)
                    return exitKey2

                if(kb.is_pressed("end")):
                    rescue()

                pauseCheck()
        else:
            while True:
                if(timePassed >= time):
                    return ""

                if(kb.is_pressed(key)):
                    print("{} pressed".format(key.capitalize()))
                    waitForRelease(key)
                    return key

                if(kb.is_pressed(exitKey)):
                    print("{} pressed".format(exitKey.capitalize()))
                    waitForRelease(exitKey)
                    return exitKey

                if(kb.is_pressed(exitKey2)):
                    print("{} pressed".format(exitKey2.capitalize()))
                    waitForRelease(exitKey2)
                    return exitKey2
                    
                
                if(kb.is_pressed("end")):
                    rescue()
                

                timePassed += 0.01
                sleep(0.01)                    
                

# This will "alt-tab" to an open excel document and highlight the current cell based on the color param
# The "color" param will take a color out of yellow, orange, or red and highlight as such
# the "note" param will take in a string note and make a note on the cell with the value
# Very situational, not always useful, I use it so I leave it in here
# I've added a custom color with modifiers you can use
# Just put the boolean true and adjust the modifers as you please

def highlightExcel(color="", note="", customColor = False, modUp=0, modLeft=0, modRight=0):
        sleep(0.5)

        activateWindow("excel")
        sleep(0.8)
        activateWindow("excel")
        sleep(0.8)
        assertTopWindow("Excel", False, False)

        pdi.press("alt")
        pdi.press('h')
        pdi.press('h')

        if not customColor:    
            for _ in range(3):
                kb.send("up")

            if color == "yellow":
                for _ in range(2):
                    kb.send("left")
                
            elif color == "orange":
                for _ in range(3):
                    kb.send("left")
                
            elif color == "red":
                for _ in range(4):
                    kb.send("left")
        else:
            for _ in range(modUp):
                kb.send("up")
            for _ in range(modRight):
                kb.send("right")
            for _ in range(modLeft):
                kb.send("left")
                       
                    
        pdi.press("enter")
        pdi.press("esc")

        if(note != ""):
            pressKeyList([
                "alt",
                "n,1,0.8",
                "c,1,0.8",
                "2,1,0.8",
                "-1,{}".format(note),
                "ctrl+enter",
                "esc,2"
            ])

def assertTopWindow(windowName, remote = True, exact = True):
    countUp = 0
    toFind = windowName + " - \\\\Remote" if remote else windowName
    if exact:
        while win32gui.GetWindowText(win32gui.GetForegroundWindow()) != toFind:
            if kb.is_pressed("end"):
                rescue()
            if kb.is_pressed("delete"):
                print("Canceled")
                return
            
            pauseCheck()
            
            if countUp % 5 == 0 and countUp >= 10: 
                system("cls")
                print("Current:", win32gui.GetWindowText(win32gui.GetForegroundWindow()))
                print("Desired: {}".format(windowName))

            sleep(0.3)
            countUp += 1
    else:
         while not search(windowName, win32gui.GetWindowText(win32gui.GetForegroundWindow())):
            if kb.is_pressed("end"):
                rescue()
            if kb.is_pressed("delete"):
                print("Canceled")
                return
            
            pauseCheck()
            
            if countUp % 5 == 0 and countUp >= 10: 
                system("cls")
                print("Current:", win32gui.GetWindowText(win32gui.GetForegroundWindow()))
                print("Desired: {}".format(windowName))

            sleep(0.3)
            countUp += 1       
    
    print("Window Confirmed...")
    sleep(0.3)

# This will wait for a claim to adjudicate and block the thread from progressing when it is running
#
# Params:
# initalCursorValue - needs to be a win32gui.GetCursorInfo() when being called
#                     this might not need to be passed, however for maximum reliabilty
#                     it should be passed in.
#
# beep - will beep when the claim is done adjudicating, so you look back at the screen

def waitForAdj(initalCursorValue=None, message=True):
    cursors = []
    if initalCursorValue != None: cursors.append(initalCursorValue[1])

    doubleCheck = 0
    increment = 0

    while True:
        var = win32gui.GetCursorInfo()
        currentWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        cursors.append(var[1])

        if(kb.is_pressed("end")): rescue()
        pauseCheck()

        if cursors[increment - 1] == var[1] and "facets" in currentWindow.lower() and increment > 1:
            doubleCheck += 1
            if doubleCheck == 1:
                if message:
                    print("Done Adjudicating...")
                break
        if increment < 10: activateWindow("facets")

        increment += 1
        sleep(0.4) 

# When the end key is pressed this command will take over and stop all keypresses
# No way to continue the program when this is activated, you have to end the program

def rescue():
    os._exit(1)

def activateEDI():
    app = pywinauto.Application(backend="win32").connect(title_re="^Viewer")
    app.top_window().set_focus()
    app.top_window().wait("visible")

#
#   Debug Stuff
#
if __name__ == "__main__":
    winsound.Beep(2500, 500) 
