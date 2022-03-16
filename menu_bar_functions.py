from subprocess import run
from sys import platform

import vars


def open_terminal(left_tree, admin=False):
    if left_tree.selection():
        path = vars.actual_left_path
    else:
        path = vars.actual_right_path

    if platform == "linux":
        if not admin:
            run("x-terminal-emulator &", shell=True, cwd=path)
        else:
            run("x-terminal-emulator -e 'sudo su' &", shell=True, cwd=path)
