import os

from PIL import Image, ImageTk

import vars
from get_file_icon import get_file_icon


class ListFiles:
    def __init__(self):
        self.back = None
        self.desconocido = None
        self.folder = None
        self.array = []

    def list(self, path):
        image = Image.open ("folder.png")
        img = image.resize ((30, 30), Image.ANTIALIAS)
        blank = Image.new ('RGBA', (36, 30))
        blank.paste (img, (0, 0, 30, 30))
        self.folder = ImageTk.PhotoImage (blank)
        blank.putalpha (100)
        self.folder_hidden = ImageTk.PhotoImage (blank)
        image = Image.open ("desconocido.png")
        img = image.resize ((30, 30), Image.ANTIALIAS)
        blank = Image.new ('RGBA', (36, 30))
        blank.paste (img, (0, 0, 30, 30))
        self.desconocido = ImageTk.PhotoImage (blank)

        image = Image.open ("back_button.png")
        img = image.resize ((30, 30), Image.ANTIALIAS)
        blank = Image.new ('RGBA', (36, 30))
        blank.paste (img, (0, 0, 30, 30))
        self.back = ImageTk.PhotoImage (blank)

        list_of_files: list = []
        try:
            list_of_files = os.listdir (path)
        except PermissionError:
            print ("Debes ejecutar este programa con permisos de administrador")
        lista = []

        last = 0
        if path != '/':
            lista.insert (0, ("..", "", "", str (0), self.back))
        if len (list_of_files) == 0:
            return lista
        for i in range (len (list_of_files)):
            # Nombre, extension, tamanio, iid
            lis = list_of_files[i]
            ipath = path + "/" + lis
            last = i
            if vars.hidden == True:
                if not lis.startswith ("."):
                    if os.path.isdir (ipath):
                        image = self.folder
                        lista.insert (i, (lis, "", "<DIR>", str (i), image))
            else:
                if os.path.isdir (ipath):
                    if lis.startswith ("."):
                        image = self.folder_hidden
                    else:
                        image = self.folder
                    lista.insert (i, (lis, "", "<DIR>", str (i), image))

        lista.sort ()
        listafiles = []
        for i in range (len (list_of_files)):
            lis = list_of_files[i]
            ipath = path + "/" + lis
            last = i + last
            self.array.insert (i, "")
            if vars.hidden == True:
                if not lis.startswith ("."):
                    if os.path.isfile (ipath):
                        image = self.desconocido
                        size = self.getsize (ipath)
                        listafiles.insert (i + last,
                                           (os.path.splitext (lis)[0], os.path.splitext (lis)[1], str (size), str (i),
                                            image))
            else:
                if os.path.isfile (ipath):
                    image = self.desconocido
                    size = self.getsize (ipath)
                    listafiles.insert (i + last,
                                       (os.path.splitext (lis)[0], os.path.splitext (lis)[1], str (size), str (i),
                                        image))
        listafiles.sort ()
        lista.extend (listafiles)
        return lista

    def getsize(self, path):
        bytes = os.path.getsize (path)
        if bytes <= 1024:
            return str (bytes) + "B"
        elif bytes <= 1048576:
            return str (round (bytes / 1024, 2)) + "Kb"
        elif bytes <= 1073741824:
            return str (round (bytes / 1048576)) + "Mb"
        elif bytes <= 1099511627776:
            return str (round (bytes / 1073741824)) + "Gb"

    @staticmethod
    def imagen(image_path):
        image = Image.open (image_path)
        img = image.resize ((30, 30), Image.ANTIALIAS)
        blank = Image.new ('RGBA', (36, 30))
        blank.paste (img, (0, 0, 30, 30))
        folder = ImageTk.PhotoImage (blank)
        return folder

    def get_icon(self, path, i, ext):
        self.array.insert (i, get_file_icon (path, ext))
        return self.array
