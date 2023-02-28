import tkinter as tk
from view.viewmanager import ViewManager

if __name__ == '__main__':
    root=tk.Tk()
    view=ViewManager(root)

    root.mainloop()
