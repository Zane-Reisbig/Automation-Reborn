import keyboard as kb
import time

def hardCatch(keys:list[str,str,str]) -> str:
    """
        Waits eternally for a listed key to be pressed
        Returns the key that was pressed
        The key returned can be used to determine the outcome of the function
        keys: list of keys to wait for
    """
    while True:
        for key in keys:
            if kb.is_pressed(key):
                while kb.is_pressed(key):
                    time.sleep(0.1)
                return key



def softCatch(keys:list[str,str,str], defaultKey:str, timeOut:float) -> str:
    """
        Waits for a key to be pressed for a certain amount of time
        Returns the default key if no key is pressed
        The key returned can be used to determine the outcome of the function
        keys: list of keys to wait for
        defaultKey: key to return if no key is pressed
        timeOut: time to wait for a key to be pressed in seconds
    """
    start = time.perf_counter()
    stop = time.perf_counter()
    while (stop - start) < timeOut:
        stop = time.perf_counter()
        for key in keys:
            if kb.is_pressed(key):
                return key
    
    return defaultKey