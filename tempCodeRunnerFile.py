import tkinter as tk
from app.core.app_controller import SQLToolApp

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = SQLToolApp(root)
    
    try:
        icon = tk.PhotoImage(file="assets/logo.png")
        root.iconphoto(True, icon)
    except:
        pass
    
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
