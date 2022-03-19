import os.path
from pathlib import Path

import magic
from gi.repository import Gio

import vars
from list_files import ListFiles


class Listar:
    def __init__(self, left, class_tree, thumb):
        self.left = left
        self.thumb = thumb
        self.class_tree = class_tree
        self.listfiles = ListFiles()
        self.array_images = []

    def listar(self, label, item_text, path):
        self.thumb.stop_thread()
        if self.left:
            self.listar_left(label, item_text, path)
        else:
            self.listar_right(label, item_text, path)

    def listar_left(self, label, item_text, path):
        actual = vars.actual_left_path
        if item_text == "..":
            path = str(Path(actual).parent.absolute())
        if not self.check_file(path):
            self.read_file(path)
        else:
            lista_l = self.listfiles.list(path)  # Obtenemos la lista de elementos que contiene esa carpeta
            self.class_tree.clear()  # Limpiamos el contenido del TreeView
            self.class_tree.add_data(lista_l)  # Añadimos los nuevos datos al treeView
            vars.actual_left_path = path  # Cambiamos la variable global actual_left_path que se encuentra en vars.py
            if vars.opened_left_paths[-1] != path:
                vars.opened_left_paths.append(path)  # Añadimos el path a la lista de rutas que abrimos en la izquierda
            self.class_tree.tree.selection_add(0)
            self.class_tree.tree.focus(0)
            label.config(text=path)
            self.thumb.array = []
            self.thumb.actual = vars.actual_left_path
            self.thumb.tree = self.class_tree.tree
            self.thumb.clear()
            self.thumb.start()

    def listar_right(self, label, item_text, path):
        actual = vars.actual_right_path
        if item_text == "..":
            path = str(Path(actual).parent.absolute())
        if not self.check_file(path):
            self.read_file(path)
        else:
            vars.actual_right_path = path  # Cambiamos la variable global actual_left_path que se encuentra en vars.py
            lista_l = self.listfiles.list(path)  # Obtenemos la lista de elementos que contiene esa carpeta
            self.class_tree.clear()  # Limpiamos el contenido del TreeView
            self.class_tree.add_data(lista_l)  # Añadimos los nuevos datos al treeView
            if path != vars.opened_right_paths[-1]:
                vars.opened_right_paths.append(path)
            self.class_tree.tree.selection_add(0)
            self.class_tree.tree.focus(0)
            label.config(text=path)
            self.thumb.array = []
            self.thumb.actual = vars.actual_right_path
            self.thumb.tree = self.class_tree.tree
            self.thumb.clear()
            self.thumb.start()

    @staticmethod
    def check_file(path):
        if os.path.isdir(path):
            return True
        else:
            return False

    @staticmethod
    def read_file(path):
        mime = magic.Magic(mime=True)
        mime = mime.from_file(path)
        default = Gio.app_info_get_default_for_type(mime, False)
        file = Gio.File.new_for_path(path)
        default.launch([file])
