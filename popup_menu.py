from tkinter import Toplevel, Scrollbar, RIGHT, BOTH, Frame, Label
from tkinter.ttk import Style, Treeview


class PopUpMenu:
    def __init__(self, parent, position="center", bd=2, bordercolor="#161616"):
        self.top = Toplevel(parent, bg="black")
        self.bd = bd
        self.bordercolor = bordercolor
        self.top.attributes("-alpha", 0.5)
        self.top.geometry("500x500")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.title("Menu")
        self.top.overrideredirect(True)
        self.top.focus()
        self.top.bind("<FocusOut>", self.destroy)

        if position == "center":
            self.center(self.top)

        frame = Frame(self.top, bg=bordercolor)
        frame.pack(fill=BOTH, expand=True)
        frame.columnconfigure(0, weight=1)
        fram2 = Frame(frame, bg="black")
        fram2.pack(pady=10)
        self.label_title_image = Label(fram2, bg="black")
        self.label_title_image.grid(row=0, column=0)
        self.label_title_text = Label(fram2, bg="black", fg="white")
        self.label_title_text.grid(row=0, column=1)

        style = Style()
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        self.tree = Treeview(frame, style="mystyle.Treeview", padding=[0, 0, 0, 0], show="tree")

        scroll = Scrollbar(self.tree, bd=0, bg="#2c2c2c", troughcolor="#161616", takefocus=False)
        scroll.pack(side=RIGHT, fill="y", pady=20)
        self.tree.config(yscrollcommand=scroll.set)
        scroll.config(command=self.tree.yview)

        s = Style()
        s.theme_use('clam')
        s.configure('Treeview', hightlightthickness=0, background="black",
                    foreground="white", fieldbackground="black",
                    bd=0, font=('Calibri', 11))
        s.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        s.map('Treeview', background=[('selected', '#BFBFBF')],
              foreground=[('selected', 'black')])  # Selection mode
        self.tree.pack(fill=BOTH, expand=True, padx=self.bd, pady=self.bd)

    def title(self, text="", image=None):
        if image is None:
            self.label_title_text.config(text=text)
        else:
            self.label_title_image.config(image=image)
            self.label_title_text.config(text=text)

    def update(self):
        self.tree.update()
        self.tree.update_idletasks()

    def destroy(self, event=None):
        self.top.destroy()

    def add_command(self, text='', image=None, index=0):
        if image is None:
            self.tree.insert(parent='', index='end', text=text, values=(index,))
        else:
            self.tree.insert(parent='', index='end', text=text, image=image, values=(index,))

    @staticmethod
    def center(toplevel):
        toplevel.update_idletasks()
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2
        toplevel.geometry("+%d+%d" % (x, y))

    def onclick(self, function):
        self.tree.bind("<Button-1>", lambda event: function(event, self.tree))
