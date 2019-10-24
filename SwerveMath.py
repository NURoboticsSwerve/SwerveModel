# Put math here


class Wheel:

    def __init__(self):
        self.ang = 0
        self.vel = 0
        self.rot_vel = 0

    # x, y, and rot are all -1 to 1 values
    def set_motion(self, x, y, rot):
        print("Do nothing")


top_left = Wheel()
top_right = Wheel()
back_left = Wheel()
back_right = Wheel()