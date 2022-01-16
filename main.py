import io
import json
import os.path
import string
import sys
from tkinter import *
from tkinter import ttk

import PIL.Image
import cairosvg as cairosvg
import gi
import magic
import psutil
from PIL import ImageTk
from blkinfo import BlkDiskInfo
from gi.repository import Gio, Gtk

import SearchWindow
import vars
from CopyToClipBoard import CopyToClipBoard
from FileManipulation import FileManipulation
from MyDialog import CopyDialog
from actualizar import Actualizar
from center_frame import VerticalBarCommands
from get_file_icon import Load_Thumb
from list_files import ListFiles
from listar import Listar
from menu_bar import _Menu
from search_tree import Search
from tree_view import TreeViewlist

gi.require_version ('Gtk', '3.0')


# Name of the app
# Cargar el archivo que tiene todas las configuraciones necesarias

# the firt function we execute
def start():
    prefs = open ("preferences.json", "r")
    read_prefs = prefs.read ()
    json_read = json.loads (read_prefs)
    prefs.close ()
    actualleft = json_read["lasts_windows"]["left"]
    actualright = json_read["lasts_windows"]["right"]
    if os.path.exists (actualleft) and os.path.isdir (actualleft):
        vars.actual_left_path = actualleft
    if os.path.exists (actualright) and os.path.isdir (actualright):
        vars.actual_right_path = actualright
    vars.hidden = json_read["hidden"][0]


start ()
# Set the root window
from vertical_bar import VerticalBar

root = Tk ()
root.title (vars.name_of_the_app)
root.geometry ("800x500")

# The menu of the app
menus = _Menu (root, vars.name_of_the_app)

# The root config
root.config (bg="black", menu=menus.menu)

# The main frame of the window
frame = Frame ()
frame.configure (bg=vars.color_of_side_frames, takefocus=False)
frame.pack (expand=True, fill=BOTH)
tool_bar = Frame (frame, height=30, bg=vars.soft_gray, takefocus=False)
tool_bar.pack (fill="x")
# The left frame of the app

left_frame = Frame (frame)
left_frame.config (bg=vars.color_of_side_frames, bd=2, takefocus=False)
left_frame.pack_propagate (False)
left_frame.pack (fill=BOTH, expand=True, side=LEFT)

drive_bar_left = Frame (left_frame)
drive_bar_left.config (bg=vars.soft_gray, height=22, takefocus=False)
drive_bar_left.pack (fill="x")
drive_bar_left.grid_propagate (False)
drive_left = Frame (drive_bar_left, bg=vars.soft_gray)
drive_left.grid (row=0, column=0)

# Adding the left top lavel for the path information
left_path = Label (master=left_frame, anchor=W, bg=vars.gray, fg="white", takefocus=False)
left_path.configure (padx=10, text=vars.actual_left_path, width=1)
left_path.pack (fill="x")

# The right frame of the app
right_frame = Frame (frame)
right_frame.pack_propagate (False)
right_frame.config (bg=vars.color_of_side_frames, bd=2, takefocus=False)
right_frame.pack (fill=BOTH, expand=True, side=RIGHT)

drive_bar_right = Frame (right_frame)
drive_bar_right.config (bg=vars.soft_gray, height=22, takefocus=False)
drive_bar_right.pack (fill="x")
drive_bar_right.grid_propagate (False)
drive_right = Frame (drive_bar_right, bg=vars.soft_gray)
drive_right.grid (row=0, column=0)

# Adding the left top lavel for the path information
right_path = Label (right_frame, anchor=W, bg=vars.gray, fg="white")
right_path.configure (padx=10, text=vars.actual_right_path, width=1, takefocus=False)
right_path.pack (fill="x")

center_frame = Frame (frame)
center_frame.config (bg=vars.soft_gray, width=35, takefocus=False, highlightthickness=1,
                     highlightbackground=vars.soft_gray)
center_frame.pack (fill="y", expand=True)

# The tool bar
tool_bar = Frame (root)
tool_bar.config (bg="black", height=25, bd=1, takefocus=False)
tool_bar.pack (fill="x")
# Adding items to toolbar

