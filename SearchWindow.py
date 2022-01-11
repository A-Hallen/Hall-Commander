from tkinter import Toplevel, Entry, BOTH


class SearchWindow:
    def __init__(self, root):
        self.top = Toplevel (root, bg="black")
        self.top.attributes ("-alpha", 0.5)
        self.top.wait_visibility ()
        w = root.winfo_width ()
        h = root.winfo_height ()
        # self.top.overrideredirect(True)
        self.top.geometry (str (w) + "x" + str (h))

        # The edit
        self.entry = Entry (self.top, bg="black", fg="white")
        self.entry.pack (fill=BOTH, padx=20, pady=20)
        self.entry.focus ()
