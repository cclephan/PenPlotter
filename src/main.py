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
r = 0.375/2 #in

draw = True
def isFloat(string):
    try: 
        float(string)
        return True
    except ValueError:
        return False

def task_rot_motor():
    if draw:
        start = True
        
        pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
        pinA0 = pyb.Pin(pyb.Pin.board.PA0)
        pinA1 = pyb.Pin(pyb.Pin.board.PA1)
        motor_rot = motor_clephan_mcgrath.MotorDriver(pinC1, pinA0, pinA1, 5)
        
        pinC6 = pyb.Pin(pyb.Pin.board.PC6)
        pinC7 = pyb.Pin(pyb.Pin.board.PC7)    
        encoder_rot = encoder_clephan_mcgrath.Encoder(pinC6,pinC7,8)
        current_position = 0
        last_position = 0 
        controller_rot = control.ClosedLoop([.15,0,0], [-100,100], ticks_per_rev* current_position)
        while True:

            if start:
                encoder_rot.zero()

                startTime = utime.ticks_ms()
                t_cur = utime.ticks_ms()
                start = False
            else:
                encoder_rot.update()
                t_cur = utime.ticks_ms()
                duty = controller_rot.update(encoder_rot.read(), startTime)
                motor_rot.set_duty_cycle(duty)
            if t_cur >= startTime+500:
                startTime = t_cur
                if q_theta_rot.any():
                    last_position = current_position
                    current_position = q_theta_rot.get()
                    new_set_rot = current_position - last_position
                else:
                    motor_rot.set_duty_cycle(0)
                print('Rotation ticks: ' + str(ticks_per_rev*new_set_rot))
                controller_rot = control.ClosedLoop([.2,0,0], [-100,100], ticks_per_rev* new_set_rot)
            yield (0)


def task_rad_motor():
    if draw:    
        start = True
        
        pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
        pinB4 = pyb.Pin(pyb.Pin.board.PB4)
        pinB5 = pyb.Pin(pyb.Pin.board.PB5)
        motor_rad = motor_clephan_mcgrath.MotorDriver(pinA10, pinB4, pinB5, 3)

        pinB6 = pyb.Pin(pyb.Pin.board.PB6)
        pinB7 = pyb.Pin(pyb.Pin.board.PB7)
        encoder_rad = encoder_clephan_mcgrath.Encoder(pinB6,pinB7,4)
        
        current_rad = 0 
        last_rad = 0
        controller_rad = control.ClosedLoop([.11,0,0], [-100,100], ticks_per_rev*current_rad)        
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
            if t_cur >= startTime+500:
                startTime = t_cur
                #print('Changing setpoint')
                if q_theta_rad.any():
                    last_rad = current_rad
                    current_rad = q_theta_rad.get()
                    new_set_rad = current_rad - last_rad
                else:
                    motor_rad.set_duty_cycle(0)
                print('Radial ticks: ' + str(ticks_per_rev*new_set_rad))
                controller_rad = control.ClosedLoop([.11,0,0], [-75,75], ticks_per_rev*new_set_rad)
            yield (0)


def task_servo():
    pinA7 = pyb.Pin(pyb.Pin.board.PA7,pyb.Pin.OUT_PP)
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    servo = servo_driver.ServoDriver(pinA10,pinA7,3)
    pen_is_up = True
    servo_status = 0
    while True:
        servo_status = q_servo.get()
        if servo_status == 0 and pen_is_up == False:
            servo.pen_up()
            pen_is_up = True
            print('going up')
        elif servo_status == 1 and pen_is_up == True:
            servo.pen_down()
            pen_is_up = False
            print('going down')
        yield (0)

def task_data_collect():
    with open(file_name) as file:
        commands= []
        for line in file.readlines():
            currentLine = line.split(";")
            for thing in currentLine:
                test = thing.split(',')
                if ("PD" in test[0] or "PU" in test[0]) and len(test[0]) > 2:
                    if "PD" in test[0]:
                        test[0] = test[0][2:]
                        test.insert(0, "PD")
                    elif "PU" in test[0]:
                        test[0] = test[0][2:]
                        test.insert(0, "PU")
                commands.append(test)
    x_commands = []
    y_commands = []  
    theta_commands = []
    dpi = 1016*2 #steps per inch
    for command in commands:
        print(command)
        i = 1
        if command[0] == "PU":
            cur_command = 0
        elif command[0] == "PD":
            cur_command = 1
        while i < len(command):
            x_var = float(command[i])/dpi #inch
            x_commands.append(x_var)
            i = i + 1
            y_var = float(command[i])/dpi
            y_commands.append(y_var)          
            if x_var != 0:   
                theta1 = math.atan(y_var/x_var) / (2*math.pi)
            else:
                theta1 = 0
            i = i + 1
            radial = math.sqrt(x_var**2 + y_var**2)
            theta2 = radial/(2*math.pi * r)
            q_theta_rot.put(theta1)
            q_theta_rad.put(theta2)
            q_servo.put(cur_command)

if __name__ == '__main__':

    q_theta_rad = task_share.Queue ('f', size = 400, thread_protect = False, overwrite = False,
                           name = "Queue Theta Radial")
    q_theta_rot = task_share.Queue ('f', size = 400, thread_protect = False, overwrite = False,
                           name = "Queue Theta Rotational") 
    q_servo = task_share.Queue ('f', size = 400, thread_protect = False, overwrite = False,
                           name = "Queue Servo")

    file_name = input('Enter HPGL filename: ')
    task_data_collect()
#     while q_theta_rad.any():
#         print('Radian: ' + str(q_theta_rad.get()/100))
#         print('Rotation: ' + str(q_theta_rot.get()/100))

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
    
    while q_theta_rot.any():
     try:
         cotask.task_list.pri_sched ()
     except KeyboardInterrupt:
        break
    
    print('Program over')