import numpy
import sched, time
from graphics import *

WHEEL_LENGTH_PIX = 20
WHEEL_DIST_FROM_CENTER = 60
MAX_SPEED = 300  # in pixels/s

UPDATE_TIME = .05  # in seconds

cur_robot_rot = 0  # in degrees
cur_robot_pos_x = 70
cur_robot_pos_y = 500

SCREEN_X = 1100
SCREEN_Y = 600


class Wheel:

    def __init__(self, rot_x_default, rot_y_default):
        self.ang = 0
        self.speed = 0
        self.x_pos = 0
        self.y_pos = 0
        self.rot_x_def = rot_x_default
        self.rot_y_def = rot_y_default
        self.line = Line(Point(0, 0), Point(0, 0))

    # x, y, and rot are all -1 to 1 values
    def set_vector(self, x1, y1, rot1):
        x_vel = x1 + rot1 * numpy.sin(numpy.arctan2(self.rot_x_def, self.rot_y_def) + cur_robot_rot)
        y_vel = y1 + rot1 * numpy.cos(numpy.arctan2(self.rot_x_def, self.rot_y_def) + cur_robot_rot)
        self.speed = numpy.sqrt(x_vel ** 2 + y_vel ** 2)
        self.ang = numpy.arctan2(x_vel, y_vel)

    # Scale speed to maximum of 1 on a wheel
    def scale_speed(self, cur_max_speed):
        if cur_max_speed > 1:
            self.speed = self.speed / cur_max_speed

    def draw_wheels(self, window):
        theta = numpy.arctan2(-self.rot_y_def, self.rot_x_def) + cur_robot_rot
        self.line.undraw()
        self.line = Line(Point((cur_robot_pos_x + WHEEL_DIST_FROM_CENTER * numpy.sin(theta) -
                               WHEEL_LENGTH_PIX / 2 * numpy.sin(self.ang)) % SCREEN_X,
                               (cur_robot_pos_y - WHEEL_DIST_FROM_CENTER * numpy.cos(theta) +
                               WHEEL_LENGTH_PIX / 2 * numpy.cos(self.ang)) % SCREEN_Y),
                          Point((cur_robot_pos_x + WHEEL_DIST_FROM_CENTER * numpy.sin(theta) +
                                WHEEL_LENGTH_PIX / 2 * numpy.sin(self.ang)) % SCREEN_X,
                                (cur_robot_pos_y - WHEEL_DIST_FROM_CENTER * numpy.cos(theta) -
                                WHEEL_LENGTH_PIX / 2 * numpy.cos(self.ang)) % SCREEN_Y))
        #self.line.undraw()
        self.line.draw(window)


# Create 4 wheels (rot_x_default, rot_y_default)
front_left = Wheel(1, 1)
front_right = Wheel(1, -1)
back_left = Wheel(-1, 1)
back_right = Wheel(-1, -1)

wheels = [front_left, front_right, back_left, back_right]


# Sets wheel speeds and angles from joystick input
def set_wheel_from_joystick(x1, y1, rot_per):

    # Initialize current max speed for scaling
    max_speed = 0

    # Calculate field-centric x and y translation values
    x_new = x1 * numpy.cos(numpy.deg2rad(cur_robot_rot)) - y1 * numpy.sin(numpy.deg2rad(cur_robot_rot))
    y_new = y1 * numpy.cos(numpy.deg2rad(cur_robot_rot)) + x1 * numpy.sin(numpy.deg2rad(cur_robot_rot))

    # Set vector for every wheel and update max speed
    for wheel in wheels:
        wheel.set_vector(x_new, y_new, rot_per)
        if wheel.speed > max_speed:
            max_speed = wheel.speed

    # Scale speed down if needed
    for wheel in wheels:
        wheel.scale_speed(max_speed)

    return max_speed


def update_robot_pos(max_percent):
    global cur_robot_rot, cur_robot_pos_x, cur_robot_pos_y

    if max_percent < 1:
        max_percent = 1
    cur_robot_pos_x = cur_robot_pos_x + (MAX_SPEED * UPDATE_TIME * x / max_percent)
    cur_robot_pos_y = cur_robot_pos_y - (MAX_SPEED * UPDATE_TIME * y / max_percent)
    cur_robot_rot = cur_robot_rot + (rot * MAX_SPEED * UPDATE_TIME / WHEEL_DIST_FROM_CENTER / max_percent)
    if cur_robot_rot > 2 * numpy.pi:
        cur_robot_rot = cur_robot_rot - 2 * numpy.pi


# Joystick inputs
x = eval(input("x coord: "))
y = eval(input("y coord: "))
rot = eval(input("rotation speed: "))

set_wheel_from_joystick(x, y, rot)
win = GraphWin("Swerve", SCREEN_X, SCREEN_Y)
win.setBackground('white')
win.getMouse()


def main(sc):
    global cur_robot_rot, cur_robot_pos_x, cur_robot_pos_y
    max_pcnt = set_wheel_from_joystick(x, y, rot)
    update_robot_pos(max_pcnt)
    for wheel in wheels:
        wheel.draw_wheels(win)
    s.enter(UPDATE_TIME, 1, main, (sc,))


s = sched.scheduler(time.time, time.sleep)
s.enter(UPDATE_TIME, 1, main, (s,))
s.run()


win.close()