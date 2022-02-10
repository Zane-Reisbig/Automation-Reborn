import keyboard as kb

def waitForRelease(combination:str) -> None:
    """
        Waits for a key to be released
        Works great for waiting for a hotkey to be released
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
            return