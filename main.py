#! /usr/bin/python3
import _tkinter
import json
from os.path import exists, isdir, join, splitext, abspath, ismount, dirname
from time import sleep
from tkinter import ttk, Tk, Frame, BOTH, LEFT, Label, W, Button, FLAT, Entry, Event, RIGHT, Menu

from PIL import ImageTk, Image
from gi import require_version
from magic import Magic
from psutil import Error as psError
from psutil import disk_partitions

import CopyToClipBoard
import some_functions
import vars
from FileManipulation import FileManipulation
from MyDialog import CopyDialog
from actualizar import Actualizar
from get_file_icon import Load_Thumb
from horizontal_bar import HorizontalBar
from list_drives import Drives
from list_files import ListFiles
from listar import Listar
from menu_bar import _Menu
from popup_menu import PopUpMenu
from search_tree import Search
from tree_view import TreeViewlist
from vertical_bar import VerticalBar

# 0.95
require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk


# 1.23
# the first function we execute
def start():
    prefs = open("preferences.json", "r")
    base = {"hidden": [True], "lasts_windows": {"left": "/home/hallen", "right": "/home/hallen", "size": "900x500"},
            "toolbar": {}, "commands": {}}
    read_prefs = prefs.read()
    from json import JSONDecodeError
    try:
        json_read = json.loads(read_prefs)
    except JSONDecodeError:
        prefs.close()
        prefs = open("preferences.json", "w")
        prefs.write(json.dumps(base, indent=4))
        json_read = base
    prefs.close()
    actualleft = json_read["lasts_windows"]["left"]
    actualright = json_read["lasts_windows"]["right"]
    if exists(actualleft) and isdir(actualleft):
        vars.actual_left_path = actualleft
        vars.opened_left_paths.append(actualleft)
    if exists(actualright) and isdir(actualright):
        vars.actual_right_path = actualright
        vars.opened_right_paths.append(actualright)
    vars.hidden = json_read["hidden"][0]


def listar_left(event):
    global item_left_text
    item_left = left_frame_list.tree.selection()[0]  # Identificamos el item que a sido doble clickeado
    item_left_text = left_frame_list.tree.item(item_left, "text") + left_frame_list.tree.item(item_left, "values")[
        0]  # Extraemos el texto que poseee ese item
    if item_left_text == "":
        return
    path = vars.actual_left_path + "/" + item_left_text  # calculamos su path
    listar_l.listar(left_path, item_left_text, path)


def create_file():
    if vars.selection_left:
        file_manipulation.folder_dialog(None)
    else:
        file_manipulation.folder_dialog(None, False)


def delete_dialog():
    if vars.selection_left:
        file_manipulation.delete_dialog(None)
    else:
        file_manipulation.delete_dialog((None, False))


def edit_dialog():
    if vars.selection_left:
        file_manipulation.f2(None)
    else:
        file_manipulation.f2(None, False)


def copiar():
    if vars.selection_left:
        file_manipulation.copy_dialog(None)
    else:
        file_manipulation.copy_dialog(None, False)


def listar_right(event):
    global item_right_text
    item_right = right_frame_list.tree.selection()[0]  # Identificamos el item que a sido doble clickeado
    item_right_text = right_frame_list.tree.item(item_right, "text") + \
                      right_frame_list.tree.item(item_right, "values")[0]
    if item_right_text == "":
        return
    path = vars.actual_right_path + "/" + item_right_text  # calculamos su path
    listar_r.listar(right_path, item_right_text, path)


def edit(path, actual_path, left):
    label_edit = ttk.Entry(path)
    label_edit.pack(fill="x")
    label_edit.insert(0, actual_path)
    label_edit.focus()
    label_edit.select_range(0, "end")

    def edit_destroy(event):
        label_edit.destroy()
        label_edit.update()

    label_edit.bind("<FocusOut>", edit_destroy)
    text = ""

    def edit_enter(event):
        global text
        text = label_edit.get()
        if left:
            listar_l.listar(path, "", text)
        else:
            listar_r.listar(path, "", text)

    label_edit.bind("<Return>", edit_enter)


# Here we handle the little edit at top of the two frames
def edit_left(event):
    edit(left_path, vars.actual_left_path, True)


# Here we handle the little edit at top right
def edit_right(event):
    edit(right_path, vars.actual_right_path, False)


