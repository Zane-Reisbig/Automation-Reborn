import keyboard as kb

def waitForRelease(combination:str) -> None:
    """
        Waits for a key to be released
        The keyboard library has a builtin function for this but I cannot get it to work
    """
    keyArrs = combination.split("+")
    releasedCount = 0
    while True:
        for key in keyArrs:
            if kb.is_pressed(key):
                releasedCount = 0
                break
            else:
                releasedCount += 1
        if releasedCount == len(keyArrs):
            print("released")
            return