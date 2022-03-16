def getting_frame_focus(frame_left, frame_right):
    if not frame_left.focus_displayof():
        if not frame_right.focus_displayof():
            return frame_right
        else:
            return frame_right
    else:
        return frame_left


def image(path: str, thumb=(0, 0)):
    from PIL import Image, ImageTk

    imagen = Image.open(path)
    if thumb != (0, 0):
        imagen.thumbnail(thumb, Image.ANTIALIAS)

    photo = ImageTk.PhotoImage(imagen)
    return photo