def change_left(event):
    vars.selection_left = True
    vars.last_selection_right = right_frame_list.tree.focus()
    right_frame_list.tree.item(right_frame_list.tree.focus(), tags="odd")
    try:
        left_frame_list.tree.item(vars.last_selection_left, tags="")
    except _tkinter.TclError:
        print("error in main.py change_left function, line ~ 156 item " + str(vars.last_selection_left) + " Not found")
    right_frame_list.tree.selection_remove(*right_frame_list.tree.get_children())


def change_right(event):
    vars.selection_left = False
    vars.last_selection_left = left_frame_list.tree.focus()
    left_frame_list.tree.item(left_frame_list.tree.focus(), tags="odd")
    right_frame_list.tree.item(vars.last_selection_right, tags="")
    left_frame_list.tree.selection_remove(*left_frame_list.tree.get_children())


def tab(event, left=True):
    if left:
        vars.selection_left = False
        if vars.last_selection_right == "":
            vars.last_selection_right = 0
        right_frame_list.tree.selection_add(vars.last_selection_right)
        right_frame_list.tree.focus(vars.last_selection_right)
        change_right(event)
    else:
        vars.selection_left = True
        if vars.last_selection_left == "":
            vars.last_selection_left = 0
        left_frame_list.tree.selection_add(vars.last_selection_left)
        left_frame_list.tree.focus(vars.last_selection_left)
        change_left(event)


def back_space(event, left=True):
    if left:
        listar_l.listar(left_path, "..", vars.actual_left_path + "/..")
    else:
        listar_r.listar(right_path, "..", vars.actual_right_path + "/..")