tool_bar.columnconfigure (0, weight=1)
tool_bar.columnconfigure (1, weight=1)
tool_bar.columnconfigure (2, weight=1)
tool_bar.columnconfigure (3, weight=1)
tool_bar.columnconfigure (4, weight=1)
Label (center_frame, height=3, width=4, bg=vars.soft_gray, takefocus=False).grid (row=0, column=0)

# The tree  view
left_frame_list = TreeViewlist (left_frame)
right_frame_list = TreeViewlist (right_frame)
# left_frame_list.add_data(data)


# Initialized the reading of the data
leftlistfiles = ListFiles ()
lista_l = leftlistfiles.list (vars.actual_left_path)
left_frame_list.add_data (lista_l)
array_images_left = []
left_thumb_thread = Load_Thumb (left_frame_list.tree, vars.actual_left_path, array_images_left)
left_thumb_thread.start ()
# Inicializamos la clase listar para el frame izquierdo
listar_l = Listar (True, left_frame_list, left_thumb_thread)

item_left_text = ""


def listar_left(event):
    global item_left_text
    item_left = left_frame_list.tree.selection ()[0]  # Identificamos el item que a sido doble clickeado
    item_left_text = left_frame_list.tree.item (item_left, "text") + left_frame_list.tree.item (item_left, "values")[
        0]  # Extraemos el texto que poseee ese item
    if item_left_text == "":
        return
    path = vars.actual_left_path + "/" + item_left_text  # calculamos su path
    listar_l.listar (left_path, item_left_text, path)


rightlistfiles = ListFiles ()
lista_r = rightlistfiles.list (vars.actual_right_path)
right_frame_list.add_data (lista_r)
array_images_right = []
right_thumb_thread = Load_Thumb (right_frame_list.tree, vars.actual_right_path, array_images_right)
right_thumb_thread.start ()
# Inicializamos la clase listar para el frame derecho
listar_r = Listar (False, right_frame_list, right_thumb_thread)

actualizar = Actualizar (left_path, right_path, listar_r, listar_l)
item_right_text = ""
# =========================------------------===========================----------------------============================#|
file_manipulation = FileManipulation (left_frame_list, right_frame_list, listar_l, listar_r, left_path, right_path,
                                      root, actualizar)  # |


# =========================------------------===========================----------------------============================#|
def create_file():
    if vars.selection_left:
        file_manipulation.folder_dialog (None)
    else:
        file_manipulation.folder_dialog (None, False)


def delete_dialog():
    if vars.selection_left:
        file_manipulation.delete_dialog (None)
    else:
        file_manipulation.delete_dialog ((None, False))


def edit_dialog():
    if vars.selection_left:
        file_manipulation.f2 (None)
    else:
        file_manipulation.f2 (None, False)


def copiar():
    if vars.selection_left:
        file_manipulation.copy_dialog (None)
    else:
        file_manipulation.copy_dialog (None, False)


b_copiar = Button (tool_bar, text="F5 Copiar", height=1, width=0,
                   bd=0, command=copiar, padx=20, bg="black", fg="white", takefocus=False)
b_copiar.grid (row=0, column=1, sticky='nsew', rowspan=2)

b_mover = Button (tool_bar, text="F6 Mover", height=1, width=0, bd=0, padx=20, bg="black", fg="white", takefocus=False)
b_mover.grid (row=0, column=2, sticky='nsew', rowspan=2)

b_editar = Button (tool_bar, text="F2 Renombrar", height=1, width=0, bd=0, padx=20, bg="black",
                   fg="white", takefocus=False, command=edit_dialog)
b_editar.grid (row=0, column=0, sticky='nsew', rowspan=1)

b_eliminar = Button (tool_bar, text="F8 Delete", height=1, width=0, bd=0, padx=20, bg="black",
                     fg="white", takefocus=False, command=delete_dialog)
b_eliminar.grid (row=0, column=4, sticky='nsew', rowspan=2)

b_new_folder = Button (tool_bar, text="F7 Nueva Carpeta", height=1, width=0,
                       bd=0, padx=20, bg="black", fg="white", takefocus=False, command=create_file)
b_new_folder.grid (row=0, column=3, sticky='nsew', rowspan=2)


# =========================------------------===========================----------------------==========================

