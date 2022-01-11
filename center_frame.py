import json
import subprocess
from pathlib import Path
from tkinter import Label, Menu, Toplevel, Frame, BOTH, Entry, Button, filedialog

import PIL
from PIL import Image, ImageTk

import vars


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------Initialize the images of the central frame---------------
# ----------------------------------------------------------------------------------------------------------------------


class VerticalBarCommands:
    def __init__(self, center_frame, listar_r, listar_l, left_path, right_path):
        f = open ("preferences.json")
        c = f.read ()
        f.close ()
        js = json.loads (c)
        self.center_frame = center_frame
        self.commands = js["commands"]
        self.image_array = []
        self.order_array = []
        self.index_array = []
        self.foto_array = []
        self.link_array = []
        self.image_path = ""
        self.listar_r = listar_r
        self.listar_l = listar_l
        self.left_path = left_path
        self.right_path = right_path

    @staticmethod
    def executes(over):
        subprocess.run (over + " &", shell=True)

    def command(self):

        if len (self.commands) != 0:
            for i in range (len (self.commands)):
                if not str (i + 1) in self.commands:
                    i = i + 1
                if self.commands[str (i + 1)] == "":
                    self.image_array.insert (i, "")
                    continue
                e = self.commands[str (i + 1)]
                row = e[0]
                image_path = e[1]
                self.index_array.append (i)
                self.order_array.insert (i, e[2])
                self.link_array.insert (i, e[3])
                try:
                    image = Image.open (image_path)
                except FileNotFoundError:
                    image = Image.open ("unknown_program.png")
                img = image.resize ((35, 35), Image.ANTIALIAS)
                self.image_array.insert (i, ImageTk.PhotoImage (img))
                item = Label (master=self.center_frame, image=self.image_array[i],
                              height=35, text=str (i + 1), width=35, bg=vars.soft_gray)

                def execute(event, index):
                    if self.link_array[index] == True:
                        self.open_link (self.order_array[index])
                    else:
                        self.executes (self.order_array[index])

                item.bind ('<Button-1>', lambda event, index=i: execute (event, index))
                item.bind ('<Button-3>', self.menu_popup)
                item.grid (column=0, row=row)

    def open_link(self, order):
        left = vars.selection_left
        if left == True:
            listar = self.listar_l
            label = self.left_path
        else:
            listar = self.listar_r
            label = self.right_path

        name = Path (order).name
        listar.listar (label, str (name), order)

    def menu_popup(self, event):
        widget = event.widget
        text = widget.cget ("text")

        def eliminar():
            widget.destroy ()

            f = open ("preferences.json", "r")
            c = f.read ()
            f.close ()
            js = json.loads (c)
            commands = js["commands"]
            for i in range (len (commands)):
                if str (i + 1) == text:
                    del js["commands"][str (i + 1)]

            s = json.dumps (js, indent=4)
            f = open ("preferences.json", "w")
            f.write (s)
            f.close ()

        def edit():
            f = open ("preferences.json", "r")
            c = f.read ()
            f.close ()
            js = json.loads (c)
            commands = js["commands"]
            texto = ""
            foto = []
            indice = 0
            for i in range (len (commands)):
                if str (i + 1) == text:
                    texto = js["commands"][str (i + 1)][2]
                    foto.append (js["commands"][str (i + 1)][1])
                    indice = js["commands"][str (i + 1)][0]
            self.edit_message (texto, foto, indice, widget)

        menu = Menu (self.center_frame, tearoff=False)
        menu.add_command (label="Eliminar", command=eliminar)
        menu.add_command (label="Editar", command=edit)
        menu.tk_popup (event.x_root, event.y_root)

    def edit_message(self, texto, foto, indice, widget):
        top = Toplevel (self.center_frame, bg="black")

        # ---------------------
        def openfile():
            self.image_path = filedialog.askopenfilename (title="Escoje un Icono", initialdir=vars.actual_left_path,
                                                          filetypes=(("Imagenes", ".png", ".jpg"), ("All", "*.*")))
            if self.image_path:
                top.lift ()
            else:
                self.image_path = foto[0]
                top.destroy ()

        # ---------------------
        top.resizable (False, False)
        top.geometry ('300x120')
        frame = Frame (top, borderwidth=1, highlightthickness=1, highlightcolor=vars.soft_gray, bg="black")
        frame.pack (pady=10, padx=10, fill=BOTH)
        entry = Entry (frame, bg=vars.soft_gray)
        entry.insert (0, texto)

        # ..........................................................................

        # ---------------------
        def close():
            top.destroy ()

        def aceptar():
            create_item (None)

        # ---------------------

        def create_item(e):
            try:
                order = entry.get ()
                if self.image_path == "":
                    image = Image.open (foto[0])
                else:
                    image = Image.open (self.image_path)

                img = image.resize ((35, 35), Image.ANTIALIAS)
                self.foto_array.append (ImageTk.PhotoImage (img))
                rows = indice
                item = Label (master=self.center_frame, image=self.foto_array[0], height=35, width=35,
                              text=str (indice), bg=vars.soft_gray)

                def execute(event):

                    if self.link_array[indice - 1] == True:
                        self.open_link (self.order_array[indice - 1])
                    else:
                        subprocess.run (order + " &", shell=True)

                def _menu(event):
                    class_ = VerticalBarCommands (self.center_frame, self.listar_r, self.listar_l, self.left_path,
                                                  self.right_path)
                    class_.menu_popup (event)

                item.bind ('<Button-1>', execute)
                item.bind ('<Button-3>', _menu)
                widget.destroy ()
                item.grid (column=0, row=rows)

                # Ahora procedemos a guardar la configuracion de este comando en un json
                f = open ("preferences.json", "r")
                c = f.read ()
                f.close ()
                js = json.loads (c)
                e = js["commands"][str (indice)][3]
                if self.image_path == "":
                    data = [rows, foto[0], order, e]
                else:
                    data = [rows, self.image_path, order, e]

                js["commands"][str (rows)] = data
                s = json.dumps (js, indent=4)
                f = open ("preferences.json", "w")
                f.write (s)
            except  PIL.UnidentifiedImageError:
                print ("El archivo no es una imagen valida")
            finally:
                close ()

        # ..........................................................................
        entry.bind ('<Return>', create_item)
        entry.focus ()
        entry.grid (row=0, column=0, padx=10, pady=10)
        button = Button (frame, text="Open", command=openfile)
        button.grid (row=0, column=1, padx=10, pady=10)
        close_frame = Frame (top, bg="black")
        close_frame.pack (fill="x", padx=13)
        cancelar = Button (close_frame, text="Cancelar", command=close)
        cancelar.pack (side='left')
        aceptar = Button (close_frame, text="Aceptar", command=aceptar)
        aceptar.pack (side='right')
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
