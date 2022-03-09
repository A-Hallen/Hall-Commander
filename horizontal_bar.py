import json
import subprocess
import threading
from tkinter import Frame, Button, Menu, FLAT, Toplevel, BOTH, Entry, filedialog

from PIL import Image, ImageTk

import vars


class HorizontalBar:
    """
    Class for called when we start the app for
    in a separate thread, fill all the icons for
    programs
    """

    def __init__(self, frame):
        self.frame: Frame = frame
        self.imagenes = []
        self.fotos_urls = []
        with open("preferences.json", "r") as prefs:
            read = prefs.read()
            self.js = json.loads(read)

    @staticmethod
    def execute_command(event, order):
        subprocess.run(order + " &", shell=True)

    def edit(self, text, button: Button):
        js = self.js["toolbar"][text]
        root = self.frame.master
        top = Toplevel(root, bg="black")
        top.resizable(False, False)
        top.geometry('300x120')
        top.transient(root)
        frame = Frame(top, borderwidth=1, highlightthickness=1, highlightcolor=vars.soft_gray, bg="black")
        frame.pack(pady=10, padx=10, fill=BOTH)
        entry = Entry(frame, bg=vars.soft_gray)
        entry.insert(0, js[1])
        column = button.grid_info().get("column")

        def editar():
            order = entry.get()
            image = Image.open(self.fotos_urls[column])
            image.thumbnail((35, 35), Image.ANTIALIAS)
            imagen = ImageTk.PhotoImage(image)
            self.imagenes.insert(column, imagen)
            button.config(image=self.imagenes[column])
            self.js["toolbar"][str(column + 1)][0] = self.fotos_urls[column]
            self.js["toolbar"][str(column + 1)][1] = order
            with open("preferences.json", "w") as file:
                file.write(json.dumps(self.js, indent=4))
            close()

        def openfile():
            file = filedialog.askopenfilename(title="Escoje un Icono", initialdir=vars.actual_right_path,
                                              filetypes=(("all", "*.*"),))
            if file:
                self.fotos_urls[column] = file
                top.lift()
            else:
                top.destroy()

        def close():
            top.destroy()

        entry.bind('<Return>', lambda event: editar())
        entry.focus()
        entry.grid(row=0, column=0, padx=10, pady=10)
        button_open = Button(frame, text="Open", command=openfile)
        button_open.grid(row=0, column=1, padx=10, pady=10)
        close_frame = Frame(top, bg="black")
        close_frame.pack(fill="x", padx=13)
        cancelar = Button(close_frame, text="Cancelar", command=close)
        cancelar.pack(side='left')

        aceptar = Button(close_frame, text="Aceptar", command=lambda: editar())
        aceptar.pack(side='right')

    def delete(self, i, label: Button):
        js = self.js["toolbar"]
        del js[i]
        with open("preferences.json", "w") as prefs:
            prefs.write(json.dumps(self.js, indent=4))
        label.destroy()

    def execute_left(self, event):
        button = event.widget
        text = button.cget("text")
        menu = Menu(self.frame, tearoff=False, relief=FLAT, bd=9, bg=vars.dark_gray,
                    fg="white", activeforeground="green", activebackground=vars.dark_gray)
        menu.add_command(label="Editar", command=lambda: self.edit(text, button))
        menu.add_command(label="Eliminar", command=lambda: self.delete(text, button))
        menu.tk_popup(event.x_root, event.y_root)

    def load_icons(self):
        """
        This is called in a separate thread
        here initialize the icons for the toolbar
        """
        js = self.js["toolbar"]
        for var, i in enumerate(js):
            columns = self.frame.grid_size()[0]
            try:
                self.fotos_urls.append(js[i][0])
                image = Image.open(js[i][0])
            except FileNotFoundError:
                self.fotos_urls.append("unknown_program.png")
                image = Image.open("unknown_program.png")
            image.thumbnail((35, 35), Image.ANTIALIAS)
            self.imagenes.append(ImageTk.PhotoImage(image))
            label = Button(self.frame, text=i, image=self.imagenes[var], bg=vars.soft_gray, bd=0, highlightthickness=0)
            label.bind('<Button-1>', lambda event: self.execute_command(event, js[i][1]))
            label.bind('<Button-3>', lambda event: self.execute_left(event))
            label.grid(row=0, column=columns, padx=5, pady=5)

    def start(self):
        """
        Function called in the start of our program,
        here we start the separate thread.
        """
        thread = threading.Thread(target=self.load_icons)
        thread.daemon = True
        thread.start()

    def start_menu(self, event):
        menu = Menu(self.frame, tearoff=False, relief=FLAT, bd=9, bg=vars.dark_gray,
                    fg="white", activeforeground="green", activebackground=vars.dark_gray)
        menu.add_command(label="Add Command")
        menu.tk_popup(event.x_root, event.y_root)
