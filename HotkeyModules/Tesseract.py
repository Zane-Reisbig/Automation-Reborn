import pytesseract, pyautogui, mouse, win32gui, win32ui, pyperclip, pywinauto, os, re
from PIL import ImageGrab
from win32api import GetSystemMetrics

#Confusing win32 commands
def grabText(activateWindow:False=True,
            regex:str="\d{12}",
            autoRetry=False,
            copyToClipboard=False,
            ) -> str|None:
    """
        Tesseract is used to grab text from the screen
        The text is returned as a string
        If the text is not found, the function will return None
        If the text is found, the function will return the text, if the regex passes the check
        If autoRetry is True, the function will retry the function until it finds a text that passes the regex
    """

    dc = win32gui.GetDC(0)
    dcObj = win32ui.CreateDCFromHandle(dc) #I think DC refers to the content that's actually /in/ the window
    facets_hwnd = win32gui.FindWindow(None, "Facets - ")
    monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1)) #Screen size for cursor math

    userName = os.getlogin()
    my_tesseract = f'C:/Users/{userName}/AppData/Local/Programs/Tesseract-OCR/tesseract'

    try:
        pytesseract.pytesseract.tesseract_cmd = my_tesseract #Put your own location here
    except(Exception):
        print(Exception("Cannot find Tesseract.exe"))


    while text == None and autoRetry == True: # if autoRetry is true, this will keep retrying until it finds a valid regex
        try:
            if activateWindow:
                facets = pywinauto.Application(backend="win32").connect(title_re="^Facets*", found_index=0) # The trys are there to prevent ugly errors

        except(Warning):
            print('There was a warning')
                

        before = pyautogui.position()           #This part moves the mouse back where it should be after changing the window,
        facets.top_window().set_focus()         #I've had trouble with that before
        mouse.move(x=before[0], y=before[1])
        facets.top_window().wait('visible')


        mouse.wait(button='left',target_types='down')       #Watch for next mouse down
        orig_mousex, orig_mousey = pyautogui.position()     #Save coords for rectangle

        box = (orig_mousex-2, orig_mousey+2, orig_mousex+1, orig_mousey-1) #The + and - are to make it a bit easier to slect?

        while mouse.is_pressed(button='left'):              #This loop goes until you release the button
            mousex, mousey = pyautogui.position()
            box = (orig_mousex, orig_mousey, mousex, mousey)
                
            dcObj.DrawFocusRect(box)                            #This is a win32gui thing, draws a focus box with dotted lines and stuff
            win32gui.InvalidateRect(facets_hwnd, monitor, True) # Refresh the entire monitor, clears the whole screen, especially the stuff inside the rectangle


        im = ImageGrab.grab(box)                                #Pillow grabs the most recent coords of the box you dragged
        text = pytesseract.image_to_string(im)  #pytesseract lets you only grab digits
        text = re.search(regex, text)

        if text is not None:
            text = text.group(0)
            if copyToClipboard: pyperclip.copy(text)
            return text
        elif autoRetry == False:
            print("Failed to find a valid regex")
            return None