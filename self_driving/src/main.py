#VEX IQ Python-Project
import vex
from time import sleep, time
import random
import math

random.seed(0)

#region config
motor_right = vex.Motor(6, True)
motor_left = vex.Motor(9, False)

motor_arm = vex.Motor(2, True)
motor_pincher = vex.Motor(7, False)
distance_sens = vex.Distance(0)
#endregion config

def go(speed_left, speed_right):
    motor_right.set_velocity(speed_right*100, PERCENT)
    motor_left.set_velocity(speed_left*100, PERCENT)
    motor_right.spin(FORWARD)
    motor_left.spin(FORWARD)

def stop():
    motor_left.stop()
    motor_right.stop()

def time_now():
    return float(time())

class MovingVar:
    def __init__(self, name, init_val, gamma):
        self.name = name
        self.gamma = gamma
        self.val = init_val

    def update(self, new_val, elapsed):
        coef = math.exp(-elapsed * self.gamma)
        self.val = self.val*coef + new_val*(1-coef)
    
    def print(self):
        print(self.name, round(self.val, 2))

distance = MovingVar("distance", 2, 50.)
speed = MovingVar("speed", 0, 50.)
acceleration = MovingVar("acceleration", 0, 50.)

motor_l = MovingVar("motor_l", 0, 5.)
motor_r = MovingVar("motor_r", 0, 5.)

elapsed = 0.05

def update_variables():
    old_dist = distance.val
    old_speed = speed.val
    distance.update(distance_sens.object_distance(MM)*1e-3, elapsed)
    speed.update((old_dist-distance.val)/elapsed, elapsed)
    acceleration.update((old_speed-speed.val)/elapsed, elapsed)

turn_dir = (0,0)
button_pressed = 0
is_on = False
turning = False

SPEED = -0.5

while True:
    sleep(elapsed)

    if brain.buttonLeft.pressing():
        if button_pressed < 0:
            is_on = not is_on
        button_pressed = 0.3
    else:
        button_pressed -= elapsed

    if not is_on:
        stop()
        continue

    if distance.val < 1.5:

        forward_speed = (max(distance.val,0.5)-0.5)/1.
        turning_speed = 1-forward_speed
        if not turning:
            turn_dir = random.choice([(-SPEED,SPEED),(SPEED,-SPEED)])
        turning = True
        motor_l.update(forward_speed*SPEED + turn_dir[0]*turning_speed, elapsed)
        motor_r.update(forward_speed*SPEED + turn_dir[1]*turning_speed, elapsed)
    else:
        motor_l.update(SPEED, elapsed*3)
        motor_r.update(SPEED, elapsed*3)
        turning=False

    go(motor_l.val,motor_r.val)

    distance.print()
    motor_l.print()

    update_variables()

    






motor_arm.spin_for(FORWARD, 90, DEGREES)

motor_pincher.spin(FORWARD)
sleep(0.5)
motor_pincher.set_stopping(HOLD)
motor_pincher.stop()

# main thread
motor_right.spin(FORWARD)
motor_left.spin(FORWARD)

sleep(1)

motor_left.stop()
motor_right.stop()