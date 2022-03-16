import errno
import os
from tkinter import Entry

import vars
from MyDialog import CustomDialog, YesOrNoDialog, EliminarDialog, CopyDialog
from actualizar import Actualizar


class FileManipulation:
    def __init__(self, left_frame_list, right_frame_list, listar_l, listar_r, left_path, right_path, root,
                 update: Actualizar):
        self.left_path = left_path
        self.right_path = right_path
        self.listar_l = listar_l
        self.listar_r = listar_r
        self.left_frame_list = left_frame_list
        self.right_frame_list = right_frame_list
        self.root = root
        self.update = update

    def getsize(self, path):
        bytes = os.path.getsize(path)
        if bytes <= 1024:
            return str(bytes) + "B"
        elif bytes <= 1048576:
            return str(round(bytes / 1024, 2)) + "Kb"
        elif bytes <= 1073741824:
            return str(round(bytes / 1048576)) + "Mb"
        elif bytes <= 1099511627776:
            return str(round(bytes / 1073741824)) + "Gb"

    # function a considerar para la accion de renombrar

    def consideration(self, event, left=True):
        item = self.right_frame_list.tree.focus()
        bounding_box = self.right_frame_list.tree.bbox(item)
        entry = Entry(self.right_frame_list.tree, bg="black", fg="white")
        entry.focus()

        def destroy(event):
            entry.destroy()

        entry.bind("<FocusOut>", destroy)
        self.right_frame_list.tree.selection_remove(item)
        text = self.right_frame_list.tree.item(item, "text")
        entry.place(x=bounding_box[0] + 50, y=bounding_box[1], width=bounding_box[2] - 140, height=bounding_box[3])
        entry.insert(0, text)

    def f2(self, event, left=True):
        if left:
            item = self.left_frame_list.tree.focus()
            text = self.left_frame_list.tree.item(item, "text") + self.left_frame_list.tree.item(item, "values")[0]
        else:
            item = self.right_frame_list.tree.focus()
            text = self.right_frame_list.tree.item(item, "text") + self.right_frame_list.tree.item(item, "values")[0]
        dialog = CustomDialog(self.root, text)
        if dialog.text != "":
            if left:
                actualpath = vars.actual_left_path
                tree = self.left_frame_list.tree
            else:
                tree = self.right_frame_list.tree
                actualpath = vars.actual_right_path

            try:
                old = actualpath + "/" + text
                new = actualpath + "/" + dialog.text
                os.rename(old, new)
                self.update.update()
                if left:
                    if vars.actual_left_path == vars.actual_right_path:
                        self.update.update()
                tree.focus(item)
                for i in tree.get_children():
                    n = tree.item(i, "text") + tree.item(i, "values")[0]
                    if n == dialog.text:
                        tree.focus(i)
                        tree.selection_set(i)
            except PermissionError:
                print("Debes ejecutar este programa con permisos de administrador")

    def folder_dialog(self, event, left=True):
        dialog = CustomDialog(self.root, text="Nueva Carpeta")
        if dialog.text != "":
            if left:
                actualpath = vars.actual_left_path
            else:
                actualpath = vars.actual_right_path

            path = actualpath + "/" + dialog.text
            try:
                os.mkdir(path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                else:
                    print("El directorio ya existe")
            finally:
                self.update.update()

    def delete_dialog(self, event, left=True):
        if left:
            listar = self.listar_l
            label_path = self.left_path
            actualpath = vars.actual_left_path
            item = self.left_frame_list.tree.focus()
            text = self.left_frame_list.tree.item(item, "text") + self.left_frame_list.tree.item(item, "values")[0]
        else:
            listar = self.listar_r
            label_path = self.right_path
            actualpath = vars.actual_right_path
            item = self.right_frame_list.tree.focus()
            text = self.right_frame_list.tree.item(item, "text") + self.right_frame_list.tree.item(item, "values")[0]

        dialog = YesOrNoDialog(self.root, text, "Eliminar", height=120, width=300)
        if dialog.answer == True:
            path = actualpath + "/" + text
            EliminarDialog(path, text, self.root, listar, label_path, actualpath)

    def copy_dialog(self, event, left=True):
        if left:
            listar = self.listar_r
            label_path = self.right_path
            tree = self.left_frame_list.tree
            actual = vars.actual_left_path
            destiny = vars.actual_right_path
            items = tree.selection()
        else:
            listar = self.listar_l
            tree = self.right_frame_list.tree
            label_path = self.left_path
            actual = vars.actual_right_path
            destiny = vars.actual_left_path
            items = tree.selection()
        dialog_text = "estos archivos " + "\n hacia " + destiny
        if len(items) == 1:
            dialog_text = "" + tree.item(tree.focus(), "text") + "\n hacia " + destiny

        dialog = YesOrNoDialog(self.root, text=dialog_text, action="Copiar", width=350, height=150)
        if dialog.answer:
            items_path = []
            for i in items:
                if tree.item(i, "text") == "..":
                    continue
                paths = actual + "/" + tree.item(i, "text") + tree.item(i, "values")[0]
                items_path.append(paths)

            CopyDialog(items_path, destiny, listar, label_path, self.root, self.update)
