import json
import os
import subprocess
from os.path import splitext
from tkinter import Frame, Button, Menu, FLAT, Toplevel, BOTH, Entry, filedialog, Label

from PIL import Image, ImageTk
from gi import require_version

import vars
from popup_menu import PopUpMenu

require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk


class HorizontalBar:
    """
    Class for called when we start the app for
    in a separate thread, fill all the icons for
    programs
    """

    def __init__(self, frame):
        self.program_icon_array = []
        self.frame: Frame = frame
        self.imagenes = []
        self.fotos_urls = []
        with open("preferences.json", "r") as prefs:
            read = prefs.read()
            self.js = json.loads(read)

    @staticmethod
    def execute_command(event, js):
        order = js[event.widget.cget("text")][1]
        subprocess.run(order + " &", shell=True)

    def edit(self, text, button: Button):
        with open("preferences.json", "r") as f:
            js = json.loads(f.read())["toolbar"][text]
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
            btn_text = button.cget("text")
            image = Image.open(self.fotos_urls[column - 4])
            image.thumbnail((25, 25), Image.ANTIALIAS)
            imagen = ImageTk.PhotoImage(image)
            self.imagenes.insert(column, imagen)
            button.config(image=self.imagenes[column])
            self.js["toolbar"][btn_text][0] = self.fotos_urls[column - 4]
            self.js["toolbar"][btn_text][1] = order
            with open("preferences.json", "w") as file:
                file.write(json.dumps(self.js, indent=4))
            close()

        def openfile():
            file = filedialog.askopenfilename(title="Escoje un Icono", initialdir=vars.actual_right_path,
                                              filetypes=(("all", "*.*"),))
            if file:
                self.fotos_urls[column - 4] = file
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

        aceptar = Button(close_frame, text="Aceptar", command=editar)
        entry.bind("<Return>", lambda event: editar())
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

    def back_fun_release(self, event, left_tree, right_tree, listar_l, listar_r, left_path, right_path):
        boton = event.widget
        boton.config(image=self.imagenes[1][0])
        if left_tree.selection():
            if len(vars.opened_left_paths) > 1:
                back_path = vars.opened_left_paths[len(vars.opened_left_paths) - 2]
                name = os.path.basename(back_path)
                vars.opened_left_forward.append(vars.actual_left_path)
                listar_l.listar(left_path, name, back_path)
                vars.opened_left_paths.__delitem__(len(vars.opened_left_paths) - 1)
                vars.opened_left_paths.__delitem__(len(vars.opened_left_paths) - 1)

        elif right_tree.selection():
            if len(vars.opened_right_paths) > 1:
                back_path = vars.opened_right_paths[len(vars.opened_right_paths) - 2]
                name = os.path.basename(back_path)
                vars.opened_right_forward.append(vars.actual_right_path)
                listar_r.listar(right_path, name, back_path)
                vars.opened_right_paths.__delitem__(len(vars.opened_right_paths) - 1)
                vars.opened_right_paths.__delitem__(len(vars.opened_right_paths) - 1)

    def back_fun_press(self, event):
        event.widget.config(image=self.imagenes[1][1])

    def forward_fun_press(self, event):
        event.widget.config(image=self.imagenes[2][1])

    def forward_fun_release(self, event, left_tree, right_tree, listar_l, listar_r, left_path, right_path):
        event.widget.config(image=self.imagenes[2][0])
        if left_tree.selection():
            if len(vars.opened_left_forward) > 0:
                forward_path = vars.opened_left_forward[len(vars.opened_left_forward) - 1]
                vars.opened_left_paths.append(vars.actual_left_path)
                listar_l.listar(left_path, os.path.basename(forward_path), forward_path)
                vars.opened_left_forward.__delitem__(len(vars.opened_left_forward) - 1)
        elif right_tree.selection():
            if len(vars.opened_right_forward) > 0:
                forward_path = vars.opened_right_forward[len(vars.opened_right_forward) - 1]
                vars.opened_right_paths.append(vars.actual_right_path)
                listar_r.listar(right_path, os.path.basename(forward_path), forward_path)
                vars.opened_right_forward.__delitem__(len(vars.opened_right_forward) - 1)

    @staticmethod
    def actualizar(left_path, right_path, listar_r, listar_l, left_tree, right_tree):
        from actualizar import Actualizar
        update = Actualizar(left_path, right_path, listar_r, listar_l)
        if left_tree.selection():
            update.update_left()
        elif right_tree.selection():
            update.update_right()
        else:
            update.update()

    def hide(self, event, left_path, right_path, listar_r, listar_l, left_tree, right_tree):
        preferences = open("preferences.json", "r")
        read = preferences.read()
        preferences.close()
        js = json.loads(read)
        if not js["hidden"][0]:
            js["hidden"][0] = True
            save = json.dumps(js, indent=4)
            prefs = open("preferences.json", "w")
            prefs.write(save)
            vars.hidden = True
            event.widget.config(image=self.imagenes[3][0])
        else:
            js["hidden"][0] = False
            save = json.dumps(js, indent=4)
            prefs = open("preferences.json", "w")
            prefs.write(save)
            vars.hidden = False
            event.widget.config(image=self.imagenes[3][1])
        from actualizar import Actualizar
        Actualizar(left_path, right_path, listar_r, listar_l).update()

    def load_pred(self, left_path, right_path, listar_r, listar_l, left_tree, right_tree):
        from some_functions import image
        self.imagenes.append(image("resources/update.ico", (25, 25)))
        self.imagenes.append([image("resources/back.png", (25, 25)),
                              image("resources/back_pressed.png", (25, 25))])
        self.imagenes.append([image("resources/forward.png", (25, 25)),
                              image("resources/forward_pressed.png", (25, 25))])
        self.imagenes.append([image("resources/btn_off.png", (25, 25)),
                              image("resources/btn_on.png", (25, 25))])
        update = Label(self.frame, image=self.imagenes[0], bg=vars.soft_gray, bd=0, highlightthickness=0)
        update.grid(row=0, column=0)
        update.bind("<Button-1>", lambda event: self.actualizar(left_path, right_path,
                                                                listar_r, listar_l, left_tree, right_tree))
        back = Label(self.frame, image=self.imagenes[1][0], bg=vars.soft_gray, bd=0, highlightthickness=0)
        back.grid(row=0, column=1, padx=5, pady=5)
        back.bind("<ButtonPress-1>", self.back_fun_press)
        back.bind("<ButtonRelease-1>", lambda event: self.back_fun_release(event,
                                                                           left_tree, right_tree, listar_l, listar_r,
                                                                           left_path, right_path))

        forward = Label(self.frame, image=self.imagenes[2][0], bg=vars.soft_gray, bd=0, highlightthickness=0)
        forward.grid(row=0, column=2, padx=5, pady=5)
        forward.bind("<ButtonPress-1>", self.forward_fun_press)
        forward.bind("<ButtonRelease-1>", lambda event: self.forward_fun_release(event,
                                                                                 left_tree, right_tree, listar_l,
                                                                                 listar_r, left_path, right_path))
        if vars.hidden:
            hidden = Label(self.frame, image=self.imagenes[3][0], bg=vars.soft_gray, bd=0, highlightthickness=0)
        else:
            hidden = Label(self.frame, image=self.imagenes[3][1], bg=vars.soft_gray, bd=0, highlightthickness=0)
        hidden.grid(row=0, column=3)
        hidden.bind("<Button-1>", lambda event: self.hide(event, left_path, right_path,
                                                          listar_r, listar_l, left_tree, right_tree))

    def start(self):
        """
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
            image.thumbnail((25, 25), Image.ANTIALIAS)
            self.imagenes.append(ImageTk.PhotoImage(image))
            label = Button(self.frame, text=i, image=self.imagenes[var + 4], bg=vars.soft_gray, bd=0,
                           highlightthickness=0)
            label.bind('<Button-1>', lambda event: self.execute_command(event, js))
            label.bind('<Button-3>', lambda event: self.execute_left(event))
            label.grid(row=0, column=columns, padx=5, pady=5)

    def command(self):
        def aceptar_(entr):
            text = entr.get()
            if text == "":
                return
            with open("preferences.json", "r") as f:
                js = json.loads(f.read())
            columns = self.frame.grid_size()[0]
            while True:
                if not str(columns) in js["toolbar"]:
                    js["toolbar"][str(columns)] = ["resources/terminal.ico", text]
                    with open("preferences.json", "w") as file:
                        file.write(json.dumps(js, indent=4))
                        self.js = js
                    break
                else:
                    columns += 1
            image = Image.open("resources/terminal.ico")
            image.thumbnail((25, 25), Image.ANTIALIAS)
            self.imagenes.append(ImageTk.PhotoImage(image))
            self.fotos_urls.append("resources/terminal.ico")
            label = Button(self.frame, text=str(columns),
                           image=self.imagenes[-1], bg=vars.soft_gray, bd=0, highlightthickness=0)
            label.bind('<Button-1>', lambda e: self.execute_command(e, text))
            label.bind('<Button-3>', lambda e: self.execute_left(e))
            label.grid(row=0, column=columns, padx=5, pady=5)
            top.destroy()

        top = Toplevel(self.frame, bg="black")
        top.resizable(False, False)
        top.geometry('300x120')
        frame = Frame(top, borderwidth=1, highlightthickness=1, highlightcolor=vars.soft_gray, bg="black")
        frame.pack(pady=10, padx=10, fill=BOTH)
        entry = Entry(frame, bg=vars.soft_gray)
        entry.focus()
        top.transient(self.frame.master)
        entry.pack(fill="x")
        close_frame = Frame(top, bg="black")
        close_frame.pack(fill="x", padx=13)
        cancelar = Button(close_frame, text="Cancelar", command=top.destroy)
        cancelar.pack(side='left')
        aceptar = Button(close_frame, text="Aceptar", command=lambda: aceptar_(entry))
        aceptar.pack(side='right')
        top.bind("<Escape>", lambda event: top.destroy())

    def program(self):
        apps = Gio.app_info_get_all()
        menu_ = PopUpMenu(self.frame.master, bd=10, bordercolor="black")
        menu_.title(text="Escoge una Aplicación")

        def launch(event, tree):
            item_ = tree.identify("item", event.x, event.y)
            index = tree.item(item_, "values")[0]
            menu_.destroy()
            # Item clicked
            app = apps[int(index)]
            icon = app.get_icon()
            icon_theme = Gtk.IconTheme.get_default()
            icon_file = icon_theme.lookup_icon(icon.to_string(), 32, 0)
            command = app.get_commandline()
            if icon_file is not None:
                icon_path = icon_file.get_filename()
            else:
                icon_path = "resources/terminal.ico"
            with open("preferences.json", "r") as f:
                js = json.loads(f.read())
            columns = self.frame.grid_size()[0]
            while True:
                if not str(columns) in js["toolbar"]:
                    js["toolbar"][str(columns)] = [icon_path, command]
                    with open("preferences.json", "w") as file:
                        file.write(json.dumps(js, indent=4))
                        self.js = js
                    break
                else:
                    columns += 1
            image = Image.open(icon_path)
            image.thumbnail((25, 25), Image.ANTIALIAS)
            self.imagenes.append(ImageTk.PhotoImage(image))
            self.fotos_urls.append(icon_path)
            label = Button(self.frame, text=str(columns),
                           image=self.imagenes[-1], bg=vars.soft_gray, bd=0, highlightthickness=0)
            label.bind('<Button-1>', lambda e: self.execute_command(e, self.js["toolbar"]))
            label.bind('<Button-3>', lambda e: self.execute_left(e))
            label.grid(row=0, column=columns, padx=5, pady=5)

        menu_.onclick(launch)

        def get_images(filename):
            pg = None
            try:
                formats = [".ppm", ".png", ".jpg", ".jpeg", ".gif", ".tiff", ".bmp"]
                if splitext(filename)[1].lower() in formats:
                    pil_img = Image.open(filename)
                    res_pil = pil_img.resize((30, 30), Image.ANTIALIAS)
                    pg = ImageTk.PhotoImage(res_pil)
                else:
                    from cairosvg import svg2png
                    png = svg2png(url=filename)
                    from io import BytesIO
                    pil_img = Image.open(BytesIO(png))
                    res_pil = pil_img.resize((30, 30), Image.ANTIALIAS)
                    pg = ImageTk.PhotoImage(res_pil)
            except:
                pil_img = Image.open("desconocido.png")
                res_pil = pil_img.resize((30, 30), Image.ANTIALIAS)
                pg = ImageTk.PhotoImage(res_pil)
            finally:
                return pg

        def start_thread():
            for index, app_ in enumerate(apps):
                if not app_.should_show():
                    self.program_icon_array.insert(index, None)
                    continue
                try:
                    icono = app_.get_icon()
                    icono_theme = Gtk.IconTheme.get_default()
                    icono_file = icono_theme.lookup_icon(icono.to_string(), 32, 0)
                    nombre = ""
                    if icono_file is not None:
                        nombre = icono_file.get_filename()
                except:
                    nombre = ""

                image_ = get_images(nombre)
                self.program_icon_array.insert(index, image_)
                menu_.add_command(text=app_.get_name(), image=self.program_icon_array[index], index=index)

        from threading import Thread
        hilo = Thread(target=start_thread)
        hilo.start()

    def start_menu(self, event):
        menu = Menu(self.frame, tearoff=False, relief=FLAT, bd=9, bg=vars.dark_gray,
                    fg="white", activeforeground="green", activebackground=vars.dark_gray)
        menu.add_command(label="Añadir comando", command=self.command)
        menu.add_command(label="Añadir programa", command=self.program)
        menu.tk_popup(event.x_root, event.y_root)