def start_m(event, _frame, actual):
    """
    this function starts the frame context menus

    :param actual:  the actual path should be string
    :param _frame:
    :param event: the event
    :return:
    """
    global program_icon_array
    tree: ttk.Treeview = event.widget
    item = tree.identify("item", event.x, event.y)
    # Initialize the images

    menu = Menu(_frame, tearoff=False, relief=FLAT, bd=9, bg=vars.dark_gray,
                fg="white", activeforeground="green", activebackground=vars.dark_gray)
    if item == "":
        print("This is not any item")
    else:
        name = tree.item(item, "text")
        ext = tree.item(item, "values")[0]
        full_name = name + ext
        mime = Magic(mime=True)
        path = join(actual, full_name)
        if isdir(path):
            menu.add_command(label="Abrir carpeta")
        else:
            mime = mime.from_file(path)
            open_with = Menu(menu, tearoff=False, bd=9, relief=FLAT, activeforeground="green",
                             bg=vars.dark_gray, fg="white", activebackground=vars.dark_gray)

            # mounts = Gio.unix_mount_points_get()
            def get_images(filename):
                pg = None
                try:
                    formats = [".ppm", ".png", ".jpg", ".jpeg", ".gif", ".tiff", ".bmp"]
                    if splitext(filename)[1].lower() in formats:
                        pil_img = Image.open(filename)
                        res_pil = pil_img.resize((30, 30), Image.ANTIALIAS)
                        pg = ImageTk.PhotoImage(res_pil)
                    else:
                        from cairosvg import svg2png
                        png = svg2png(url=filename)
                        from io import BytesIO
                        pil_img = Image.open(BytesIO(png))
                        res_pil = pil_img.resize((30, 30), Image.ANTIALIAS)
                        pg = ImageTk.PhotoImage(res_pil)
                except:
                    pil_img = Image.open("desconocido.png")
                    res_pil = pil_img.resize((30, 30), Image.ANTIALIAS)
                    pg = ImageTk.PhotoImage(res_pil)
                finally:
                    return pg

            # This is the function that launchs the files
            def launch_program(program):
                item_list = tree.selection()
                path_list = []
                for i in item_list:
                    _path = join(actual, tree.item(i, "text") + tree.item(i, "values")[0])
                    path_list.append(Gio.File.new_for_path(_path))
                program.launch(path_list)

            l = Gio.app_info_get_recommended_for_type(mime)
            for e in range(len(l)):
                app = l[e]
                icon = app.get_icon()
                icon_theme = Gtk.IconTheme.get_default()
                icon_file = icon_theme.lookup_icon(icon.to_string(), 32, 0)
                final_filename = ""
                if icon_file is not None:
                    final_filename = icon_file.get_filename()

                imagen = get_images(final_filename)
                program_icon_array.insert(e, imagen)
                open_with.add_command(image=program_icon_array[e], compound="left", label=app.get_name(),
                                      command=lambda program=app: launch_program(program))
            default = Gio.app_info_get_default_for_type(mime, False)
            image_new = Image.new('RGBA', (30, 30))
            image_new = ImageTk.PhotoImage(image_new)

            def launch_other_program():
                global program_icon_array
                program_icon_array = []
                apps = Gio.app_info_get_all()
                menu_ = PopUpMenu(root, bd=10, bordercolor="black")
                texto = "Abrir: " + tree.item(item, "text")
                imagen_ = tree.item(item, "image")
                menu_.title(text=texto, image=imagen_)

                def launch(event, tree):
                    item_ = tree.identify("item", event.x, event.y)
                    index = tree.item(item_, "values")[0]
                    menu_.destroy()
                    launch_program(apps[int(index)])

                menu_.onclick(launch)

                def start_thread():
                    for index, app_ in enumerate(apps):
                        if not app_.should_show():
                            program_icon_array.insert(index, None)
                            continue
                        try:
                            icono = app_.get_icon()
                            icono_theme = Gtk.IconTheme.get_default()
                            icono_file = icono_theme.lookup_icon(icono.to_string(), 32, 0)
                            nombre = ""
                            if icono_file is not None:
                                nombre = icono_file.get_filename()
                        except:
                            nombre = ""

                        image_ = get_images(nombre)
                        program_icon_array.insert(index, image_)
                        menu_.add_command(text=app_.get_name(), image=program_icon_array[index], index=index)

                from threading import Thread
                hilo = Thread(target=start_thread)
                hilo.start()

            def copiar():
                selections = []
                paths = tree.selection()
                for f in paths:
                    item_text = tree.item(f, "text") + tree.item(f, "values")[0]
                    selections.append(join(actual, item_text))
                CopyToClipBoard.CopyToClipBoard().copyfile(selections)

            def pegar():
                if vars.last_selection_left:
                    CopyDialog(vars.portapapeles, actual, listar_r, left_path, root, actualizar)
                else:
                    CopyDialog(vars.portapapeles, actual, listar_l, right_path, root, actualizar)

            open_with.add_command(image=image_new, compound="left", label="Abri con otro programa",
                                  command=launch_other_program)
            menu.add_command(image=tree.item(item, "image"), compound="left", label="Abrir archivo",
                             command=lambda default=default: launch_program(default))
            menu.add_separator()
            menu.add_cascade(label="Abrir con", menu=open_with)
            menu.add_separator()
            menu.add_command(image=image_array[2], compound="left", label="Copiar", command=copiar)
            menu.add_command(image=image_array[1], compound="left", label="Cortar")
            if len(vars.portapapeles) == 0:
                print("Portapapeles vacio")
            else:
                menu.add_command(image=image_array[4], label="Pegar", command=pegar, compound="left")
            menu.add_command(image=image_array[0], compound="left", label="Eliminar")
            menu.add_command(image=image_array[3], compound="left", label="Propiedades")

        menu.tk_popup(event.x_root, event.y_root)


def function_menu_r(event):
    start_m(event, right_frame, vars.actual_right_path)


def function_menu_l(event):
    start_m(event, right_frame, vars.actual_left_path)


def find_sdiskpart(path):
    path = abspath(path)
    while not ismount(path):
        path = dirname(path)
    p = [p for p in disk_partitions(all=True) if p.mountpoint == path.__str__()]

    if len(p) == 1:
        return p[0]

    raise psError


def f12(event, left=True):
    """
    Here we instantiate the searchwindow class
    """
    import SearchWindow
    global iscontrolpressed
    iscontrolpressed = True
    if left:
        SearchWindow.SearchWindow(root, vars.actual_left_path, listar_l, left_path)
    else:
        SearchWindow.SearchWindow(root, vars.actual_right_path, listar_r, right_path)


