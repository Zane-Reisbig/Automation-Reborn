from asyncore import loop
import keyboard as kb
import time

def hardCatch(keys:list[str,str,str]) -> str:
    """
        Waits eternally for a listed key to be pressed
        Returns the key that was pressed
        The key returned can be used to determine the outcome of the function
    """
    while True:
        for key in keys:
            if kb.is_pressed(key):
                return key



def softCatch(keys:list[str,str,str], defaultKey:str, timeOut:float) -> str:
    """
        Waits for a key to be pressed for a certain amount of time
        Returns the default key if no key is pressed
        The key returned can be used to determine the outcome of the function
    """
    start = time.perf_counter()
    stop = time.perf_counter()
    while (stop - start) < timeOut:
        stop = time.perf_counter()
        for key in keys:
            if kb.is_pressed(key):
                return key
    
    return defaultKey