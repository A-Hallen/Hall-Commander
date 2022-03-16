import os.path
import shutil
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import simpledialog, W, ttk, E
from tkinter.ttk import Progressbar

from PIL import Image, ImageTk

import vars


def buttonbox(top, frame, label, ok_pressed, cancel_pressed):
    ok_button = tk.Button(frame, text='Ok', width=5, command=ok_pressed, bg="black", fg="green")
    ok_button.pack(side="left", padx=10, pady=5)
    cancel_button = tk.Button(frame, text="Cancel", width=5, command=cancel_pressed, bg="black", fg="green")
    cancel_button.pack(side="right", padx=10, pady=5)
    top.bind("<Return>", lambda event: ok_pressed())
    top.bind("<Escape>", lambda event: cancel_pressed())
    label.focus()


class YesOrNoDialog:
    def __init__(self, parent, text, action, width, height):
        self.answer = False
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title(action + " " + text)
        self.top.config(padx=20, bg="black")
        self.top.geometry(str(width) + "x" + str(height))
        self.top.resizable(False, False)
        self.top.attributes('-alpha', 0.7)
        self.top.bind('FocusOut', self.focus_back)
        self.top.transient(self.top.master)
        self.top.grab_set()
        self.text = ""
        foto = ""
        if action == "Eliminar" or action == "eliminar":
            foto = Image.open("resources/borrar.png")
        elif action == "Copiar" or action == "copiar":
            foto = Image.open("resources/copiar.png")

        imagen = ImageTk.PhotoImage(foto)

        self.top.iconphoto(True, imagen)
        self.frame = tk.Frame(self.top, padx=20, pady=20, bg="black")
        self.frame.pack()
        self.label = tk.Label(self.frame, width=30, pady=5)
        self.label.pack(padx=10)
        paraph = "Deseas mover el archivo "
        if action == "Eliminar" or action == "eliminar":
            paraph = "Deseas Eliminar "
        elif action == "Copiar" or action == "copiar":
            paraph = "Deseas copiar "
        self.label.config(text=paraph + text + "?", bg="black", fg="green", anchor=W, pady=10)
        buttonbox(self.top, self.frame, self.label, self.ok_pressed, self.cancel_pressed)
        self.top.wait_window()

    def focus_back(self, event):
        self.label.focus_set()

    def ok_pressed(self):
        self.answer = True
        self.top.destroy()

    def cancel_pressed(self):
        self.top.destroy()


class MyDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.my_username = None
        self.root = parent
        super().__init__(parent, title)

    def body(self, frame):
        self.my_username_label = tk.Label(frame, width=25, text="Nuevo nombre")
        self.my_username_label.pack(padx=10)
        self.my_username_box = tk.Entry(frame, width=30)
        self.my_username_box.pack(padx=10)
        self.attributes('-alpha', 0.7)
        self.config(bg="black", )
        self.my_username_label.config(bg="black", fg="white")
        frame.config(bg="black")
        self.my_username_box.focus()
        self.root.update_idletasks()
        self.geometry('%dx%d+%d+%d' % (300, 100, 300, 200))
        foto = Image.open("resources/renombrar.png")
        imagen = ImageTk.PhotoImage(foto)
        self.config(padx=20)
        self.iconphoto(True, imagen)
        self.root.update_idletasks()

        root_name = self.root.winfo_pathname(self.root.winfo_id())
        dialog_name = self.winfo_pathname(self.winfo_id())
        self.root.tk.eval('tk::PlaceWindow {0} widget {1}'.format(dialog_name, root_name))
        return self.my_username_box

    def ok_pressed(self):
        self.my_username = self.my_username_box.get()
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        self.ok_button = tk.Button(self, text='Ok', width=5, command=self.ok_pressed, bg="black", fg="green")
        self.ok_button.pack(side="left", padx=15)
        cancel_button = tk.Button(self, text="Cancel", width=5, command=self.cancel_pressed, bg="black", fg="green")
        cancel_button.pack(side="right", padx=15)
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())
        self.my_username_box.focus()


