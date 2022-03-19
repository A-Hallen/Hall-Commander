import os.path
import threading
import time
from io import BytesIO

import PIL
from PIL import ImageTk, Image
from cairosvg import svg2png
from gi.repository import Gio, Gtk
from moviepy.video.io.VideoFileClip import VideoFileClip

import vars


def get_file_icon(path, ext):
    photos = [".jpg", ".png", ".jpeg", ".ico", ".icon"]
    if ext in photos:
        try:
            image = Image.open(path)
        except PIL.UnidentifiedImageError:
            image = Image.open("resources/fotos.png")
    else:
        if ext == "":
            image = Image.open("folder.png")
        else:
            image = Image.open("desconocido.png")

    image.thumbnail((30, 30), Image.ANTIALIAS)
    blank = Image.new('RGBA', (36, 30))
    blank.paste(image)
    return ImageTk.PhotoImage(blank)


class Load_Thumb:
    def __init__(self, tree, actual: str, array: list):
        self.thumb_thread = None
        self.tree = tree
        self.actual = actual
        self.array = array
        self.stop = threading.Event()

    def stop_thread(self):
        self.stop.set()

    def clear(self):
        self.stop.clear()

    def start(self):
        self.thumb_thread = threading.Thread(target=self.load_async)
        self.thumb_thread.daemon = True
        self.thumb_thread.start()

    def load_def(self, path, photos, item):
        img = self.load_default(path, photos)
        if img:
            self.array.insert(int(item), img)
            try:
                self.tree.item(item, image=self.array[int(item)])
            except IndexError:
                print("line 148, index out of range get_file_icon")
            except:
                print("line 150, error unknown get_file_icon")
        else:
            self.array.insert(int(item), "")

    @staticmethod
    def load_default(path, photos):
        file = Gio.File.new_for_path(path)
        file_info = file.query_info('standard::icon', 0)
        file_icon = file_info.get_icon().get_names()[0]
        icon_theme = Gtk.IconTheme.get_default()
        icon_filename = icon_theme.lookup_icon(file_icon, 32, 0)
        final_filename = ""
        if icon_filename is not None:
            final_filename = icon_filename.get_filename()
        if os.path.splitext(final_filename)[1].lower() in photos:
            imagen = Image.open(final_filename)
            imagen.thumbnail((30, 30), Image.ANTIALIAS)
            return ImageTk.PhotoImage(imagen)

        else:
            return None

    def load_async(self):
        photos = [".jpg", ".png", ".jpeg", ".ico"]
        videos = [".mp4", ".mpg", ".avi", ".rmvb", ".webm", ".mkv"]
        img_ext = [".apk", ".zip", ".exe", ".rar", ".tar", ".tgz", ".gz"]
        imagenes = ["android.png", "zip.ico", "exe.png", "rar.ico", "tar3.ico", "tgz2.ico", "tgz2.ico"]
        music = ['pcm', 'wav', 'aiff', 'mp3', 'aac', 'ogg', 'wma', 'flac', 'alac', 'wma']

        while True:
            try:
                childrens = self.tree.get_children()
                break
            except RuntimeError:
                time.sleep(0.01)

        for item in childrens:
            if not self.stop.is_set():
                try:
                    ext = self.tree.item(item, "values")[0]
                except:
                    ext = ""
                    print("exception in line 66 get_file_icon")
                try:
                    name = self.tree.item(item, "text")
                    path = os.path.join(self.actual, name + ext)
                except:
                    print("exception in line 71 get_file_icon")
                    continue
                if ext.lower() in photos:
                    try:
                        image = Image.open(path)
                    except (PIL.UnidentifiedImageError, FileNotFoundError):
                        image = Image.open("resources/fotos.png")

                    if not vars.hidden:
                        if name.startswith("."):
                            image.putalpha(100)
                    image.thumbnail((30, 30), Image.ANTIALIAS)
                    blank = Image.new('RGBA', (36, 30))
                    blank.paste(image)

                    self.array.insert(int(item), ImageTk.PhotoImage(blank))
                    try:
                        self.tree.item(item, image=self.array[int(item)])
                    except:
                        print("item in exception" + item)
                elif ext.lower() in videos:
                    try:
                        clips = VideoFileClip(path)
                        duration = clips.duration
                        max_duration = int(duration) + 1
                        i = max_duration // 2
                        frame = clips.get_frame(i)
                        image = Image.fromarray(frame)
                    except UnicodeDecodeError:
                        image = Image.open("resources/video.ico")

                    image.thumbnail((30, 30), Image.ANTIALIAS)
                    blank = Image.new('RGBA', (36, 30))
                    blank.paste(image)
                    if not vars.hidden:
                        if name.startswith("."):
                            blank.putalpha(100)
                    imagen = ImageTk.PhotoImage(blank)
                    self.array.insert(int(item), imagen)
                    try:
                        self.tree.item(item, image=self.array[int(item)])
                    except IndexError:
                        print("line 111, index out of range get_file_icon")
                    except:
                        print("line 113, error unknown get_file_icon")
                elif ext.lower() == ".desktop":
                    try:
                        app = Gio.DesktopAppInfo.new_from_filename(path)
                        icon_name = app.get_string("Icon")
                        icon_theme = Gtk.IconTheme.get_default()
                        icon = icon_theme.lookup_icon(icon_name, 32, 0)
                        if icon:
                            icon_path = icon.get_filename()
                            if os.path.splitext(icon_path)[1].lower() in photos:
                                try:
                                    image = Image.open(icon_path)
                                    image.thumbnail((30, 30), Image.ANTIALIAS)
                                    self.array.insert(int(item), ImageTk.PhotoImage(image))
                                    self.tree.item(item, image=self.array[int(item)])
                                except PIL.UnidentifiedImageError:
                                    self.load_def(path, photos, item)
                            elif os.path.splitext(icon_path)[1].lower() == ".svg":
                                png = svg2png(url=icon_path)
                                image = Image.open(BytesIO(png))
                                image.thumbnail((30, 30), Image.ANTIALIAS)
                                self.array.insert(int(item), ImageTk.PhotoImage(image))
                                self.tree.item(item, image=self.array[int(item)])
                            else:
                                self.load_def(path, photos, item)
                        else:
                            icon_path = icon_name
                            if os.path.splitext(icon_path)[1].lower() in photos:
                                try:
                                    image = Image.open(icon_path)
                                    image.thumbnail((30, 30), Image.ANTIALIAS)
                                    self.array.insert(int(item), ImageTk.PhotoImage(image))
                                    self.tree.item(item, image=self.array[int(item)])
                                except PIL.UnidentifiedImageError:
                                    self.load_def(path, photos, item)
                            elif os.path.splitext(icon_path)[1].lower() == ".svg":
                                png = svg2png(url=icon_path)
                                image = Image.open(BytesIO(png))
                                image.thumbnail((30, 30), Image.ANTIALIAS)
                                self.array.insert(int(item), ImageTk.PhotoImage(image))
                                self.tree.item(item, image=self.array[int(item)])
                            else:
                                self.load_def(path, photos, item)
                            self.load_def(path, photos, item)
                    except TypeError:
                        self.load_def(path, photos, item)

                elif ext.lower() == ".svg":
                    try:
                        png = svg2png(url=path)
                        image = Image.open(BytesIO(png))
                    except PIL.UnidentifiedImageError:
                        image = Image.open("resources/fotos.png")
                    image.thumbnail((30, 30), Image.ANTIALIAS)
                    self.array.insert(int(item), ImageTk.PhotoImage(image))
                    self.tree.item(item, image=self.array[int(item)])
                elif ext.lower() in img_ext:
                    index = img_ext.index(ext.lower())
                    img = imagenes[index]
                    image = Image.open("resources/" + img)
                    image.thumbnail((30, 30), Image.ANTIALIAS)
                    self.array.insert(int(item), ImageTk.PhotoImage(image))
                    self.tree.item(item, image=self.array[int(item)])
                elif not os.path.isdir(path):
                    self.load_def(path, photos, item)
                else:
                    self.array.insert(int(item), "")