def listar_right(event):
    global item_right_text
    item_right = right_frame_list.tree.selection ()[0]  # Identificamos el item que a sido doble clickeado
    item_right_text = right_frame_list.tree.item (item_right, "text") + \
                      right_frame_list.tree.item (item_right, "values")[0]  # Extraemos el texto que posee ese item
    if item_right_text == "":
        return
    path = vars.actual_right_path + "/" + item_right_text  # calculamos su path
    listar_r.listar (right_path, item_right_text, path)


def edit(path, actual_path, left):
    label_edit = ttk.Entry (path)
    label_edit.pack (fill="x")
    label_edit.insert (0, actual_path)
    label_edit.focus ()
    label_edit.select_range (0, "end")

    def edit_destroy(event):
        label_edit.destroy ()
        label_edit.update ()

    label_edit.bind ("<FocusOut>", edit_destroy)
    text = ""

    def edit_enter(event):
        global text
        text = label_edit.get ()
        if left == True:
            listar_l.listar (path, "", text)
        else:
            listar_r.listar (path, "", text)

    label_edit.bind ("<Return>", edit_enter)


# Here we handle the littel edit at top of the two frames
def edit_left(event):
    edit (left_path, vars.actual_left_path, True)


# Here we handle the little edit at top right
def edit_right(event):
    edit (right_path, vars.actual_right_path, False)


# -------------------------------------===========================================--------------------------------------
vertical_bar = VerticalBar (center_frame, True, listar_r, listar_l, left_path, right_path)


def click_center(event):
    vertical_bar.start (event)


center_frame.bind ("<ButtonPress-3>", click_center)
# -------------------------------------Initialize the images of the central frame----------------------------------------
vertical_bar_commands = VerticalBarCommands (center_frame, listar_r, listar_l, left_path, right_path)
vertical_bar_commands.command ()


# -------------------------------------===========================================--------------------------------------
def change_left(event):
    vars.selection_left = True
    vars.last_selection_right = right_frame_list.tree.focus ()
    right_frame_list.tree.item (right_frame_list.tree.focus (), tags="odd")
    left_frame_list.tree.item (vars.last_selection_left, tags="")
    right_frame_list.tree.selection_remove (*right_frame_list.tree.get_children ())


def change_right(event):
    vars.selection_left = False
    vars.last_selection_left = left_frame_list.tree.focus ()
    left_frame_list.tree.item (left_frame_list.tree.focus (), tags="odd")
    right_frame_list.tree.item (vars.last_selection_right, tags="")
    left_frame_list.tree.selection_remove (*left_frame_list.tree.get_children ())


def tab(event, left=True):
    if left:
        a = left_frame_list.tree.focus ()
        vars.selection_left = False
        if vars.last_selection_right == "":
            vars.last_selection_right = 0
        right_frame_list.tree.selection_add (vars.last_selection_right)
        right_frame_list.tree.focus (vars.last_selection_right)
        change_right (event)
    else:
        vars.selection_left = True
        if vars.last_selection_left == "":
            vars.last_selection_left = 0
        left_frame_list.tree.selection_add (vars.last_selection_left)
        left_frame_list.tree.focus (vars.last_selection_left)
        change_left (event)


def back_space(event, left=True):
    if left:
        listar_l.listar (left_path, "..", vars.actual_left_path + "/..")
    else:
        listar_r.listar (right_path, "..", vars.actual_right_path + "/..")


# Here we initialize the images of menus
image_array = []
image_array.insert (0, PIL.ImageTk.PhotoImage
(PIL.Image.open ("resources/borrar.png").resize ((24, 24), PIL.Image.ANTIALIAS)))
image_array.insert (1, PIL.ImageTk.PhotoImage
(PIL.Image.open ("resources/cortar.png").resize ((24, 24), PIL.Image.ANTIALIAS)))
image_array.insert (2, PIL.ImageTk.PhotoImage
(PIL.Image.open ("resources/copiar.png").resize ((24, 24), PIL.Image.ANTIALIAS)))
image_array.insert (3, PIL.ImageTk.PhotoImage
(PIL.Image.open ("resources/propiedades.png").resize ((24, 24), PIL.Image.ANTIALIAS)))
image_array.insert (4, PIL.ImageTk.PhotoImage
(PIL.Image.open ("resources/paste.ico").resize ((24, 24), PIL.Image.ANTIALIAS)))

program_icon_array = []


