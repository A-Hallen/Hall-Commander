import threading
import time
from threading import Thread, Event
from tkinter import ttk, W, CENTER, BOTH, NO, Scrollbar, RIGHT
from tkinter.ttk import Progressbar, Treeview

import vars


class TreeViewlist:
    stop_event: Event

    def __init__(self, frame):
        # Here we initialize the images
        self.item = 0
        self.progress_bar = None
        self.frame = frame
        self.stop_event: Event
        self.c = 0

        # Here we are gonna list all files
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=1, bd=0, bordercolor="blue",
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 11, 'normal'),
                        borderwidth=0)  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.tree = Treeview(frame, style="mystyle.Treeview", padding=[0, 0, 0, 0])
        scroll = Scrollbar(self.tree, bd=0, bg=vars.gray, troughcolor=vars.dark_gray, takefocus=False)
        scroll.pack(side=RIGHT, fill="y", pady=27)
        self.tree.config(yscrollcommand=scroll.set)
        scroll.config(command=self.tree.yview)
        self.tree.tag_configure('even', foreground='green')
        self.tree.tag_configure('odd', background='#222222')
        self.tree['columns'] = ("Ext", "Tamaño")
        self.tree.column("Ext", anchor=W, width=30)
        self.tree.column("Tamaño", anchor=W, width=90, stretch=NO)

        self.tree.heading("#0", text="Nombre", anchor=CENTER)
        self.tree.heading("Ext", text="Ext", anchor=W)
        self.tree.heading("Tamaño", text="Tamaño")

        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview', rowheight=35, hightlightthickness=0, background=vars.tree_view_background,
                    foreground=vars.tree_view_foreground, fieldbackground=vars.tree_view_fieldbackground,
                    bd=0, font=('Calibri', 11))
        s.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        s.map('Treeview', background=[('selected', '#BFBFBF')], foreground=[('selected', 'black')])  # Selection mode

        # Add Data
        self.tree.pack(expand=True, fill=BOTH)

    def double_click(self, function):
        self.tree.bind("<Double-1>", function)
        self.tree.bind("<Return>", function)

    def click(self, function):
        self.tree.bind("<Button-1>", function)

    def f2(self, function):
        self.tree.bind("<F2>", function)

    def tab(self, function):
        self.tree.bind("<Tab>", function)

    def threada(self, event, stop_event, function_a):
        while not stop_event.is_set() and self.c != 7:
            self.c = self.c + 1
            time.sleep(0.1)
        self.callb(event, function_a)

    def calla(self, event, function_a):
        self.item = self.tree.identify("item", event.x, event.y)
        if self.item not in self.tree.selection():
            self.tree.selection_add(self.item)
        else:
            self.tree.selection_remove(self.item)
        self.stop_event = threading.Event()
        t_array = Thread(target=self.threada, args=(event, self.stop_event, function_a))
        t_array.daemon = True
        t_array.start()
        time.sleep(0.1)

        s = ttk.Style()
        s.theme_use("clam")
        s.configure("red.Horizontal.TProgressbar", foreground='black', background='green',
                    troughcolor='white', bordercolor="black", lightcolor="black", darkcolor="black")
        time.sleep(0.1)
        self.progress_bar = Progressbar(self.frame, style="red.Horizontal.TProgressbar",
                                        orient="horizontal", length=7, mode="determinate", )
        self.progress_bar.place(x=event.x, y=event.y + 10, width=60, height=13)
        self.progress_bar.start(4)

    def callb(self, event, function_a):
        if not self.progress_bar:
            return
        self.progress_bar.destroy()
        self.stop_event.set()
        if self.c == 7:
            self.tree.selection_add(self.tree.identify("item", event.x, event.y))
            function_a(event)
            self.c = 0
        else:
            self.c = 0

    def right_bind_press(self, function_a):
        self.tree.bind("<ButtonPress-3>", lambda event, function_a=function_a: self.calla(event, function_a))

    def right_bind_release(self, function_a):
        self.tree.bind('<ButtonRelease-3>', lambda event, function_a=function_a: self.callb(event, function_a))

    def back_space(self, function):
        self.tree.bind('<BackSpace>', function)

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def F7(self, function):
        self.tree.bind('<F7>', function)

    def F5(self, function):
        self.tree.bind('<F5>', function)

    def delete(self, function):
        self.tree.bind("<Delete>", function)

    def a(self, function):
        self.tree.bind("<Key>", function)

    def drag(self, function):
        self.tree.bind("<B1-Motion>", function)

    def drag_left(self, event):
        self.item = self.tree.identify("item", event.x, event.y)
        self.tree.selection_add(self.item)

    def f12(self, function):
        self.tree.bind("<Control-F12>", function)

    def add_data(self, data):
        a = 0
        self.tree.bind("<B3-Motion>", self.drag_left)

        for record in data:
            self.tree.insert(parent='', image=record[4], index='end', iid=a, text=record[0],
                             values=(record[1], record[2]))
            a = a + 1
