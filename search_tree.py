class Search:
    def __init__(self, tree):
        self.tree = tree
        self.old_array = []
        self.save_old ()

    def save_old(self):
        childs = self.tree.get_children ()

        for i in childs:
            name = self.tree.item (i, "text")
            ext = self.tree.item (i, "values")[0]
            size = self.tree.item (i, "values")[1]
            imagen = self.tree.item (i, "image")
            self.old_array.insert (int (i), (name, ext, size, imagen))

    def serach_tree(self, text):
        self.tree.delete (*self.tree.get_children ())
        for e in range (len (self.old_array)):
            i = self.old_array[e]
            name = i[0]
            ext = i[1]
            size = i[2]
            imagen = i[3]
            full_name = name + ext
            if text.lower () in full_name.lower () or name == "..":
                self.tree.insert (parent='', image=imagen, index='end', iid=str (e), text=name, values=(ext, size))
