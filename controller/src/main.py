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
controller = vex.Controller()
#endregion config

def go(speed_left, speed_right):
    motor_right.set_velocity(speed_right*100, PERCENT)
    motor_left.set_velocity(speed_left*100, PERCENT)
    motor_right.spin(FORWARD)
    motor_left.spin(FORWARD)

def stop():
    motor_left.stop()
    motor_right.stop()

SPEED = 1.
TURN_SPEED = 0.3*SPEED
ARM_SPEED = 0.3
PINCHER_SPEED = 0.2

def read_controller():
    cA = controller.axisA.position()/100.
    cB = controller.axisB.position()/100.
    cC = controller.axisC.position()/100.
    cD = controller.axisD.position()/100.

    cC = (1 if cC > 0 else -1) * abs(cC)**1.5
    cD = (1 if cD > 0 else -1) * abs(cD)**1.5
    return [cA, cB, cC, cD]

motor_arm.set_stopping(HOLD)
motor_pincher.set_stopping(HOLD)

while True:
    cA, cB, cC, cD = read_controller()
    
    norm = max(cC+cD, 1)
    cC /= norm
    cD /= norm
    ml = cC*TURN_SPEED + cD*SPEED
    mr = -cC*TURN_SPEED + cD*SPEED
    go(ml, mr)

    if cA != 0:
        motor_arm.set_velocity(-cA*100*ARM_SPEED, PERCENT)
        motor_arm.spin(FORWARD)
    else:
        motor_arm.stop()

    if cB != 0:
        motor_pincher.set_velocity(cB*100*PINCHER_SPEED, PERCENT)
        motor_pincher.spin(FORWARD)
    else:
        motor_pincher.stop()
