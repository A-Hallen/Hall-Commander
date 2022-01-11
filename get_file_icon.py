import os.path
import threading

import PIL
from PIL import ImageTk, Image
from moviepy.video.io.VideoFileClip import VideoFileClip


def get_file_icon(path, ext):
    photos = [".jpg", ".png", ".jpeg", ".ico"]
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
            if not self.stop.is_set ():
                # print("\rExecution " + item + "\r", end="_"+item+"_")
                ext = self.tree.item (item, "values")[0]
                name = self.tree.item (item, "text")
                path = os.path.join (self.actual, name + ext)
                if ext.lower () in photos:
                    try:
                        image = Image.open (path)
                    except PIL.UnidentifiedImageError:
                        image = Image.open ("resources/fotos.png")

                    image.thumbnail ((30, 30), Image.ANTIALIAS)
                    blank = Image.new ('RGBA', (36, 30))
                    blank.paste (image)

                    self.array.insert (int (item), ImageTk.PhotoImage (blank))
                    try:
                        self.tree.item (item, image=self.array[int (item)])
                    except:
                        print ("item in exception" + item)
                elif ext.lower () in videos:
                    clips = VideoFileClip (path)
                    frames = clips.reader.fps
                    duration = clips.duration
                    max_duration = int (duration) + 1
                    i = max_duration // 2
                    frame = clips.get_frame (i)
                    image = Image.fromarray (frame)
                    image.thumbnail ((30, 30), Image.ANTIALIAS)
                    blank = Image.new ('RGBA', (36, 30))
                    blank.paste (image)
                    imagen = ImageTk.PhotoImage (blank)
                    self.array.insert (int (item), imagen)
                    self.tree.item (item, image=self.array[int (item)])

                else:
                    self.array.insert (int (item), "")