def start_m(event, frame, actual):
    """
    this function starts the frame context menus

    :param event: the event
    :param frame: the frame in wich we want to inherit
    :return:
    """
    tree: ttk.Treeview = event.widget
    item = tree.identify ("item", event.x, event.y)
    # Initialize the images

    image = tree.item (item, "image")

    menu = Menu (frame, tearoff=False, relief=FLAT, bd=9, bg=vars.dark_gray,
                 fg="white", activeforeground="green", activebackground=vars.dark_gray)
    if item == "":
        print ("This is not any item")
    else:
        name = tree.item (item, "text")
        ext = tree.item (item, "values")[0]
        full_name = name + ext
        mime = magic.Magic (mime=True)
        path = os.path.join (actual, full_name)
        if os.path.isdir (path):
            menu.add_command (label="Abrir carpeta")
        else:
            mime = mime.from_file (path)
            open_with = Menu (menu, tearoff=False, bd=9, relief=FLAT, activeforeground="green",
                              bg=vars.dark_gray, fg="white", activebackground=vars.dark_gray)

            # mounts = Gio.unix_mount_points_get()

            # This is the function that launchs the files
            def launch_program(program):
                item_list = tree.selection ()
                path_list = []
                for i in item_list:
                    _path = os.path.join (actual, tree.item (i, "text") + tree.item (i, "values")[0])
                    path_list.append (Gio.File.new_for_path (_path))
                program.launch (path_list)

            l = Gio.app_info_get_recommended_for_type (mime)
            for e in range (len (l)):
                app = l[e]
                icon = app.get_icon ()
                icon_theme = Gtk.IconTheme.get_default ()
                icon_file = icon_theme.lookup_icon (icon.to_string (), 32, 0)
                final_filename = ""
                if icon_file != None:
                    final_filename = icon_file.get_filename ()

                try:
                    png = cairosvg.svg2png (url=final_filename)
                    pil_img = PIL.Image.open (io.BytesIO (png))
                    res_pil = pil_img.resize ((30, 30), PIL.Image.ANTIALIAS)
                    pg = ImageTk.PhotoImage (res_pil)
                    program_icon_array.insert (e, pg)
                except:
                    print ("error", final_filename)
                open_with.add_command (image=program_icon_array[e], compound="left", label=app.get_name (),
                                       command=lambda program=app: launch_program (program))
            default = Gio.app_info_get_default_for_type (mime, False)
            image_new = PIL.Image.new ('RGBA', (30, 30))
            image_new = ImageTk.PhotoImage (image_new)

            def copiar():
                selections = []
                paths = tree.selection ()
                for f in paths:
                    item_text = tree.item (f, "text") + tree.item (f, "values")[0]
                    selections.append (os.path.join (actual, item_text))

                CopyToClipBoard ().copyfile (selections)

            def pegar():
                if vars.last_selection_left == True:
                    copy_dialog = CopyDialog (vars.portapapeles, actual, listar_r, left_path, root, actualizar)
                else:
                    copy_dialog = CopyDialog (vars.portapapeles, actual, listar_l, right_path, root, actualizar)

            open_with.add_command (image=image_new, compound="left", label="Abri con otro programa")
            menu.add_command (image=image, compound="left", label="Abrir archivo",
                              command=lambda default=default: launch_program (default))
            menu.add_separator ()
            menu.add_cascade (label="Abrir con", menu=open_with)
            menu.add_separator ()
            menu.add_command (image=image_array[2], compound="left", label="Copiar", command=copiar)
            menu.add_command (image=image_array[1], compound="left", label="Cortar")
            if len (vars.portapapeles) == 0:
                print ("Portapapeles vacio")
            else:
                menu.add_command (image=image_array[4], label="Pegar", command=pegar, compound="left")
            menu.add_command (image=image_array[0], compound="left", label="Eliminar")
            menu.add_command (image=image_array[3], compound="left", label="Propiedades")

        menu.tk_popup (event.x_root, event.y_root)


def function_menu_r(event):
    start_m (event, right_frame, vars.actual_right_path)


def function_menu_l(event):
    start_m (event, right_frame, vars.actual_left_path)


def find_sdiskpart(path):
    path = os.path.abspath (path)
    while not os.path.ismount (path):
        path = os.path.dirname (path)
    p = [p for p in psutil.disk_partitions (all=True) if p.mountpoint == path.__str__ ()]

    if len (p) == 1:
        return p[0]

    raise psutil.Error


