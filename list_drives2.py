import os
from tkinter import Frame, Button, Label, Menu, FLAT

import psutil
from PIL import Image, ImageTk

import vars
from devices import Devices
from vars import soft_gray, dark_gray


class Drives:
    def __init__(self, drive_left, drive_right, label_left_t,
                 label_right_t, label_left_d, label_right_d,
                 listar_l, listar_r, left_path, right_path):
        self.drive_left: Frame = drive_left
        self.drive_right: Frame = drive_right
        self.label_left_t = label_left_t
        self.label_right_t = label_right_t
        self.label_left_d = label_left_d
        self.label_right_d = label_right_d
        self.listar_l = listar_l
        self.listar_r = listar_r
        self.left_path = left_path
        self.right_path = right_path
        self.photo = []
        self.dict_of_devices = Devices().return_dict()  # Here we return a dictionary of all the devices connected
        imagenes = ["hd_hard", "hd_hard_unmounted", "usb", "usb_unmounted", "movil", "movil_unmounted"]
        for name in imagenes:
            image = Image.open("resources/" + name + ".ico")
            image.thumbnail((20, 20), Image.ANTIALIAS)
            self.photo.append(ImageTk.PhotoImage(image))

        self.start()
        self.monitoring()

    def get_disponible(self, path):
        name = self.find_sdiskpart(path).device
        df = os.popen("df -h " + name)
        i = 0
        while i < 2:
            line = df.readline()
            if i == 1:
                return line.split()[0:4][3]
            i = i + 1

    @staticmethod
    def find_sdiskpart(path):
        path = os.path.abspath(path)
        while not os.path.ismount(path):
            path = os.path.dirname(path)
        p = [p for p in psutil.disk_partitions(all=True) if p.mountpoint == path.__str__()]

        if len(p) == 1:
            return p[0]

        raise psutil.Error

    def get_size(self, path):
        name = self.find_sdiskpart(path).device
        df = os.popen("df -h " + name)
        i = 0
        while i < 2:
            line = df.readline()
            if i == 1:
                return line.split()[0:2][1]
            i = i + 1

    def listar_movile(self, path, left=True):
        if left:
            self.listar_l.listar(self.left_path, "", path)
        else:
            self.listar_r.listar(self.right_path, "", path)

    def listar_(self, path, left=True):
        size = str(self.get_size(path))
        disponible = self.get_disponible(path)
        if left:
            self.label_left_t.config(text="Tamaño: " + size)
            self.label_left_d.config(text="Libre: " + disponible)
            self.listar_l.listar(self.left_path, "", path)
        else:
            self.label_right_t.config(text="Tamaño: " + size)
            self.label_right_d.config(text="Libre: " + disponible)
            self.listar_r.listar(self.right_path, "", path)

    def list_or_mount(self, name, left=True):
        device = self.dict_of_devices[name]
        if device[5] != "":
            if device[3] == "movil":
                self.listar_movile(device[5], left)
            else:
                self.listar_(device[5], left)
        else:
            self.mount_(device, name, left)

    def start(self):
        for index, name in enumerate(self.dict_of_devices):  # We iterate in this dictionary
            fram_l = Frame(self.drive_left, bg=soft_gray)  # Create the frames
            fram_r = Frame(self.drive_right, bg=soft_gray)

            fram_l.grid(row=0, column=index)  # Pack the frames
            fram_r.grid(row=0, column=index)

            device = self.dict_of_devices[name]
            alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                        "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

            mounted = False
            tipo = device[3]  # Here we get the type (The Bus system)
            if device[5] != "":
                mounted = True
            image = self.photo[self.get_image(tipo, mounted)]
            button_l = Button(fram_l, image=image, bg=soft_gray, bd=0, highlightthickness=0, takefocus=False)
            button_r = Button(fram_r, image=image, bg=soft_gray, bd=0, highlightthickness=0, takefocus=False)

            button_l.bind("<Button-1>", lambda event, n=name: self.list_or_mount(n))
            button_l.bind("<Button-3>", lambda event, n=name: self.add_menu(event, n))
            button_r.bind("<Button-1>", lambda event, i=False, n=name: self.list_or_mount(n, i))
            button_r.bind("<Button-3>", lambda event, n=name: self.add_menu(event, n, False))
            button_l.grid(row=0, column=0)
            button_r.grid(row=0, column=0)
            label_l = Label(fram_l, text=str(alphabet[index]), bg=soft_gray, takefocus=False)
            label_r = Label(fram_r, text=str(alphabet[index]), bg=soft_gray, takefocus=False)
            label_l.grid(row=0, column=1)
            label_r.grid(row=0, column=1)

    def add_menu(self, event, name, left=True):
        device = self.dict_of_devices[name]
        boton: Button = event.widget
        menu = Menu(master=boton, tearoff=False, relief=FLAT, bd=9, bg=dark_gray,
                    fg="white", activeforeground="green", activebackground=dark_gray)

        menu.add_command(label="Desmontar", command=lambda e, dev=device: self.umount(dev, name, left))
        if device[3] == 'usb':
            menu.add_command(label="Expulsar", command=lambda e, dev=device: self.eject(dev, name))

        menu.tk_popup(event.x_root, event.y_root)

    @staticmethod
    def get_image(tipo, mounted):
        image = 0
        if tipo == "ata":
            if not mounted:
                image = 1
        elif tipo == "usb":
            if mounted:
                image = 2
            else:
                image = 3
        elif tipo == "movil":
            if mounted:
                image = 4
            else:
                image = 5
        return image

    def eject(self, device, name):
        print(device)
        full_name = device[6]
        try:
            os.system("pkexec eject " + full_name)
            del self.dict_of_devices[name]
            self.drive_left.winfo_children()[device[0]].destroy()
            self.drive_right.winfo_children()[device[0]].destroy()
            if device[5] in vars.actual_left_path:
                self.listar_(os.getenv("HOME"), True)
            if device[5] in vars.actual_right_path:
                self.listar_(os.getenv("HOME"), False)
        except Exception as e:
            print("eject function " + str(e))

    def umount(self, device, name, left):
        full_name = device[6]
        try:
            os.system("pkexec umount " + full_name)
            self.dict_of_devices[name][5] = ""
            self.drive_left.winfo_children()[device[0]].winfo_children()[0].config(
                image=self.photo[self.get_image(device[3], False)])
            self.drive_right.winfo_children()[device[0]].winfo_children()[0].config(
                image=self.photo[self.get_image(device[3], False)])
            if left:
                if os.path.exists(vars.actual_left_path):
                    self.listar_(vars.actual_left_path, left)
                else:
                    self.listar_(os.getenv("HOME", left))
            else:
                if os.path.exists(vars.actual_right_path):
                    self.listar_(vars.actual_right_path, left)
                else:
                    self.listar_(os.getenv("HOME"), left)

        except Exception as e:
            print("umount function " + str(e))

    def mount_(self, device, name, left):
        full_name = device[6]
        print(device)
        print("mounting... ")
        user = os.getenv("USER")
        mount_point = os.path.join("/media", user)
        if device[4] != "":
            new = os.path.join(mount_point, device[4])
        else:
            new = os.path.join(mount_point, name)
        try:
            os.system("pkexec sh -c 'mkdir -p " + new + " && mount " + full_name + " " + new + "'")
            self.dict_of_devices[name][5] = new
            print("Device " + name + " mounted at " + new)
            self.drive_left.winfo_children()[device[0]].winfo_children()[0].config(
                image=self.photo[self.get_image(device[3], True)])
            self.drive_right.winfo_children()[device[0]].winfo_children()[0].config(
                image=self.photo[self.get_image(device[3], True)])
            self.listar_(new, left)

        except Exception as e:
            print("mount_ function " + str(e))

    def monitoring(self):
        pass
