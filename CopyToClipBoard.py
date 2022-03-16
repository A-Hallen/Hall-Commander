from gi import require_version

import vars

require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class CopyToClipBoard:
    def __init__(self, text=True, file=None):
        pass

    def copyfile(self, text_array: list):
        vars.portapapeles = []
        for i in text_array:
            vars.portapapeles.append(i)
        return vars.portapapeles

    def copy_text(self, text):
        cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        cb.set_text(text, -1)
        cb.store()

    # On linux with gtk
    def paste_text(self):
        clipboardContents = Gtk.Clipboard().wait_for_text()
        # for python 2, returns None if the clipboard is blank.
        if clipboardContents is None:
            return ''
        else:
            return clipboardContents
