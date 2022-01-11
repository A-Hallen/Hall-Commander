import json
import subprocess
from pathlib import Path
from tkinter import Menu, Toplevel, Entry, filedialog, Button, BOTH, Frame, Label

import PIL
from PIL import Image, ImageTk

import vars
from center_frame import VerticalBarCommands


class VerticalBar:
    def __init__(self, vertical_frame, left, listar_r, listar_l, left_path, right_path):
        self.imagen = None
        self.image_path = "unknown_program.png"
        self.folder_path = "folder.png"
        self.top = None
        self.left = left
        self.vertical_frame = vertical_frame
        self.entry: Entry
        self.listar_r = listar_r
        self.listar_l = listar_l
        self.left_path = left_path
        self.right_path = right_path

    def open_link(self, event, order):
        left = vars.selection_left
        if left == True:
            label = self.left_path
            listar = self.listar_l
        else:
            label = self.right_path
            listar = self.listar_r
        name = Path (order).name
        listar.listar (label, name, order)

    def start(self, event):
        menu = Menu (self.vertical_frame, tearoff=False)
        menu.add_command (label="Add Command", command=self.command)
        menu.add_command (label="Add Link", command=(lambda link=True: self.command (link)))
        menu.tk_popup (event.x_root, event.y_root)

    def command(self, link=False):
        self.top = Toplevel (self.vertical_frame, bg="black")
        self.top.resizable (False, False)
        self.top.geometry ('300x120')
        frame = Frame (self.top, borderwidth=1, highlightthickness=1, highlightcolor=vars.soft_gray, bg="black")
        frame.pack (pady=10, padx=10, fill=BOTH)
        self.entry = Entry (frame, bg=vars.soft_gray)

        if link == True:
            self.entry.bind ('<Return>', self.create_link)
        else:
            self.entry.bind ('<Return>', self.create_item)
        self.entry.focus ()
        self.entry.grid (row=0, column=0, padx=10, pady=10)
        button = Button (frame, text="Open", command=self.openfile)
        button.grid (row=0, column=1, padx=10, pady=10)
        close_frame = Frame (self.top, bg="black")
        close_frame.pack (fill="x", padx=13)
        cancelar = Button (close_frame, text="Cancelar", command=self.close)
        cancelar.pack (side='left')

        if link == True:
            aceptar = Button (close_frame, text="Aceptar", command=self.aceptar_link)
        else:
            aceptar = Button (close_frame, text="Aceptar", command=self.aceptar)
        aceptar.pack (side='right')

    def close(self):
        self.top.destroy ()

    def aceptar(self):
        self.create_item (None)

    def aceptar_link(self):
        self.create_link (None)

    def create_link(self, event):
        try:
            order = self.entry.get ()
            image = Image.open (self.folder_path)
            img = image.resize ((35, 35), Image.ANTIALIAS)
            self.imagen = ImageTk.PhotoImage (img)
            rows = self.vertical_frame.grid_size ()[1]
            item = Label (master=self.vertical_frame, image=self.imagen, height=35, width=35, text=str (rows),
                          bg=vars.soft_gray)

            def execute_link(event):
                self.open_link (event, order)

            item.bind ('<Button-1>', execute_link)

            def _menu(event):
                class_ = VerticalBarCommands (self.vertical_frame, self.listar_r, self.listar_l, self.left_path,
                                              self.right_path)
                class_.menu_popup (event)

            item.bind ('<Button-3>', _menu)
            item.grid (column=0, row=rows)

            f = open ("preferences.json", "r")
            c = f.read ()
            f.close ()
            js = json.loads (c)
            data = [rows, self.folder_path, order, True]
            js["commands"][str (rows)] = data
            s = json.dumps (js, indent=4)
            f = open ("preferences.json", "w")
            f.write (s)
        except PIL.UnidentifiedImageError:
            print ("El archivo no es una imagen valida")
        finally:
            self.close ()

    def create_item(self, e):
        try:
            order = self.entry.get ()
            image = Image.open (self.image_path)
            img = image.resize ((35, 35), Image.ANTIALIAS)
            self.imagen = ImageTk.PhotoImage (img)
            rows = self.vertical_frame.grid_size ()[1]
            item = Label (master=self.vertical_frame, image=self.imagen, height=35, width=35, text=str (rows),
                          bg=vars.soft_gray)

            def execute(event):
                subprocess.run (order + " &", shell=True)

            item.bind ('<Button-1>', execute)

            def _menu(event):
                class_ = VerticalBarCommands (self.vertical_frame, self.listar_r, self.listar_l, self.left_path,
                                              self.right_path)
                class_.menu_popup (event)

            item.bind ('<Button-3>', _menu)
            item.grid (column=0, row=rows)

            # Ahora procedemos a guardar la configuracion de este comando en un json
            f = open ("preferences.json", "r")
            c = f.read ()
            f.close ()
            js = json.loads (c)
            print (str (rows))
            data = [rows, self.image_path, order, False]
            js["commands"][str (rows)] = data
            s = json.dumps (js, indent=4)
            f = open ("preferences.json", "w")
            f.write (s)
        except PIL.UnidentifiedImageError:
            print ("El archivo no es una imagen valida")
        finally:
            self.close ()

    def openfile(self):
        if self.left:
            dire = vars.actual_left_path
        else:
            dire = vars.actual_right_path
        file = filedialog.askopenfilename (title="Escoje un Icono", initialdir=dire,
                                           filetypes=(("Imagenes", ".png", ".jpg"), ("All", "*.*")))
        if file:
            self.image_path = file
            self.top.lift ()
        else:
            self.top.destroy ()

    def initialize(self, imagen):
        print ("Now this function is executing some script")
        f = open ("preferences.json", "r")
        c = f.read ()
        f.close ()
        js = json.loads (c)
        commands = js["commands"]
        if len (commands) != 0:
            for i in range (len (commands)):
                e = commands[str (i + 1)]
                row = e[0]
                image_path = e[1]
                order = e[2]
                print (order)

                image = Image.open (image_path)
                img = image.resize ((35, 35), Image.ANTIALIAS)
                self.imagen = ImageTk.PhotoImage (img)
                item = Label (master=self.vertical_frame, image=self.imagen, height=35, width=35, bg=vars.soft_gray)

                def execute(event):
                    subprocess.run (order + " &", shell=True)

                item.bind ('<Button-1>', execute)
                item.grid (column=0, row=row)