def motion_general(event: Event, left=True):
    if left:
        other = right_frame_list.tree
        tree = left_frame_list.tree
        frame_list = right_frame
    else:
        tree = right_frame_list.tree
        other = left_frame_list.tree
        frame_list = left_frame

    if event.widget.winfo_containing(event.x_root, event.y_root) != event.widget:
        widget = event.widget
        item = widget.focus()
        imagen = widget.item(item, "image")
        x = event.x - 30
        y = event.y - 30
        canvas_drag.config(image=imagen)
        canvas_drag.place(in_=widget, x=x, y=y, width=30, height=30)
    global hovered_items
    item_under = other.identify("item", event.x, event.y)
    if item_under != hovered_items:
        other.item(hovered_items, tags="")

    containing = event.widget.winfo_containing(event.x_root, event.y_root)
    if containing == other:
        frame_list.config(bg="green")
        hovered_items = item_under
        other.item(item_under, tags="even")
        label.grid_forget()
    elif containing == center_frame:
        row = center_frame.grid_size()[1]
        label.grid(column=0, row=row, pady=2)
        frame_list.config(bg="black")
    else:
        label.grid_forget()
        frame_list.config(bg="black")


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
    canvas_drag.place_forget()
    frame_list.config(bg="black")
    item_in_drag = tree.selection()
    other.item(hovered_items, tags="")
    item = other.identify("item", event.x, event.y)
    containing = event.widget.winfo_containing(event.x_root, event.y_root)

    if containing == other:
        if other.item(item, "text") == "":
            path_item = ""
        else:
            name_item = other.item(item, "text") + other.item(item, "values")[0]
            path_item = join(actual_dest, name_item)
        items_path = []
        for i in item_in_drag:
            if tree.item(i, "text") != "..":
                items_path.append(join(actual_source, tree.item(i, "text") + tree.item(i, "values")[0]))
        if isdir(path_item):
            destiny = join(actual_dest, path_item)
        else:
            destiny = actual_dest
        CopyDialog(items_path, destiny, listar, label_path, root, actualizar)
    elif containing == center_frame:
        label.grid_forget()
        path = join(actual_source,
                    tree.item(item_in_drag[0], "text") + tree.item(item_in_drag[0], "values")[0])
        vertical_bar.create_link(None, True, path)


# Create the entry widget for search actions in panels
def destroy(event, search, left=None, item=0):
    search.serach_tree("")
    if left != None:
        if left == True:
            left_frame_list.tree.focus_set()
            left_frame_list.tree.focus(item)
        else:
            right_frame_list.tree.focus_set()
            right_frame_list.tree.focus(item)
    event.widget.pack_forget()


def b_(event, search_tree):
    entry = event.widget
    text = entry.get()
    search_tree.serach_tree(text)


def a(event):
    global iscontrolpressed
    if event.keysym == "Control_L" or event.keysym == "Control_R":
        iscontrolpressed = True
    if event.char == "" or iscontrolpressed or event.keysym == "Escape":
        return
    key = event.char
    search_tree = Search(right_frame_list.tree)
    item_focused = right_frame_list.tree.focus()
    entry_search_right.bind("<Escape>",
                            lambda event, item=item_focused, search=search_tree: destroy(event, search, False, item))
    entry_search_right.bind("<KeyRelease>", lambda event, search=search_tree: b_(event, search))

    entry_search_right.pack(fill=BOTH)
    entry_search_right.focus()
    entry_search_right.insert(0, key)


def b(event: Event):
    global iscontrolpressed
    if event.keysym == "Control_L" or event.keysym == "Control_R":
        iscontrolpressed = True
    if event.char == "" or iscontrolpressed or event.keysym == "Escape":
        return
    key = event.char
    search_tree = Search(left_frame_list.tree)
    item_focused = left_frame_list.tree.focus()
    entry_search_left.bind("<Escape>",
                           lambda event, item=item_focused, search=search_tree: destroy(event, search, True, item))
    entry_search_left.bind("<KeyRelease>", lambda event, search=search_tree: b_(event, search))
    entry_search_left.pack(fill=BOTH)
    entry_search_left.focus()
    entry_search_left.insert(0, key)


def save_size(js):
    w = root.winfo_width()
    h = root.winfo_height()
    with open("preferences.json", "w") as prefs:
        js["lasts_windows"]["size"] = str(w) + "x" + str(h)
        s = json.dumps(js, indent=4)
        prefs.write(s)


def last_windows():
    """
    Here we save the paths in wich we are right now
    for close the program, and store the paths and the size
    of the window
    """
    prefs = open("preferences.json", "r")
    read = prefs.read()
    prefs.close()
    jsprefs = json.loads(read)
    save_size(jsprefs)
    jsprefs["lasts_windows"]["left"] = vars.actual_left_path
    jsprefs["lasts_windows"]["right"] = vars.actual_right_path
    pref = open("preferences.json", "w")
    s = json.dumps(jsprefs, indent=4)
    pref.write(s)
    pref.close()
    root.destroy()


