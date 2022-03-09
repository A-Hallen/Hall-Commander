def getting_frame_focus(frame_left, frame_right):
    if not frame_left.focus_displayof ():
        if not frame_right.focus_displayof ():
            return frame_right
        else:
            return frame_right
    else:
        return frame_left
