"""!
@file main.py
@author Christian Clephan
@author Kyle McGrath
@date   02-Jan-2022
@copyright (c) 2022 released under CalPoly
"""
import math
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
r = 0.375 #in

S0_INIT = 0
S1_PEN_UP = 1
S2_PEN_DOWN = 2
S3_DRAW = 3

state = 3
def isFloat(string):
    try: 
        float(string)
        return True
    except ValueError:
        return False

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
        controller_rot = control.ClosedLoop([.15,0,0], [-100,100], ticks_per_rev* set_rot)
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
            #if duty < 10:
                if q_theta_rot.any():
                    set_rot = q_theta_rot.get()-set_rot
                    new_set_rot = set_rot/100
                print('Rotation ticks: ' + str(ticks_per_rev*new_set_rot))
                controller_rot = control.ClosedLoop([.11,0,0], [-100,100], ticks_per_rev* new_set_rot)
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
        
        set_rad = 0
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
#                 if duty < 10:
                if q_theta_rad.any():
                    set_rad = q_theta_rad.get()-set_rad
                new_set_rad = set_rad/100
                print('Radial ticks: ' + str(ticks_per_rev*new_set_rad))
                controller_rad = control.ClosedLoop([.11,0,0], [-100,100], ticks_per_rev*new_set_rad)
            yield (0)


def task_servo():
    pinA7 = pyb.Pin(pyb.Pin.board.PA7,pyb.Pin.OUT_PP)
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    servo = servo_driver.ServoDriver(pinA10,pinA7,3)
    pen_is_up = True
    n = 0
    while True:
        if q_servo.get() == 0 and pen_is_up == False:
            servo.pen_up()
            n = n+1
            pen_is_up = True
            print('goin up baby')
        elif q_servo.get() == 1 and pen_is_up == True:
            servo.pen_down()
            pen_is_up = False
            print('goin down baby')
        if n > 1:
            q_stop.put(1)
        yield (0)

def task_data_collect():
    with open(file_name) as file:
        commands= []
        for line in file.readlines():
            currentLine = line.split(";")
            for thing in currentLine:
                test = thing.split(',')
                if ("PD" in test[0] or "PU" in test[0]) and len(test[0]) > 2:
                    #theShid = re.split('(\d+)', test[0])
                    if "PD" in test[0]:
                        test[0].replace("PD", "")
                        test.insert(0, "PD")
                    elif "PU" in test[0]:
                        test[0].replace("PU", "")
                        test.insert(0, "PU")
                commands.append(test)
    x_commands = []
    y_commands = []  
    theta_commands = []
    dpi = 1016
    for command in commands:
        i = 1
        if command[0] == "PU":
            #print("Pen Up")
            cur_command = 0
        elif command[0] == "PD":
            #print("Pen Down")
            cur_command = 1
        while i < len(command):
            if isFloat(command[i]) == True:
                x_var = int(command[i])/dpi
                x_commands.append(x_var)
            else:
                x_var = 0
                x_commands.append(x_var)
            i = i + 1
            if isFloat(command[i]) == True:
                y_var = int(command[i])/dpi
                y_commands.append(y_var)
            else:
                y_var = 0
                y_commands.append(y_var)            
            if x_var != 0:   
                theta1 = math.atan(y_var/x_var) / (2*math.pi)
            else:
                theta1 = math.pi / 2 / (2*math.pi)
            i = i + 1
            radial = math.sqrt(x_var**2 + y_var**2)
            theta2 = radial/(2*math.pi * r)
            theta1 = round(theta1*100)
            theta2 = round(theta2*100)
            q_theta_rot.put(theta1)
            q_theta_rad.put(theta2)
            q_servo.put(cur_command)
            #theta_commands.append((cur_command, theta1, theta2))    

if __name__ == '__main__':

    q_theta_rad = task_share.Queue ('h', size = 400, thread_protect = False, overwrite = False,
                           name = "Queue Theta Radial")
    q_theta_rot = task_share.Queue ('h', size = 400, thread_protect = False, overwrite = False,
                           name = "Queue Theta Rotational") 
    q_servo = task_share.Queue ('h', size = 400, thread_protect = False, overwrite = False,
                           name = "Queue Servo")
    q_stop = task_share.Queue ('h', size = 1, thread_protect = False, overwrite = False,
                           name = "Queue Stop")
    file_name = input('Enter HPGL filename: ')
    task_data_collect()
#     print(q_theta_rad)
#     print(q_theta_rot)
#     print(q_servo)
    print('Data Collection Finished')
    
    task_rot = cotask.Task (task_rot_motor, name = 'Task Rotational Motor', priority = 1, 
                         period = 500, profile = True, trace = False)
    task_rad = cotask.Task (task_rad_motor, name = 'Task Radial Motor', priority = 1, 
                         period = 500, profile = True, trace = False)
    task_srvo = cotask.Task (task_servo, name = 'Task Servo', priority = 0, 
                     period = 500, profile = True, trace = False)
    
    cotask.task_list.append (task_rot)
    cotask.task_list.append (task_rad)
    cotask.task_list.append (task_srvo)
    gc.collect ()
    
    while q_stop.empty():
     try:
         cotask.task_list.pri_sched ()
     except KeyboardInterrupt:
        break
    
    print('Program be over cuh')