# noinspection PyTypeChecker
def hidden(event):
    """
    When press ctrl o we hide or unhide files and store this in preferences.json
    """
    global iscontrolpressed, tool_bar_top, hidden_icon
    boton: Button = tool_bar_top.winfo_children()[3]
    iscontrolpressed = True
    preferences = open("preferences.json", "r")
    read = preferences.read()
    preferences.close()
    js = json.loads(read)
    if not js["hidden"][0]:
        js["hidden"][0] = True
        save = json.dumps(js, indent=4)
        prefs = open("preferences.json", "w")
        prefs.write(save)
        vars.hidden = True
        boton.config(image=hidden_icon[1])

    else:
        js["hidden"][0] = False
        save = json.dumps(js, indent=4)
        prefs = open("preferences.json", "w")
        prefs.write(save)
        vars.hidden = False
        boton.config(image=hidden_icon[0])
    actualizar.update()


def release_control(event):
    global iscontrolpressed
    iscontrolpressed = False


def set_geometry():
    # read the window last size
    with open("preferences.json", "r") as last_size_prefs:
        json_size = json.loads(last_size_prefs.read())
        while True:
            try:
                root.geometry(json_size["lasts_windows"]["size"])
                menus = _Menu(root, vars.name_of_the_app, left_frame_list, right_frame_list)

                # The root config
                root.config(bg="black", menu=menus.menu)
                break
            except RuntimeError:
                sleep(0.001)


def initialize_image_menus():
    global label_right_t, label_left_d, label_left_t, label_right_d, image_array
    while True:
        try:
            label_left_t = Label(drive_bar_left, padx=10, takefocus=False, fg=vars.gray, font=('Calibri', 9, 'normal'),
                                 bg=vars.soft_gray)
            break
        except RuntimeError:
            sleep(0.001)
    label_left_t.grid(row=0, column=1)
    label_left_d = Label(drive_bar_left, padx=10, fg=vars.gray, takefocus=False, font=('Calibri', 9, 'normal'),
                         bg=vars.soft_gray)
    label_left_d.grid(row=0, column=2)

    label_right_t = Label(drive_bar_right, padx=10, takefocus=False, fg=vars.gray, font=('Calibri', 9, 'normal'),
                          bg=vars.soft_gray)
    label_right_t.grid(row=0, column=1)
    label_right_d = Label(drive_bar_right, padx=10, fg=vars.gray, takefocus=False, font=('Calibri', 9, 'normal'),
                          bg=vars.soft_gray)
    label_right_d.grid(row=0, column=2)

    Drives(drive_left, drive_right, label_left_t,
           label_right_t, label_left_d, label_right_d,
           listar_l, listar_r, left_path, right_path)

    for i, imag in enumerate(["borrar.png", "cortar.png", "copiar.png", "propiedades.png", "paste.ico"]):
        image_array.insert(i, ImageTk.PhotoImage(Image.open("resources/" + imag).resize((24, 24), Image.ANTIALIAS)))


def vertical_thread():
    global vertical_bar
    vertical_bar = VerticalBar(center_frame, True, listar_r, listar_l, left_path, right_path)
    while True:
        try:
            center_frame.bind("<ButtonPress-3>", vertical_bar.start)
            break
        except RuntimeError:
            sleep(0.001)

    # -----------------------------Initialize the images of the central frame--------------------------------
    from center_frame import VerticalBarCommands
    vertical_bar_commands = VerticalBarCommands(center_frame, listar_r, listar_l, left_path, right_path)
    vertical_bar_commands.command()


