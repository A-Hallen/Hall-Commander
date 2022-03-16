import threading

import vars
from listar import Listar


class Actualizar:
    def __init__(self, left_path, right_path, listar_r: Listar, listar_l: Listar):
        self.listar_r = listar_r
        self.listar_l = listar_l
        self.left_path = left_path
        self.right_path = right_path

    def update_left(self):
        self.listar_l.listar(self.left_path, "", vars.actual_left_path)

    def update_right(self):
        self.listar_r.listar(self.right_path, "", vars.actual_right_path)

    def update(self):
        threading.Thread(target=self.update_right).start()
        threading.Thread(target=self.update_left).start()
