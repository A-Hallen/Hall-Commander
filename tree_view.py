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
        self.progress_bar = None
        self.frame = frame
        self.stop_event = None
        self.c = 0

        # Here we are gonna list all files
        style = ttk.Style ()
        style.configure ("mystyle.Treeview", highlightthickness=1, bd=0, bordercolor="blue",
                         font=('Calibri', 11))  # Modify the font of the body
        style.configure ("mystyle.Treeview.Heading", font=('Calibri', 11, 'normal'),
                         borderwidth=0)  # Modify the font of the headings
        style.layout ("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.tree = Treeview (frame, style="mystyle.Treeview", padding=[0, 0, 0, 0])

        scroll = Scrollbar (self.tree, bd=0, bg=vars.gray, troughcolor=vars.dark_gray, takefocus=False)
        scroll.pack (side=RIGHT, fill="y", pady=27)
        self.tree.config (yscrollcommand=scroll.set)
        scroll.config (command=self.tree.yview)
        self.tree.tag_configure ('even', foreground='red')
        self.tree.tag_configure ('odd', background='#222222')
        self.tree['columns'] = ("Ext", "Tamanio")
        self.tree.column ("Ext", anchor=W, width=30)
        self.tree.column ("Tamanio", anchor=W, width=90, stretch=NO)

        self.tree.heading ("#0", text="Nombre", anchor=CENTER)
        self.tree.heading ("Ext", text="Ext", anchor=W)
        self.tree.heading ("Tamanio", text="Tamanio")

        s = ttk.Style ()
        s.theme_use ('clam')
        s.configure ('Treeview', rowheight=35, hightlightthickness=0, background=vars.tree_view_background,
                     foreground=vars.tree_view_foreground, fieldbackground=vars.tree_view_fieldbackground,
                     bd=0, font=('Calibri', 11))
        s.layout ("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        s.map ('Treeview', background=[('selected', '#BFBFBF')], foreground=[('selected', 'black')])

        # Add Data
        self.tree.pack (expand=True, fill=BOTH)

    def double_click(self, function):
        self.tree.bind ("<Double-1>", function)
        self.tree.bind ("<Return>", function)

    def click(self, function):
        self.tree.bind ("<Button-1>", function)

    def f2(self, function):
        self.tree.bind ("<F2>", function)

    def tab(self, function):
        self.tree.bind ("<Tab>", function)

    def threada(self, event, stop_event, function_a, function_b):
        while not stop_event.is_set () and self.c != 7:
            self.c = self.c + 1
            time.sleep (0.1)
        self.callb (event, function_a, function_b)

    def calla(self, event, function_a, function_b):
        item = self.tree.identify ("item", event.x, event.y)
        # self.tree.selection_remove(*self.tree.get_children())
        self.tree.selection_add (item)
        self.stop_event = threading.Event ()
        t_array = Thread (target=self.threada, args=(event, self.stop_event, function_a, function_b))
        t_array.daemon = True
        t_array.start ()
        time.sleep (0.1)
        s = ttk.Style ()
        s.theme_use ("clam")
        s.configure ("red.Horizontal.TProgressbar", foreground='black', background='green',
                     troughcolor='white', bordercolor="black", lightcolor="black", darkcolor="black")
        time.sleep (0.1)
        self.progress_bar = Progressbar (self.frame, style="red.Horizontal.TProgressbar",
                                         orient="horizontal", length=6, mode="determinate", )
        self.progress_bar.place (x=event.x, y=event.y + 10, width=60, height=13)
        self.progress_bar.start (4)

    def callb(self, event, function_a, function_b):
        self.progress_bar.destroy ()
        self.stop_event.set ()
        if self.c == 7:
            function_a (event)
            self.c = 0
        else:
            self.c = 0
            function_b (event)

    def right_bind_press(self, function_a, function_b):

        self.tree.bind ("<ButtonPress-3>", lambda event, function_a=function_a,
                                                  function_b=function_b: self.calla (event, function_a, function_b))

    def right_bind_release(self, function_a, function_b):
        self.tree.bind ('<ButtonRelease-3>', lambda event, function_a=function_a,
                                                    function_b=function_b: self.callb (event, function_a, function_b))

    def back_space(self, function):
        self.tree.bind ('<BackSpace>', function)

    def clear(self):
        self.tree.delete (*self.tree.get_children ())

    def F7(self, function):
        self.tree.bind ('<F7>', function)

    def F5(self, function):
        self.tree.bind ('<F5>', function)

    def test(self, event):
        print ("this is a del test")

    def delete(self, function):
        self.tree.bind ("<Delete>", function)

    def a(self, function):
        self.tree.bind ("<a>", function)
        self.tree.bind ("<b>", function)
        self.tree.bind ("<c>", function)
        self.tree.bind ("<d>", function)
        self.tree.bind ("<e>", function)
        self.tree.bind ("<f>", function)
        self.tree.bind ("<g>", function)
        self.tree.bind ("<h>", function)
        self.tree.bind ("<i>", function)
        self.tree.bind ("<j>", function)
        self.tree.bind ("<k>", function)
        self.tree.bind ("<l>", function)
        self.tree.bind ("<m>", function)
        self.tree.bind ("<n>", function)
        self.tree.bind ("<o>", function)
        self.tree.bind ("<p>", function)
        self.tree.bind ("<q>", function)
        self.tree.bind ("<r>", function)
        self.tree.bind ("<s>", function)
        self.tree.bind ("<t>", function)
        self.tree.bind ("<u>", function)
        self.tree.bind ("<v>", function)
        self.tree.bind ("<w>", function)
        self.tree.bind ("<x>", function)
        self.tree.bind ("<y>", function)
        self.tree.bind ("<z>", function)

    def add_data(self, data):
        a = 0
        for record in data:
            self.tree.insert (parent='', image=record[4], index='end', iid=a, text=record[0],
                              values=(record[1], record[2]))
            a = a + 1