def tool_bar_thread():
    # The toolbar top predefined actions
    tool_bar_start = HorizontalBar(tool_bar_top)
    tool_bar_top.bind("<ButtonPress-3>", tool_bar_start.start_menu)
    tool_bar_start.load_pred(left_path, right_path, listar_r, listar_l,
                             left_frame_list.tree, right_frame_list.tree)
    tool_bar_start.start()
    # =========================------------------===========================----------------------============================#|
    Button(tool_bar, text="F5 Copiar", height=1, width=0, bd=0, command=copiar, padx=20,
           bg="black", fg="white", takefocus=False).grid(row=0, column=1, sticky='nsew', rowspan=2)
    Button(tool_bar, text="F6 Mover", height=1, width=0, bd=0, padx=20, bg="black", fg="white",
           takefocus=False).grid(row=0, column=2, sticky='nsew', rowspan=2)
    Button(tool_bar, text="F2 Renombrar", height=1, width=0, bd=0, padx=20, bg="black", fg="white",
           takefocus=False, command=edit_dialog).grid(row=0, column=0, sticky='nsew', rowspan=1)
    Button(tool_bar, text="F8 Delete", height=1, width=0, bd=0, padx=20, bg="black", fg="white",
           takefocus=False, command=delete_dialog).grid(row=0, column=4, sticky='nsew', rowspan=2)
    Button(tool_bar, text="F7 Nueva Carpeta", height=1, width=0, bd=0, padx=20, bg="black", fg="white",
           takefocus=False, command=create_file).grid(row=0, column=3, sticky='nsew', rowspan=2)
    # =========================------------------===========================----------------------==========================


start()
# Set the root window
root = Tk()
root.title(vars.name_of_the_app)
# The menu of the app
# The main frame of the window
frame = Frame(root)
frame.configure(bg=vars.color_of_side_frames, takefocus=False)
frame.pack(expand=True, fill=BOTH)
tool_bar_top = Frame(frame, height=30, bg=vars.soft_gray, takefocus=False)
tool_bar_top.pack(fill="x")

# The left frame of the app
left_frame = Frame(frame)
left_frame.config(bg=vars.color_of_side_frames, bd=2, takefocus=False)
left_frame.pack_propagate(False)
left_frame.pack(fill=BOTH, expand=True, side=LEFT)

drive_bar_left = Frame(left_frame)
drive_bar_left.config(bg=vars.soft_gray, height=22, takefocus=False)
drive_bar_left.pack(fill="x")
drive_bar_left.grid_propagate(False)
drive_left = Frame(drive_bar_left, bg=vars.soft_gray)
drive_left.grid(row=0, column=0)

# Adding the left top lavel for the path information
left_path = Label(master=left_frame, anchor=W, bg=vars.gray, fg="white", takefocus=False)
left_path.configure(padx=10, text=vars.actual_left_path, width=1)
left_path.pack(fill="x")

# The right frame of the app
right_frame = Frame(frame)
right_frame.pack_propagate(False)
right_frame.config(bg=vars.color_of_side_frames, bd=2, takefocus=False)
right_frame.pack(fill=BOTH, expand=True, side=RIGHT)

drive_bar_right = Frame(right_frame)
drive_bar_right.config(bg=vars.soft_gray, height=22, takefocus=False)
drive_bar_right.pack(fill="x")
drive_bar_right.grid_propagate(False)
drive_right = Frame(drive_bar_right, bg=vars.soft_gray)
drive_right.grid(row=0, column=0)

# Adding the left top lavel for the path information
right_path = Label(right_frame, anchor=W, bg=vars.gray, fg="white")
right_path.configure(padx=10, text=vars.actual_right_path, width=1, takefocus=False)
right_path.pack(fill="x")

center_frame = Frame(frame)
center_frame.config(bg=vars.soft_gray, width=35, takefocus=False, highlightthickness=1,
                    highlightbackground=vars.soft_gray)
center_frame.pack(fill="y", expand=True)

# The tool bar
tool_bar = Frame(root)
tool_bar.config(bg="black", height=25, bd=1, takefocus=False)
tool_bar.pack(fill="x")
# Adding items to toolbar

for n in range(5):
    tool_bar.columnconfigure(n, weight=1)
Label(center_frame, height=3, width=4, bg=vars.soft_gray, takefocus=False).grid(row=0, column=0)

# The tree  view
left_frame_list = TreeViewlist(left_frame)
right_frame_list = TreeViewlist(right_frame)
# left_frame_list.add_data(data)

# Initialized the reading of the data
leftlistfiles = ListFiles()
lista_l = leftlistfiles.list(vars.actual_left_path)

left_frame_list.add_data(lista_l)
array_images_left = []
left_thumb_thread = Load_Thumb(left_frame_list.tree, vars.actual_left_path, array_images_left)
left_thumb_thread.start()
# Inicializamos la clase listar para el frame izquierdo
listar_l = Listar(True, left_frame_list, left_thumb_thread)