class CustomDialog:
    def __init__(self, parent, text):
        self.top = tk.Toplevel(parent)
        self.top.title("Renombrar " + text)
        self.top.config(padx=20, bg="black")
        self.top.geometry("300x100")
        self.top.resizable(False, False)
        self.top.attributes('-alpha', 0.7)
        self.top.bind('<FocusOut>', self.focus_back)
        self.top.transient(parent)
        self.top.grab_set()
        self.text = ""
        foto = Image.open("resources/renombrar.png")
        imagen = ImageTk.PhotoImage(foto)
        self.top.iconphoto(True, imagen)
        self.frame = tk.Frame(self.top, padx=20, pady=20, bg="black")
        self.frame.pack()
        self.entry = tk.Entry(self.frame, width=30)
        self.entry.pack(padx=10)
        self.entry.focus()
        self.entry.insert(0, text)
        name = os.path.splitext(text)[0]
        self.entry.select_range(0, len(name))
        self.entry.icursor(len(name))
        buttonbox(self.top, self.frame, self.entry, self.ok_pressed, self.cancel_pressed)
        self.top.wait_window()

    def focus_back(self, event):
        self.entry.focus_set()

    def get_string(self):
        return self.entry.get()

    def ok_pressed(self):
        self.text = self.entry.get()
        self.top.destroy()

    def cancel_pressed(self):
        self.top.destroy()


threads = []


