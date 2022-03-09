"""!
@file main.py
Main file which runs a step response to rotate one revolution, prints values of 
time v.s. encoder position in ticks, and resets the system to run another
response. First, pins are created that will be used in the encoder/motor driver
and an encoder/motor object is created. The code then goes through a loop
asking the user for a Kp value, running the response by constantly updating
controller calculated duty and encoder position. After 2 seconds the encoder
is set to zero and all information collected in time/position arrays is
displayed. The user can exit the loop by pressing control+c, which will also
turn off the motor.
@author Christian Clephan
@author Kyle McGrath
@date   02-Jan-2022
@copyright (c) 2022 released under CalPoly
"""

import pyb
import cotask
import gc
import control
import utime
import encoder_clephan_mcgrath
import motor_clephan_mcgrath
import servo_driver
import task_share

ticks_per_rev = 256*2*16


S0_INIT = 0
S1_PEN_UP = 1
S2_PEN_DOWN = 2
S3_DRAW = 3

state = 3
def task_rot_motor():
    if state == S3_DRAW:
        start = True
        
        pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
        pinA0 = pyb.Pin(pyb.Pin.board.PA0)
        pinA1 = pyb.Pin(pyb.Pin.board.PA1)
        motor_rot = motor_clephan_mcgrath.MotorDriver(pinC1, pinA0, pinA1, 5)
        
        pinC6 = pyb.Pin(pyb.Pin.board.PC6)
        pinC7 = pyb.Pin(pyb.Pin.board.PC7)    
        encoder_rot = encoder_clephan_mcgrath.Encoder(pinC6,pinC7,8)
        
        set_rot = 0    
        controller_rot = control.ClosedLoop([.15,0,0], [-100,100], ticks_per_rev*set_rot)
        
        while True:

            if start:
                encoder_rot.zero()

                #Starting time to collect data
                startTime = utime.ticks_ms()
                t_cur = utime.ticks_ms()
                start = False
            else:
                #Updates encoder position, uses that value to update duty from controller, and sleeps 10ms
                encoder_rot.update()
                t_cur = utime.ticks_ms()
                duty = controller_rot.update(encoder_rot.read(), startTime)
                motor_rot.set_duty_cycle(duty)
                
            yield (0)


def task_rad_motor():
    if state == S3_DRAW:    
        start = True
        
        pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
        pinB4 = pyb.Pin(pyb.Pin.board.PB4)
        pinB5 = pyb.Pin(pyb.Pin.board.PB5)
        motor_rad = motor_clephan_mcgrath.MotorDriver(pinA10, pinB4, pinB5, 3)

        pinB6 = pyb.Pin(pyb.Pin.board.PB6)
        pinB7 = pyb.Pin(pyb.Pin.board.PB7)
        encoder_rad = encoder_clephan_mcgrath.Encoder(pinB6,pinB7,4)

        set_rad = (2.85-1.8)
        controller_rad = control.ClosedLoop([.11,0,0], [-100,100], ticks_per_rev*set_rad)
        
        while True:

            if start:
                encoder_rad.zero()

                #Starting time to collect data
                startTime = utime.ticks_ms()
                t_cur = utime.ticks_ms()
                start = False
            else:
                #Updates encoder position, uses that value to update duty from controller, and sleeps 10ms
                encoder_rad.update()
                t_cur = utime.ticks_ms()
                duty = controller_rad.update(encoder_rad.read(), startTime)
                motor_rad.set_duty_cycle(duty)

            yield (0)


def task_servo():
    pinA7 = pyb.Pin(pyb.Pin.board.PA7,pyb.Pin.OUT_PP)
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    servo = servo_driver.ServoDriver(pinA10,pinA7,3)
    if state == S1_PEN_UP:
        servo.pen_up()
    elif state == S2_PEN_DOWN:
        servo.pen_down()

#def task_data_collect():
    
    
    
#def task_logic():
    

if __name__ == '__main__':
    
    task_rot = cotask.Task (task_rot_motor, name = 'Task Rotational Motor', priority = 1, 
                         period = 10, profile = True, trace = False)
    task_rad = cotask.Task (task_rad_motor, name = 'Task Radial Motor', priority = 1, 
                         period = 35, profile = True, trace = False)
    task_srvo = cotask.Task (task_servo, name = 'Task Servo', priority = 0, 
                     period = 50, profile = True, trace = False)
    
    cotask.task_list.append (task_rot)
    cotask.task_list.append (task_rad)
    
    gc.collect ()
    
    while True:
     try:
         cotask.task_list.pri_sched ()
     except KeyboardInterrupt:
         break