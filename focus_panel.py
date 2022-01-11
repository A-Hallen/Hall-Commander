class GetFocusPanel:
    def __init__(self, left_tree, right_tree):
        self.left_tree = left_tree
        self.right_tree = right_tree

    def get_left(self):
        if self.left_tree.focus () == "":
            return False
        else:
            return True