def get_device_tipe(mountpoint):
    if 'win' in sys.platform:
        drives = []
        from ctypes import windll
        bitmask = windll.kernel32.GetLogicalDrives ()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append (letter)
                bitmask >>= 1
                return drives
    elif 'linux' in sys.platform:
        myblkd = BlkDiskInfo ()
        filters = {
            'mountpoint': str (mountpoint)
        }

        my_filtered_disks = myblkd.get_disks (filters)
        json_output = json.dumps (my_filtered_disks, indent=4)
        print (json_output)
        name = os.path.abspath (mountpoint)


label_left_t = Label (drive_bar_left, padx=10, takefocus=False, fg=vars.gray, font=('Calibri', 9, 'normal'),
                      bg=vars.soft_gray)
label_left_t.grid (row=0, column=1)
label_left_d = Label (drive_bar_left, padx=10, fg=vars.gray, takefocus=False, font=('Calibri', 9, 'normal'),
                      bg=vars.soft_gray)
label_left_d.grid (row=0, column=2)

label_right_t = Label (drive_bar_right, padx=10, takefocus=False, fg=vars.gray, font=('Calibri', 9, 'normal'),
                       bg=vars.soft_gray)
label_right_t.grid (row=0, column=1)
label_right_d = Label (drive_bar_right, padx=10, fg=vars.gray, takefocus=False, font=('Calibri', 9, 'normal'),
                       bg=vars.soft_gray)
label_right_d.grid (row=0, column=2)


def list_drives(photo):
    # ============

    partitions = psutil.disk_partitions ()
    a = 0

    def get_disponible(path):
        name = find_sdiskpart (path).device
        df = os.popen ("df -h " + name)
        i = 0
        while i < 2:
            line = df.readline ()
            if i == 1:
                return line.split ()[0:4][3]
            i = i + 1

    def get_size(path):
        name = find_sdiskpart (path).device
        df = os.popen ("df -h " + name)
        i = 0
        while i < 2:
            line = df.readline ()
            if i == 1:
                return line.split ()[0:2][1]
            i = i + 1

    def listar(path, left=True):
        get_size (path)
        if left:
            label_left_t.config (text="Tamaño: " + str (get_size (path)))
            label_left_d.config (text="Libre: " + str (get_disponible (path)))
            listar_l.listar (left_path, "", path)
        else:
            label_right_t.config (text="Tamaño: " + str (get_size (path)))
            label_right_d.config (text="Libre: " + str (get_disponible (path)))
            listar_r.listar (right_path, "", path)

    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    def get_type(name):
        df = os.popen ("lsblk -do name,rm,tran")

        for lines in df.readlines ():
            split = lines.split ()[0:3]
            name_ = "/dev/" + split[0] + split[1]
            if name_ == name:
                return split[2]

    for p in range (len (partitions)):
        fram_l = Frame (drive_left, bg=vars.soft_gray)
        fram_r = Frame (drive_right, bg=vars.soft_gray)

        fram_l.grid (row=0, column=p)
        fram_r.grid (row=0, column=p)
        name = find_sdiskpart (partitions[p].mountpoint).device
        type = get_type (name)
        if type == "usb":
            image = photo[1]
        else:
            image = photo[0]

        button_l = Button (fram_l, image=image, bg=vars.soft_gray, bd=0, highlightthickness=0, takefocus=False,
                           command=lambda path=partitions[p].mountpoint: listar (path))
        button_r = Button (fram_r, image=image, bg=vars.soft_gray, bd=0, highlightthickness=0, takefocus=False,
                           command=lambda path=partitions[p].mountpoint: listar (path, False))
        button_l.grid (row=0, column=0)
        button_r.grid (row=0, column=0)
        label_l = Label (fram_l, text=str (alphabet[p]), bg=vars.soft_gray, takefocus=False)
        label_r = Label (fram_r, text=str (alphabet[p]), bg=vars.soft_gray, takefocus=False)
        label_l.grid (row=0, column=1)
        label_r.grid (row=0, column=1)


image_disk = PIL.Image.open ("resources/hd_hard.ico")
img_disk = image_disk.resize ((20, 20), PIL.Image.ANTIALIAS)
image_usb = PIL.Image.open ("resources/usb.ico")
img_usb = image_usb.resize ((20, 20), PIL.Image.ANTIALIAS)
photo = []
photo.append (ImageTk.PhotoImage (img_disk))
photo.append (ImageTk.PhotoImage (img_usb))
list_drives (photo)

