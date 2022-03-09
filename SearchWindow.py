import os
from pathlib import Path
from threading import Thread
from tkinter import Toplevel, BOTH, Frame, Scrollbar, RIGHT, Entry, HORIZONTAL
from tkinter.ttk import Style, Treeview

import PIL.Image
from PIL import ImageTk


class SearchWindow:
    def __init__(self, root, place, listar, label_path):
        self.top = Toplevel(root, bg="black")
        self.top.attributes("-alpha", 0.5)
        self.HOME = place
        self.listar = listar
        self.label_path = label_path
        self.top.wait_visibility()
        self.tree = None
        self.coincidencias = []
        foto = PIL.Image.open("resources/buscar.png")
        image = ImageTk.PhotoImage(foto)
        self.top.iconphoto(True, image)
        self.top.geometry("700x500")
        self.center(self.top)
        self.top.title("Buscar")

        # The main frame
        frame = Frame(self.top)
        frame.pack(fill=BOTH, expand=True)
        frame.columnconfigure(0, weight=1)

        # The entry search
        self.entry = Entry(frame, fg="green")

        self.entry.pack(fill="x", padx=5, pady=5)
        self.entry.bind("<Return>", self.buscar)

        # The tree view
        style = Style()
        style.configure("mystyle.Treeview", highlightthickness=1, bd=0, bordercolor="blue",
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 11, 'normal'),
                        borderwidth=0)  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        self.tree = Treeview(frame, style="mystyle.Treeview", padding=[0, 0, 0, 0])

        scroll = Scrollbar(self.tree, bd=0, bg="#2c2c2c", troughcolor="#161616", takefocus=False)
        scroll.pack(side=RIGHT, fill="y", pady=27)
        scrollh = Scrollbar(self.tree, bd=0, bg="#2c2c2c", troughcolor="#161616", takefocus=False, orient=HORIZONTAL)
        scrollh.pack(side="bottom", fill="x", padx=27)
        self.tree.config(yscrollcommand=scroll.set, xscrollcommand=scrollh.set)
        scroll.config(command=self.tree.yview)
        scrollh.config(command=self.tree.xview)

        self.tree['columns'] = "Path"
        self.tree.column("Path", minwidth=200)
        self.tree.column("#0", minwidth=500)
        self.tree.heading("#0", text="Nombre")
        self.tree.heading("Path", text="Direccion")

        s = Style()
        s.theme_use('clam')
        s.configure('Treeview', rowheight=35, hightlightthickness=0, background="black",
                    foreground="white", fieldbackground="black",
                    bd=0, font=('Calibri', 11))
        s.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        s.map('Treeview', background=[('selected', '#BFBFBF')], foreground=[('selected', 'black')])  # Selection mode

        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind("<Double-1>", self.enter)
        self.entry.focus_set()
        self.entry.focus()

    @staticmethod
    def center(toplevel):
        toplevel.update_idletasks()
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2
        toplevel.geometry("+%d+%d" % (x, y))

    def enter(self, event):
        item = self.tree.identify("item", event.x, event.y)
        text = self.tree.item(item, "text")
        path = Path(self.tree.item(item, "values")[0])
        parent = str(path.parent.absolute())
        self.listar.listar(self.label_path, text, parent)

    # Principal function
    def search(self, texto, home):
        try:
            lista = os.listdir(home)
        except PermissionError:
            return
        for archivo in lista:
            path = os.path.join(home, archivo)
            if texto.lower() in archivo.lower():
                self.coincidencias.append(os.path.join(home, archivo))
                index = len(self.tree.get_children())
                self.tree.insert(parent='', index=index, iid=str(index), text=archivo, values=(path,))
            if os.path.isdir(path):
                self.search(texto, path)

    def start(self, texto, home):
        self.search(texto, home)

    def buscar(self, event=None):
        self.coincidencias = []
        text = self.entry.get()
        self.tree.delete(*self.tree.get_children())
        hilo = Thread(target=self.start, args=(text, self.HOME))

        hilo.daemon = True
        hilo.start()