item_left_text = ""

rightlistfiles = ListFiles()
lista_r = rightlistfiles.list(vars.actual_right_path)
right_frame_list.add_data(lista_r)
array_images_right = []
right_thumb_thread = Load_Thumb(right_frame_list.tree, vars.actual_right_path, array_images_right)
right_thumb_thread.start()
# Inicializamos la clase listar para el frame derecho
listar_r = Listar(False, right_frame_list, right_thumb_thread)

actualizar = Actualizar(left_path, right_path, listar_r, listar_l)
item_right_text = ""

# =========================------------------===========================----------------------============================#|
file_manipulation = FileManipulation(left_frame_list, right_frame_list, listar_l, listar_r, left_path, right_path,
                                     root, actualizar)

# -------------------------------------===========================================--------------------------------------
# Thread for initialize the vertical bar
vertical_bar: VerticalBar
# -------------------------------------===========================================--------------------------------------

# Here we initialize the images of menus
image_array = []
program_icon_array = []

label_left_t: Label
label_left_d: Label
label_right_t: Label
label_right_d: Label

# Initialize the menus in a separate thread and some images too

hovered_items = 0
hovered_items_tree = 0
iscontrolpressed = False
canvas_drag: Label
label: Label
entry_search_right: Entry
entry_search_left: Entry

# bind all functions and this things
left_frame_list.double_click(listar_left)  # Añadimos la función
left_path.bind("<Double-1>", edit_left)
left_frame_list.click(change_left)
left_frame_list.f2(file_manipulation.f2)
left_frame_list.tab(tab)
left_frame_list.back_space(back_space)
left_frame_list.right_bind_press(function_menu_l)
left_frame_list.right_bind_release(function_menu_l)
left_frame_list.F7(file_manipulation.folder_dialog)
left_frame_list.delete(file_manipulation.delete_dialog)
left_frame_list.F5(file_manipulation.copy_dialog)
left_frame_list.f12(f12)

right_frame_list.double_click(listar_right)
right_path.bind("<Double-1>", edit_right)
right_frame_list.click(change_right)
right_frame_list.f2(lambda event: file_manipulation.f2(event, False))
right_frame_list.tab(lambda event, left=False: tab(event, left))
right_frame_list.back_space(lambda event, left=False: back_space(event, left))
right_frame_list.right_bind_press(function_menu_r)
right_frame_list.right_bind_release(function_menu_r)
right_frame_list.F7(lambda event: file_manipulation.folder_dialog(event, False))
right_frame_list.delete(lambda event: file_manipulation.delete_dialog(event, False))
right_frame_list.F5(lambda event: file_manipulation.copy_dialog(event, False))
right_frame_list.f12(lambda event: f12(event, False))

image_drag = Image.open("folder.png")
photo_drag = ImageTk.PhotoImage(image_drag)
canvas_drag = Label(image=photo_drag)

ima = Image.new('RGBA', (30, 30))
label = Label(master=center_frame, image=ImageTk.PhotoImage(ima))

right_frame_list.tree.bind("<ButtonRelease-1>", lambda event: droped(event, False))
right_frame_list.drag(lambda event: motion_general(event, False))
left_frame_list.tree.bind("<ButtonRelease-1>", droped)
left_frame_list.drag(motion_general)

entry_search_right = Entry(right_frame, bg="black", fg="white", takefocus=False, insertbackground="white")

entry_search_left = Entry(left_frame, bg="black", fg="white", takefocus=False, insertbackground="white")

# Here we bind all the chart keys like a, b, c, d, e etc.
right_frame_list.a(a)
left_frame_list.a(b)

root.protocol('WM_DELETE_WINDOW', last_windows)

foto = Image.open("folder.png")
image = ImageTk.PhotoImage(foto)
root.iconphoto(True, image)

hidden_icon = [some_functions.image("resources/btn_on.png", (25, 25)),
               some_functions.image("resources/btn_off.png", (25, 25))]

root.bind("<KeyRelease-Control_L>", release_control)
root.bind("<KeyRelease-Control_R>", release_control)
root.bind("<Control-o>", hidden)

root.after_idle(set_geometry)
root.after_idle(tool_bar_thread)
root.after_idle(vertical_thread)
root.after_idle(initialize_image_menus)
root.mainloop()
