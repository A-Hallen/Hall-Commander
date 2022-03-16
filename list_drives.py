import glob
import os.path
from tkinter import Frame, Button, Label

import psutil

from vars import soft_gray


class Drives:
    def __init__(self, drive_left, drive_rigth, photo, label_left_t,
                 label_right_t, label_left_d, label_right_d,
                 listar_l, listar_r, left_path, right_path):

        self.label_left_t = label_left_t
        self.label_right_t = label_right_t
        self.label_right_d = label_right_d
        self.label_left_d = label_left_d
        self.listar_l = listar_l
        self.listar_r = listar_r
        self.left_path = left_path
        self.right_path = right_path
        self.photo = photo
        self.drive_left = drive_left
        self.drive_right = drive_rigth

        self.all_block_devices = set(
            self.linux_block_devices()
        )
        self.used_block_devices = set(
            (str(p) for p in psutil.disk_partitions())
        )
        self.unused_block_devices = self.all_block_devices - self.used_block_devices

        used = psutil.disk_partitions()
        self.listar(used)
        self.listar_unused(self.unused_block_devices)

    def listar_unused(self, path):
        pass

    def get_size(self, path):
        name = self.find_sdiskpart(path).device
        df = os.popen("df -h " + name)
        i = 0
        while i < 2:
            line = df.readline()
            if i == 1:
                return line.split()[0:2][1]
            i = i + 1

    def get_disponible(self, path):
        name = self.find_sdiskpart(path).device
        df = os.popen("df -h " + name)
        i = 0
        while i < 2:
            line = df.readline()
            if i == 1:
                return line.split()[0:4][3]
            i = i + 1

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

    @staticmethod
    def find_sdiskpart(path):
        path = os.path.abspath(path)
        while not os.path.ismount(path):
            path = os.path.dirname(path)
        p = [p for p in psutil.disk_partitions(all=True) if p.mountpoint == path.__str__()]

        if len(p) == 1:
            return p[0]

        raise psutil.Error

    @staticmethod
    def get_type(name):
        df = os.popen("lsblk -do name,rm,tran")

        for lines in df.readlines():
            split = lines.split()[0:3]
            name_ = "/dev/" + split[0] + split[1]
            if name_ == name:
                return split[2]

    def listar(self, partitions):
        for p in range(len(partitions)):
            fram_l = Frame(self.drive_left, bg=soft_gray)
            fram_r = Frame(self.drive_right, bg=soft_gray)

            fram_l.grid(row=0, column=p)
            fram_r.grid(row=0, column=p)
            name = self.find_sdiskpart(partitions[p].mountpoint).device
            type = self.get_type(name)
            if type == "usb":
                image = self.photo[1]
            else:
                image = self.photo[0]

            alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                        "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

            button_l = Button(fram_l, image=image, bg=soft_gray, bd=0, highlightthickness=0, takefocus=False,
                              command=lambda path=partitions[p].mountpoint: self.listar_(path))
            button_r = Button(fram_r, image=image, bg=soft_gray, bd=0, highlightthickness=0, takefocus=False,
                              command=lambda path=partitions[p].mountpoint: self.listar_(path, False))
            button_l.grid(row=0, column=0)
            button_r.grid(row=0, column=0)
            label_l = Label(fram_l, text=str(alphabet[p]), bg=soft_gray, takefocus=False)
            label_r = Label(fram_r, text=str(alphabet[p]), bg=soft_gray, takefocus=False)
            label_l.grid(row=0, column=1)
            label_r.grid(row=0, column=1)

    @staticmethod
    def linux_block_devices():
        for blockdev_stat in glob.glob('/sys/block/*/stat'):
            blockdev_dir = blockdev_stat.rsplit('/', 1)[0]
            found_parts = False
            for _ in glob.glob(blockdev_dir + '/*/stat'):
                yield blockdev_stat.rsplit('/', 2)[-2]
                found_parts = True
            if not found_parts:
                yield blockdev_dir.rsplit('/', 1)[-1]

    @staticmethod
    def get_used_block_devices():
        used_block_devices = set(
            (p.device.replace('/dev/', '') for p in psutil.disk_partitions())
        )
        return used_block_devices
