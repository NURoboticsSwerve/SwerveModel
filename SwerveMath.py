import numpy

class Wheel:

    def __init__(self):
        self.ang = 0
        self.speed = 0
        self.rot_vel = 0

    # x, y, and rot are all -1 to 1 values
    def set_vector(self, x1, y1, rot1, rot_x_default, rot_y_default):
        x_vel = x1 + rot1 * rot_x_default
        y_vel = y1 + rot1 * rot_y_default
        self.speed = numpy.sqrt(x_vel ** 2 + y_vel ** 2)
        self.ang = numpy.arctan2(x_vel, y_vel)

    # Scale speed to maximum of 1 on a wheel
    def scale_speed(self, cur_max_speed):
        if cur_max_speed > 1:
            self.speed = self.speed / cur_max_speed


# Create 4 wheels
front_left = Wheel()
front_right = Wheel()
back_left = Wheel()
back_right = Wheel()

# Put wheel properties in array [name, rotX_default, rotY_default]
wheels_prop = [[front_left, 1, 1], [front_right, 1, -1], [back_left, -1, 1], [back_right, -1, -1]]

# Joystick inputs
x = eval(input("x coord: "))
y = eval(input("y coord: "))
cur_robot_rot = eval(input("current rot (deg): "))
rot = eval(input("rotation speed: "))

# Initialize current max speed for scaling
max_speed = 0

for i in range(5):

    cur_robot_rot = cur_robot_rot + 1

    # Calculate field-centric x and y translation values
    x_new = x * numpy.cos(numpy.deg2rad(cur_robot_rot)) - y * numpy.sin(numpy.deg2rad(cur_robot_rot))
    y = y * numpy.cos(numpy.deg2rad(cur_robot_rot)) + x * numpy.sin(numpy.deg2rad(cur_robot_rot))
    x = x_new

    # Set vector for every wheel and update max speed
    for wheel in wheels_prop:
        wheel[0].set_vector(x, y, rot, wheel[1], wheel[2])
        if wheel[0].speed > max_speed:
            max_speed = wheel[0].speed

    # Scale speed down if needed
    for wheel in wheels_prop:
        wheel[0].scale_speed(max_speed)
        print("Percent: ", numpy.round(wheel[0].speed * 100) / 100, "Angle: ", numpy.round(numpy.rad2deg(wheel[0].ang) * 100) / 100)

    print("")
