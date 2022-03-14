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


def isFloat(string):
    try: 
        float(string)
        return True
    except ValueError:
        return False

def task_data_collect():
    state = 0
    if state == S0_DATA_INIT:
        x_commands = []
        y_commands = []  
        theta_commands = []
        dpi = 1016 #steps per inch
        state = S1_COLLECT_DATA
    if state == S1_COLLECT_DATA:    
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
        state = S2_CONVERT_DATA
    
    if state == S2_CONVERT_DATA:
        for command in commands:
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
                    theta1 = math.atan(y_var/x_var)# / (2*math.pi)
                else:
                    theta1 = 0
                i = i + 1
                radial = math.sqrt(x_var**2 + y_var**2)
                theta2 = radial/(r)
                q_theta_rot.put(theta1)
                q_theta_rad.put(theta2)
                q_servo.put(cur_command)
        
def stop_motors():
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    pinB4 = pyb.Pin(pyb.Pin.board.PB4)
    pinB5 = pyb.Pin(pyb.Pin.board.PB5)
    pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    pinA0 = pyb.Pin(pyb.Pin.board.PA0)
    pinA1 = pyb.Pin(pyb.Pin.board.PA1)
    motor_rot = motor_clephan_mcgrath.MotorDriver(pinC1, pinA0, pinA1, 5)
    motor_rad = motor_clephan_mcgrath.MotorDriver(pinA10, pinB4, pinB5, 3)
    
    motor_rot.set_duty_cycle(0)
    motor_rad.set_duty_cycle(0)

def task_rot_motor():
    state = 0
    if state == S0_INIT:
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
        state = S1_START
    while state != S4_STOP:

        if state == S1_START:
            encoder_rot.zero()
            startTime = utime.ticks_ms()
            t_cur = utime.ticks_ms()
            state = S2_DRIVE_MOTOR
            
        if state == S2_DRIVE_MOTOR:
            encoder_rot.update()
            t_cur = utime.ticks_ms()
            duty = controller_rot.update(encoder_rot.read(), startTime)
            motor_rot.set_duty_cycle(duty)
            if t_cur >= startTime+1000:
                state = S3_CHANGE_SETPOINT
        if state == S3_CHANGE_SETPOINT:
            startTime = t_cur
            if q_theta_rot.any():
                last_position = current_position
                current_position = q_theta_rot.get()
                new_set_rot = current_position - last_position
                print('Rotation ticks: ' + str(ticks_per_rev*new_set_rot))
                controller_rot.set_setPoint(ticks_per_rev* new_set_rot)
            if q_theta_rot.empty():
                state = S4_STOP
            else:
                state = S2_DRIVE_MOTOR
        if state == S4_STOP:
            print('Stopping rot')
            motor_rot.set_duty_cycle(0)
        yield (0)


def task_rad_motor():
    state = 0
    if state == S0_INIT:
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
        state = S1_START
        
    while state != S4_STOP:
        if state == S1_START:
            encoder_rad.zero()
            startTime = utime.ticks_ms()
            t_cur = utime.ticks_ms()
            state = S2_DRIVE_MOTOR
            
        if state == S2_DRIVE_MOTOR:
            encoder_rad.update()
            t_cur = utime.ticks_ms()
            duty = controller_rad.update(encoder_rad.read(), startTime)
            motor_rad.set_duty_cycle(duty)
            print('Changing duty')
            if t_cur >= startTime+1000:
                state = S3_CHANGE_SETPOINT
        if state == S3_CHANGE_SETPOINT:
            startTime = t_cur                
            if q_theta_rad.any():
                last_rad = current_rad
                current_rad = q_theta_rad.get()
                new_set_rad = current_rad - last_rad
                print('Radial ticks: ' + str(ticks_per_rev*new_set_rad))
                controller_rad.set_setPoint(ticks_per_rev*new_set_rad)
            if q_theta_rad.empty():
                state = S4_STOP
            else:
                state = S2_DRIVE_MOTOR
        if state == S4_STOP:
            print('Stopping rad')
            motor_rot.set_duty_cycle(0)
        yield (0)


def task_servo():
    state = 0
    if state == S0_SERVO_INIT:
        pinA7 = pyb.Pin(pyb.Pin.board.PA7,pyb.Pin.OUT_PP)
        pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
        servo = servo_driver.ServoDriver(pinA10,pinA7,3)
        curMode = 0
        state = S1_PEN_UP
    while q_servo.any():
        curMode = q_servo.get()
        if curMode == 0 and state == S2_PEN_DOWN:
            servo.pen_up()
            state = S1_PEN_UP
        elif curMode == 1 and state == S1_PEN_UP:
            servo.pen_down()
            state = S2_PEN_DOWN
        yield (0)
    
if __name__ == '__main__':
    
    #State variables for task_data_collect FSM
    S0_DATA_INIT = 0
    S1_COLLECT_DATA = 1
    S2_CONVERT_DATA = 2
    
    #State variables for motor tasks FSM
    S0_INIT = 0
    S1_START = 1
    S2_DRIVE_MOTOR = 2
    S3_CHANGE_SETPOINT = 3
    S4_STOP = 4
    
    #State variables for servo task FSM
    S0_SERVO_INIT = 0
    S1_PEN_UP = 1
    S2_PEN_DOWN = 2
    
    #Creating Queues
    q_theta_rad = task_share.Queue ('f', size = 400, thread_protect = False, overwrite = False,
                           name = "Queue Theta Radial")
    q_theta_rot = task_share.Queue ('f', size = 400, thread_protect = False, overwrite = False,
                           name = "Queue Theta Rotational") 
    q_servo = task_share.Queue ('b', size = 400, thread_protect = False, overwrite = False,
                           name = "Queue Servo")
    
    #Asks user for HPGL File
    file_name = input('Enter HPGL filename: ')
    
    #Runs Data Collection task
    task_data_collect()
    print('Data Collection Finished')
    

    #Creating task objects
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
    
    #Running Cotask with task objects
    while q_servo.any():
     try:
         cotask.task_list.pri_sched ()
     except KeyboardInterrupt:
        break
    
    #Cuts off motors
    stop_motors()
    
    print('Program over')