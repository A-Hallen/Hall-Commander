# The main menubar of the app
from tkinter import Menu, FLAT

import vars


class _Menu:
    def __init__(self, root, name_of_the_app):
        self.menu = Menu(root, tearoff=False, relief=FLAT, bd=9, bg=vars.dark_gray,
                         fg="black", activeforeground="green", activebackground=vars.dark_gray, type="menubar")
        self.menu.config(bg=vars.soft_gray, bd=0, relief=FLAT, activeborderwidth=0)
        # The menu of files, o sea, archivos
        menu_archivo = Menu(self.menu, tearoff=False, relief=FLAT, bd=9, bg=vars.dark_gray,
                            fg="white", activeforeground="green", activebackground=vars.dark_gray)
        menu_archivo.add_command(label="Nuevo Archivo")
        menu_archivo.add_command(label="Nueva Carpeta")
        menu_archivo.add_command(label="Comprimir")
        menu_archivo.add_command(label="Descomprimir")
        menu_archivo.add_command(label="Salir")

        # Menu edicion
        menu_edit = Menu(self.menu, tearoff=0, bd=10, relief=FLAT, bg=vars.dark_gray, fg="white",
                         activeforeground="green", activebackground=vars.dark_gray)
        menu_edit.add_command(label="Copiar")
        menu_edit.add_command(label="Pegar")
        menu_edit.add_command(label="Cortar")
        menu_edit.add_command(label="Borrar")
        menu_edit.add_command(label="Cambiar Nombre")
        menu_edit.add_command(label="Buscar")
        menu_edit.add_command(label="Propiedades")

        # menu ir
        menu_ir = Menu(self.menu, tearoff=0, bd=10, relief=FLAT, bg=vars.dark_gray, fg="white",
                       activeforeground="green", activebackground=vars.dark_gray)
        menu_ir.add_command(label="Atras")
        menu_ir.add_command(label="Adelante")
        menu_ir.add_command(label="Inicio")
        menu_ir.add_command(label="Raiz")

        # Archivo, Editar, ir, vista, herramientas, preferencias, ayuda.
        # Menu vista
        menu_vista = Menu(self.menu, tearoff=0, bd=10, relief=FLAT, bg=vars.dark_gray, fg="white",
                          activeforeground="green", activebackground=vars.dark_gray)
        menu_vista.add_command(label="Acercar")
        menu_vista.add_command(label="Alejar")
        menu_vista.add_command(label="Mostrar Archivos Ocultos")
        menu_vista.add_command(label="Recargar")
        menu_vista.add_command(label="Personalizar")

        # Menu Herramientas
        menu_herramientas = Menu(self.menu, tearoff=0, bd=10, relief=FLAT, bg=vars.dark_gray, fg="white",
                                 activeforeground="green", activebackground=vars.dark_gray)
        menu_herramientas.add_command(label="Abrir una terminal aqui")
        menu_herramientas.add_command(label="Abrir una terminal como administrador")
        menu_herramientas.add_command(label="Abrir " + name_of_the_app + " como administrador")

        # Menu preferencias
        menu_preferencias = Menu(self.menu, tearoff=0, bd=10, relief=FLAT, bg=vars.dark_gray, fg="white",
                                 activeforeground="green", activebackground=vars.dark_gray)
        menu_preferencias.add_command(label="Configurar " + name_of_the_app)
        menu_preferencias.add_command(label="Mostrar barra de herramientas")
        menu_preferencias.add_command(label="Mostrar barra de menu")

        # Menu menus
        self.menu.add_cascade(label="Archivo", menu=menu_archivo)
        self.menu.add_cascade(label="Editar", menu=menu_edit)
        self.menu.add_cascade(label="Ir", menu=menu_ir)
        self.menu.add_cascade(label="Vista", menu=menu_vista)
        self.menu.add_cascade(label="Herramientas", menu=menu_herramientas)
        self.menu.add_cascade (label="Preferencias", menu=menu_preferencias)