left_frame_list.double_click (listar_left)  # Aniadimos la funcion
left_path.bind ("<Double-1>", edit_left)
left_frame_list.click (change_left)
left_frame_list.f2 (file_manipulation.f2)
left_frame_list.tab (tab)
left_frame_list.back_space (back_space)
left_frame_list.right_bind_press (function_menu_l)
left_frame_list.right_bind_release (function_menu_l)
left_frame_list.F7 (file_manipulation.folder_dialog)
left_frame_list.delete (file_manipulation.delete_dialog)
left_frame_list.F5 (file_manipulation.copy_dialog)

right_frame_list.double_click (listar_right)
right_path.bind ("<Double-1>", edit_right)
right_frame_list.click (change_right)
right_frame_list.f2 (lambda event: file_manipulation.f2 (event, False))
right_frame_list.tab (lambda event, left=False: tab (event, left))
right_frame_list.back_space (lambda event, left=False: back_space (event, left))
right_frame_list.right_bind_press (function_menu_r)
right_frame_list.right_bind_release (function_menu_r)
right_frame_list.F7 (lambda event: file_manipulation.folder_dialog (event, False))
right_frame_list.delete (lambda event: file_manipulation.delete_dialog (event, False))
right_frame_list.F5 (lambda event: file_manipulation.copy_dialog (event, False))
hovered_items = 0

image_drag = PIL.Image.open ("folder.ico")
photo_drag = PIL.ImageTk.PhotoImage (image_drag)
canvas_drag = Label (image=photo_drag)

ima = PIL.Image.new ('RGBA', (30, 30))
label = Label (master=center_frame, image=ImageTk.PhotoImage (ima))


def motion_general(event: Event, left=True):
    if left:
        other = right_frame_list.tree
        frame_list = right_frame
    else:
        other = left_frame_list.tree
        frame_list = left_frame

    if event.widget.winfo_containing (event.x_root, event.y_root) != event.widget:
        widget = event.widget
        item = widget.focus ()
        imagen = widget.item (item, "image")
        x = event.x - 30
        y = event.y - 30
        canvas_drag.config (image=imagen)
        canvas_drag.place (in_=widget, x=x, y=y, width=30, height=30)
    global hovered_items
    item_under = other.identify ("item", event.x, event.y)
    if item_under != hovered_items:
        other.item (hovered_items, tags="")
    containing = event.widget.winfo_containing (event.x_root, event.y_root)
    if containing == other:
        frame_list.config (bg="green")
        hovered_items = item_under
        other.item (item_under, tags="even")
        label.grid_forget ()
    elif containing == center_frame:
        row = center_frame.grid_size ()[1]
        label.grid (column=0, row=row, pady=2)
        frame_list.config (bg="black")
    else:
        label.grid_forget ()
        frame_list.config (bg="black")


def droped(event, left=True):
    if left:
        frame_list = right_frame
        other = right_frame_list.tree
        tree = left_frame_list.tree
        actual_source = vars.actual_left_path
        actual_dest = vars.actual_right_path
        listar = listar_r
        label_path = right_path
    else:
        label_path = left_path
        listar = listar_l
        actual_source = vars.actual_right_path
        actual_dest = vars.actual_left_path
        tree = right_frame_list.tree
        other = left_frame_list.tree
        frame_list = left_frame
    canvas_drag.place_forget ()
    frame_list.config (bg="black")
    item_in_drag = tree.selection ()
    other.item (hovered_items, tags="")
    item = other.identify ("item", event.x, event.y)
    containing = event.widget.winfo_containing (event.x_root, event.y_root)

    if containing == other:
        if other.item (item, "text") == "":
            path_item = ""
        else:
            name_item = other.item (item, "text") + other.item (item, "values")[0]
            path_item = os.path.join (actual_dest, name_item)
        items_path = []
        for i in item_in_drag:
            items_path.append (os.path.join (actual_source, tree.item (i, "text") + tree.item (i, "values")[0]))
        if os.path.isdir (path_item):
            destiny = os.path.join (actual_dest, path_item)
        else:
            destiny = actual_dest
        CopyDialog (items_path, destiny, listar, label_path, root, actualizar)
    elif containing == center_frame:
        imagen = tree.item (item_in_drag[0], "image")
        path = os.path.join (actual_source,
                             tree.item (item_in_drag[0], "text") + tree.item (item_in_drag[0], "values")[0])
        vertical_bar.create_link (None, True, path)


