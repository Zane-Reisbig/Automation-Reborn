import pywinauto

app = pywinauto.Application(backend="win32").connect(title_re="^Viewer")
app.top_window().set_focus()
app.top_window().wait("visible")
