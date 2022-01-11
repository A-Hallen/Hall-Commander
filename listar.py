import os.path
from pathlib import Path

import vars
from get_file_icon import Load_Thumb
from list_files import ListFiles


class Listar:
    def __init__(self, left, class_tree, thumb: Load_Thumb):
        self.left = left
        self.thumb = thumb
        self.class_tree = class_tree
        self.listfiles = ListFiles ()
        self.array_images = []

    def listar(self, label, item_text, path):
        self.thumb.stop_thread ()
        if self.left == True:
            self.listar_left (label, item_text, path)
        else:
            self.listar_right (label, item_text, path)

    def listar_left(self, label, item_text, path):
        actual = vars.actual_left_path
        if item_text == "..":
            path = str (Path (actual).parent.absolute ())
        if self.check_file (path) == False:
            self.read_file (path)
        else:
            lista_l = self.listfiles.list (path)  # Obtenemos la lista de elementos que contiene esa carpeta
            self.class_tree.clear ()  # Limpiamos el contenido del TreeView
            self.class_tree.add_data (lista_l)  # Aniadimos los nuevos datos al treeView
            vars.actual_left_path = path  # Cambiamos la variable global actual_left_path que se encuentra en vars.py
            self.class_tree.tree.selection_add (0)
            self.class_tree.tree.focus (0)
            label.config (text=path)
            self.thumb.array = []
            self.thumb.actual = vars.actual_left_path
            self.thumb.tree = self.class_tree.tree
            self.thumb.clear ()
            self.thumb.start ()

    def listar_right(self, label, item_text, path):
        actual = vars.actual_right_path
        if item_text == "..":
            path = str (Path (actual).parent.absolute ())
        if self.check_file (path) == False:
            self.read_file (path)
        else:
            vars.actual_right_path = path  # Cambiamos la variable global actual_left_path que se encuentra en vars.py
            lista_l = self.listfiles.list (path)  # Obtenemos la lista de elementos que contiene esa carpeta
            self.class_tree.clear ()  # Limpiamos el contenido del TreeView
            self.class_tree.add_data (lista_l)  # Aniadimos los nuevos datos al treeView
            self.class_tree.tree.selection_add (0)
            self.class_tree.tree.focus (0)
            label.config (text=path)
            self.thumb.array = []
            self.thumb.actual = vars.actual_right_path
            self.thumb.tree = self.class_tree.tree
            self.thumb.clear ()
            self.thumb.start ()

    def check_file(self, path):
        if os.path.isdir (path):
            return True
        else:
            return False

    def read_file(self, path):
        print (path + " Is a file")
