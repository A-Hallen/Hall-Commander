import os.path
import threading

import PIL
from PIL import ImageTk, Image
from moviepy.video.io.VideoFileClip import VideoFileClip

import vars


def get_file_icon(path, ext):
    photos = [".jpg", ".png", ".jpeg", ".ico", ".icon"]
    videos = [".mp4", ".mpg", ".avi", ".rmvb", ".webm", ".mkv"]
    audio = [".mp3"]
    if ext in photos:
        try:
            image = Image.open (path)
        except PIL.UnidentifiedImageError:
            image = Image.open ("resources/fotos.png")
    else:
        if ext == "":
            image = Image.open ("folder.png")
        else:
            image = Image.open ("desconocido.png")

    image.thumbnail ((30, 30), Image.ANTIALIAS)
    blank = Image.new ('RGBA', (36, 30))
    blank.paste (image)
    return ImageTk.PhotoImage (blank)


class Load_Thumb:
    def __init__(self, tree, actual: str, array: list):
        self.tree = tree
        self.actual = actual
        self.array = array
        self.stop = threading.Event ()

    def stop_thread(self):
        self.stop.set ()

    def clear(self):
        self.stop.clear ()

    def start(self):
        self.thumb_thread = threading.Thread (target=self.load_async)
        self.thumb_thread.daemon = True
        self.thumb_thread.start ()

    def load_async(self):
        photos = [".jpg", ".png", ".jpeg", ".ico"]
        videos = [".mp4", ".mpg", ".avi", ".rmvb", ".webm", ".mkv"]
        audio = [".mp3"]

        childrens = self.tree.get_children ()

        for item in childrens:
            if not self.stop.is_set():
                try:
                    ext = self.tree.item(item, "values")[0]
                except:
                    ext = ""
                    print("exception in line 61 get_file_icon")
                try:
                    global name
                    global path
                    name = self.tree.item(item, "text")
                    path = os.path.join(self.actual, name + ext)
                except:
                    print("exception in line 71 get_file_icon")
                    continue
                if ext.lower() in photos:
                    try:
                        image = Image.open(path)
                    except PIL.UnidentifiedImageError:
                        image = Image.open("resources/fotos.png")

                    if vars.hidden == False:
                        if name.startswith("."):
                            image.putalpha(100)
                    image.thumbnail((30, 30), Image.ANTIALIAS)
                    blank = Image.new ('RGBA', (36, 30))
                    blank.paste (image)

                    self.array.insert (int (item), ImageTk.PhotoImage (blank))
                    try:
                        self.tree.item (item, image=self.array[int (item)])
                    except:
                        print ("item in exception" + item)
                elif ext.lower () in videos:
                    clips = VideoFileClip (path)
                    duration = clips.duration
                    max_duration = int (duration) + 1
                    i = max_duration // 2
                    frame = clips.get_frame(i)
                    image = Image.fromarray(frame)
                    image.thumbnail((30, 30), Image.ANTIALIAS)
                    blank = Image.new('RGBA', (36, 30))
                    blank.paste(image)
                    if vars.hidden == False:
                        if name.startswith("."):
                            blank.putalpha(100)
                    imagen = ImageTk.PhotoImage(blank)
                    self.array.insert(int(item), imagen)
                    try:
                        self.tree.item(item, image=self.array[int(item)])
                    except IndexError:
                        print("line 98, index out of range get_file_icon")
                    except:
                        print("line 107, error unknown get_file_icon")

                else:
                    self.array.insert (int (item), "")