right_frame_list.tree.bind ("<ButtonRelease-1>", lambda event: droped (event, False))
right_frame_list.drag (lambda event: motion_general (event, False))
left_frame_list.tree.bind ("<ButtonRelease-1>", droped)
left_frame_list.drag (motion_general)


# Create the entry widget for search actions in panels
def destroy(event, search, left=None, item=0):
    search.serach_tree ("")
    if left != None:
        if left == True:
            left_frame_list.tree.focus_set ()
            left_frame_list.tree.focus (item)
        else:
            right_frame_list.tree.focus_set ()
            right_frame_list.tree.focus (item)
    event.widget.pack_forget ()


def b_(event, search_tree):
    entry = event.widget
    text = entry.get ()
    search_tree.serach_tree (text)


entry_search_right = Entry (right_frame, bg="black", fg="white", takefocus=False, insertbackground="white")


def a(event):
    if event.char == "":
        return
    key = event.char
    search_tree = Search (right_frame_list.tree)
    item_focused = right_frame_list.tree.focus ()
    entry_search_right.bind ("<Escape>",
                             lambda event, item=item_focused, search=search_tree: destroy (event, search, False, item))
    entry_search_right.bind ("<KeyRelease>", lambda event, search=search_tree: b_ (event, search))

    entry_search_right.pack (fill=BOTH)
    entry_search_right.focus ()
    entry_search_right.insert (0, key)


entry_search_left = Entry (left_frame, bg="black", fg="white", takefocus=False, insertbackground="white")


def b(event: Event):
    if event.char == "" or event.char == '':
        return
    key = event.char
    search_tree = Search (left_frame_list.tree)
    item_focused = left_frame_list.tree.focus ()
    entry_search_left.bind ("<Escape>",
                            lambda event, item=item_focused, search=search_tree: destroy (event, search, True, item))
    entry_search_left.bind ("<KeyRelease>", lambda event, search=search_tree: b_ (event, search))
    entry_search_left.pack (fill=BOTH)
    entry_search_left.focus ()
    entry_search_left.insert (0, key)


# Here we bind all the chart keys like a, b, c, d, e etc.
right_frame_list.a (a)
left_frame_list.a (b)
# root.attributes ('-alpha', 0.7)
w = 800
h = 500
ws = root.winfo_screenwidth ()
hs = root.winfo_screenheight ()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry ('%dx%d+%d+%d' % (w, h, x, y))


def last_windows():
    """
    Here we save the paths in wich we are right now
    """
    prefs = open ("preferences.json", "r")
    read = prefs.read ()
    prefs.close ()
    jsprefs = json.loads (read)
    jsprefs["lasts_windows"]["left"] = vars.actual_left_path
    jsprefs["lasts_windows"]["right"] = vars.actual_right_path
    pref = open ("preferences.json", "w")
    s = json.dumps (jsprefs, indent=4)
    pref.write (s)
    pref.close ()
    root.destroy ()


root.protocol ('WM_DELETE_WINDOW', last_windows)


def f12(event):
    """
    Here we instantiate the searchwindow class
    """
    SearchWindow.SearchWindow (root)


foto = PIL.Image.open ("folder.png")
image = ImageTk.PhotoImage (foto)
root.iconphoto (True, image)


def hidden(event):
    """
    When press ctrl o we hide or unhide files and store this in preferences.json
    """
    preferences = open ("preferences.json", "r")
    read = preferences.read ()
    preferences.close ()
    js = json.loads (read)
    if not js["hidden"][0]:
        js["hidden"][0] = True
        save = json.dumps (js, indent=4)
        prefs = open ("preferences.json", "w")
        prefs.write (save)
        vars.hidden = True
    else:
        js["hidden"][0] = False
        save = json.dumps (js, indent=4)
        prefs = open ("preferences.json", "w")
        prefs.write (save)
        vars.hidden = False
    actualizar.update ()


root.bind ("<Control-F12>", f12)
root.bind ("<Control-o>", hidden)
root.mainloop ()