class CopyDialog:
    def __init__(self, items_path, destiny, listar, label_path, parent, actualizar):
        self.update = actualizar
        self.top = tk.Toplevel(parent)
        self.top.title("Copiar")
        self.top.config(padx=20, bg="black")
        self.top.geometry("400x140")
        self.top.resizable(False, False)
        self.top.attributes('-alpha', 0.7)
        foto = Image.open("resources/copiar.png")
        imagen = ImageTk.PhotoImage(foto)
        self.top.iconphoto(True, imagen)
        self.frame = tk.Frame(self.top, bg="black")
        self.frame.pack()
        self.label = tk.Label(self.frame, text="Calculando...", bg="black", fg="white")
        self.label_size = tk.Label(self.frame, text="", bg="black", fg=vars.soft_gray)
        self.label.grid(row=0, column=0)
        self.label_path_la = tk.Label(self.top, text="", bg="black", fg="green",
                                      pady=10, font=('Helvetica 10'), anchor=E)
        self.number_files = tk.Label(self.top, text="Archivos: ", bg="black", fg="red",
                                     anchor=W)
        self.number_files.pack()
        self.label_path_la.pack(fill="x")
        self.top_frame = tk.Frame(self.top, bg="black", pady=5)
        self.down_frame = tk.Frame(self.top, bg="black")
        self.top_label = tk.Label(self.top_frame, bg="black", fg="green", font=('Helvetica 10'), anchor=E)
        self.down_label = tk.Label(self.down_frame, bg="black", fg="green", font=('Helvetica 10'), anchor=W)
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("red.Horizontal.TProgressbar", foreground='black', background='green',
                    troughcolor='white', bordercolor="black", lightcolor="black", darkcolor="black")
        self.progress_bar = Progressbar(self.top_frame, style="red.Horizontal.TProgressbar",
                                        orient="horizontal", length=350, mode="determinate", )
        self.progress_bar_down = Progressbar(self.down_frame, style="red.Horizontal.TProgressbar",
                                             orient="horizontal", length=350, mode="determinate", )

        self.copiado = 0
        self.files = 0
        self.copied = 0
        self.destiny = destiny
        self.listar = listar
        self.label_path = label_path
        self.total_bytes = 0
        if len(items_path) == 1:
            if os.path.isdir(items_path[0]):
                def copy_rec():
                    self.total_bytes = self.get_directory_size(items_path[0])
                    self.number_files.destroy()
                    self.label_path_la.destroy()
                    self.label_size.config(text="Tamaño: " + str(get_size_format(self.total_bytes)))
                    self.label_size.grid(row=0, column=2, padx=10)
                    self.top_frame.pack()
                    self.top_label.pack(padx=25)
                    self.progress_bar.pack(ipady=4)
                    self.down_frame.pack()
                    self.down_label.pack(padx=25)
                    self.progress_bar_down.pack(ipady=4)
                    self.progress_bar_down.config(maximum=self.total_bytes)
                    self.label.config(text="Copiando...")
                    self.top.geometry("400x140")
                    self.copy_recursive(source=items_path[0], destiny=
                    os.path.join(destiny, Path(items_path[0]).name))
                    self.top.destroy()
                    self.update.update()

                ta = threading.Thread(name="recursive", target=copy_rec)
                threads.append(ta)
                ta.start()
            else:
                def copiar():
                    self.number_files.destroy()
                    self.label_path_la.destroy()
                    self.label_size.config(text="Tamaño: " + str(get_size_format(os.path.getsize(items_path[0]))))
                    self.label_size.grid(row=0, column=2, padx=10)
                    self.top_frame.pack()
                    self.top_label.pack(padx=25)
                    self.progress_bar.pack(ipady=4)
                    self.top_label.config(text=items_path[0], anchor=E)
                    self.down_label.config(text=destiny, anchor=E)
                    self.label.config(text="Copiando...")
                    self.top.geometry("400x120")
                    self.copy_with_progress(items_path[0], destiny, callback=self.copy_progress)
                    self.top.destroy()
                    self.update.update()

                t = threading.Thread(name="copiando", target=copiar)
                threads.append(t)
                t.start()
        else:
            def copy_markets():

                self.total_bytes = self.get_total_size(items_path)
                self.number_files.destroy()
                self.label_path_la.destroy()
                self.label_size.config(text="Tamaño: " + str(get_size_format(self.total_bytes)))
                self.label_size.grid(row=0, column=2, padx=10)
                self.top_frame.pack()
                self.top_label.pack(padx=25)
                self.progress_bar.pack(ipady=4)
                self.down_frame.pack()
                self.down_label.pack(padx=25)
                self.progress_bar_down.pack(ipady=4)
                self.progress_bar_down.config(maximum=self.total_bytes)
                self.label.config(text="Copiando...")
                self.top.geometry("400x140")
                for i in items_path:
                    if os.path.isdir(i):
                        self.copy_recursive(source=i, destiny=os.path.join(destiny, Path(i).name))
                    else:
                        self.copied = self.copied + 1
                        self.top_label.config(text=i)
                        self.down_label.config(text=(str(self.files) + "/" + str(self.copied)))
                        self.down_label.config(text="Archivos copiados: " + str(self.copied) + "/" + str(self.files))
                        self.copy_with_progress(i, os.path.join(destiny, Path(i).name),
                                                callback=self.copy_progress_folder)
                self.top.destroy()

            sa = threading.Thread(name="recursive", target=copy_markets)
            threads.append(sa)
            sa.start()

    def copy_progress_folder(self, copied, total):
        self.progress_bar.config(maximum=total)
        self.progress_bar['value'] = copied
        self.progress_bar_down['value'] = self.copiado

    def copy_progress(self, copied, total):
        self.progress_bar.config(maximum=total)
        self.progress_bar['value'] = copied

    def copy_with_progress(self, src, dst, *, follow_symlinks=True, callback):
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        self.copyfile(src, dst, follow_symlinks=follow_symlinks, callback=callback)
        return dst

    def copyfileobj(self, fsrc, fdst, callback, total, length=16 * 1024):
        copied = 0
        while True:
            buf = fsrc.read(length)
            if not buf:
                break
            fdst.write(buf)
            copied += len(buf)
            self.copiado += len(buf)
            callback(copied, total=total)

    def copyfile(self, src, dst, *, follow_symlinks=True, callback):
        """Copy data from src to dst.

        If follow_symlinks is not set and src is a symbolic link, a new
        symlink will be created instead of copying the file it points to.

        """
        if shutil._samefile(src, dst):
            raise shutil.SameFileError("{!r} and {!r} are the same file".format(src, dst))

        for fn in [src, dst]:
            try:
                st = os.stat(fn)
            except OSError:
                # File most likely does not exist
                pass
            else:
                # XXX What about other special files? (sockets, devices...)
                if shutil.stat.S_ISFIFO(st.st_mode):
                    raise shutil.SpecialFileError("`%s` is a named pipe" % fn)

        if not follow_symlinks and os.path.islink(src):
            os.symlink(os.readlink(src), dst)
        else:
            size = os.stat(src).st_size
            with open(src, 'rb') as fsrc:
                with open(dst, 'wb') as fdst:
                    self.copyfileobj(fsrc, fdst, callback=callback, total=size)
        return dst

    def copy_recursive(self, source, destiny, ignore=None):
        if os.path.isdir(source):
            if not os.path.isdir(destiny):
                os.makedirs(destiny)
            files = os.listdir(source)
            if ignore is not None:
                ignored = ignore(source, destiny)
            else:
                ignored = set()
            for f in files:
                if f not in ignored:
                    self.copy_recursive(os.path.join(source, f),
                                        os.path.join(destiny, f),
                                        ignore)
        else:
            self.copied = self.copied + 1
            self.top_label.config(text=source)
            self.down_label.config(text=(str(self.files) + "/" + str(self.copied)))
            self.down_label.config(text="Archivos copiados: " + str(self.copied) + "/" + str(self.files))
            self.copy_with_progress(source, destiny, callback=self.copy_progress_folder)
        # ------------------------#

    def get_directory_size(self, directory):
        """Returns the `directory` size in bytes."""

        total = 0
        try:
            # print("[+] Getting the size of", directory)
            for entry in os.scandir(directory):
                if entry.is_file():
                    self.files = self.files + 1
                    self.number_files.config(text="Archivos: " + str(self.files))
                    # if it's a file, use stat() function
                    total += entry.stat().st_size
                elif entry.is_dir():
                    self.label_path_la.config(text=entry.path)
                    # if it's a directory, recursively call this function
                    total += self.get_directory_size(entry.path)
        except NotADirectoryError:
            # if `directory` isn't a directory, get the file size then
            return os.path.getsize(directory)
        except PermissionError:
            # if for whatever reason we can't open the folder, return 0
            return 0
        return total

    def get_total_size(self, items_path):
        total = 0
        for i in items_path:
            if os.path.isdir(i):
                size = self.get_directory_size(i)
                total = total + size
            else:
                size_ = os.path.getsize(i)
                total = total + size_
        return total


