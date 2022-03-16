# Colors
import os

dark_gray = "#161616"
blue = "#0000ff"
red = "#ff0000"
green = "#00ff00"
gray = "#2c2c2c"
soft_gray = "#999999"

# all the paths that we have been open in left frame
opened_left_paths = []
opened_left_forward = []
# all the path that we have been open in right frame
opened_right_paths = []
opened_right_forward = []

tree_view_background = "black"
tree_view_foreground = "white"
tree_view_fieldbackground = "black"
# the name of the title bar and other configurations
name_of_the_app = "Hall Commander"
# The color of the left and right frames
color_of_side_frames = "black"
contador = True
selection_left = False
last_selection_left = 0
last_selection_right = 0
# Show hiden files or not
show_hiden_files = True
# Actual path in were we are on both frames, left and right
actual_left_path = os.getenv ('HOME')
actual_right_path = os.getenv ('HOME')

# variable for changing the hidden state
hidden = True
# right click variables
portapapeles = []
