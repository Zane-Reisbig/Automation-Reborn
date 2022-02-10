import pywinauto
import typing

def activateWindow(windowName:typing.Pattern|str):
    """
        Brings the window to the front and sets the focus
    """
    app = pywinauto.Application().connect(title_re=f"{windowName}")
    app.top_window().set_focus()
    app.top_window().wait('visible')