class EliminarDialog:
    def __init__(self, path, name, parent, listar, label_path, actualpath):
        self.listar = listar
        self.label_path_main = label_path
        self.actualpath = actualpath
        self.path = path
        self.top = tk.Toplevel(parent)
        self.top.title("Eliminando " + name)
        self.top.config(padx=20, bg="black")
        self.top.geometry("400x140")
        self.top.resizable(False, False)
        self.top.attributes('-alpha', 0.7)
        foto = Image.open("resources/borrar.png")
        imagen = ImageTk.PhotoImage(foto)
        self.top.iconphoto(True, imagen)
        self.frame = tk.Frame(self.top, bg="black")
        self.frame.pack()
        self.label = tk.Label(self.frame, text="Calculando...", bg="black", fg="white")
        self.label_size = tk.Label(self.frame, text="35 Gb", bg="black", fg=vars.soft_gray)
        self.label.grid(row=0, column=0)
        self.label_eliminados = tk.Label(self.frame, bg="black", fg=vars.soft_gray)
        self.label_path = tk.Label(self.top, text=path, bg="black", fg="green",
                                   pady=10, font=('Helvetica 10'), anchor=E)
        self.number_files = tk.Label(self.top, text="Archivos: ", bg="black", fg="red",
                                     anchor=W)
        self.number_files.pack()
        self.label_path.pack(fill="x")
        self.top_frame = tk.Frame(self.top, bg="black", pady=5)
        self.down_frame = tk.Frame(self.top, bg="black")
        self.top_label = tk.Label(self.top_frame, bg="black", fg="green", font=('Helvetica 10'), anchor=W)
        self.down_label = tk.Label(self.down_frame, bg="black", fg="green", font=('Helvetica 10'), anchor=W)

        self.files = 0
        self.deleted = 0
        time.sleep(1)
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("red.Horizontal.TProgressbar", foreground='black', background='green',
                    troughcolor='white', bordercolor="black", lightcolor="black", darkcolor="black")
        self.progress_bar = Progressbar(self.top_frame, style="red.Horizontal.TProgressbar",
                                        orient="horizontal", length=350, mode="determinate", )
        self.progress_bar_down = Progressbar(self.down_frame, style="red.Horizontal.TProgressbar",
                                             orient="horizontal", length=350, mode="determinate", )

        t = threading.Thread(name="calculando", target=self.calculando)
        threads.append(t)
        t.start()

    def calculando(self):
        size = get_size_format(self.get_directory_size(self.path))
        self.label.config(text="Eliminando...")
        self.number_files.destroy()
        self.label_path.destroy()

        self.label_eliminados.grid(row=0, column=1)
        self.label_size.config(text="Tamaño: " + str(size))
        self.label_size.grid(row=0, column=2, padx=10)

        self.top_frame.pack()
        self.top_label.pack(padx=25)
        self.top_label.config(text=self.path + self.path + self.path)
        self.progress_bar.pack(ipady=4)
        self.down_frame.pack()
        self.down_label.pack(padx=25)
        self.down_label.config(text=self.path + self.path + self.path)
        self.progress_bar_down.pack(ipady=4)

        self.progress_bar_down.config(maximum=self.files)
        p = Path(self.path)
        if p.is_file():
            try:
                p.unlink()
                self.deleted = self.deleted + 1
                self.progress_bar_down.step()
                self.label_eliminados.config(text=(str(self.files) + "/" + str(self.deleted)))
            except:
                pass
        else:
            self.rm_tree(p)
        self.top.destroy()
        self.actualizar()

    def actualizar(self):
        name = Path(self.actualpath).name
        self.listar.listar(self.label_path_main, name, self.actualpath)

    def rm_tree(self, pth: Path):
        for f in os.listdir(pth):
            child = pth / f
            if child.is_file():
                try:
                    child.unlink()
                    self.deleted = self.deleted + 1
                    self.progress_bar_down.step()
                    self.label_eliminados.config(text=(str(self.files) + "/" + str(self.deleted)))
                except:
                    pass
            else:
                self.rm_tree(child)
        pth.rmdir()

    def get_directory_size(self, directory):
        """Returns the `directory` size in bytes."""
        total = 0
        try:
            # print("[+] Getting the size of", directory)
            for entry in os.scandir(directory):
                if entry.is_file():
                    self.files = self.files + 1
                    self.number_files.config(text="Archivos: " + str(self.files))
                    # if it's a file, use stat() function
                    total += entry.stat().st_size
                elif entry.is_dir():
                    self.label_path.config(text=entry.path)
                    # if it's a directory, recursively call this function
                    total += self.get_directory_size(entry.path)
        except NotADirectoryError:
            # if `directory` isn't a directory, get the file size then
            return os.path.getsize(directory)
        except PermissionError:
            # if for whatever reason we can't open the folder, return 0
            return 0
        return total


def get_size_format(b, factor=1024, suffix="b"):
    for unit in [" ", " K", " M", " G", " T", " P", " E", " Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
