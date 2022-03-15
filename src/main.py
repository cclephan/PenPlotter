"""!
@file main.py
Main file for pen plotter robot which is run by the user. The program begins by creating state variables,
queues, and asking the user for HPGL filename. Once the user inputs the filename, our data collection task
is run to put all the setpoint values for respective radial/angular/and servo motor into queues. The task
functions for each motor are then created as objects using cotask and appended to a list. This list is then
continuously run until there are no setpoint values left in each queue. Finally, the motors are turned off
and a print statement lets the user know the program is over.
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

##Ticks
ticks_per_rev = 256*2*16
r = 0.375/2 #in

def task_data_collect():
    '''!
    @brief Collects X/Y data from HPGL drawing and converts into readable commands for rotational/radial/servo motors
    @details Opens file specified by the user and converts HPGL standard commands to readable code to be put in
    a queue and read by other tasks as setpoint values for motor control. X/Y coordinates are converted to polar
    coordinates in revolutions for respective motors to spin. Finally, the setpoints in revolutions for DC motors
    and up or down commands for pen are put into their resepctive queues.
    '''    
    state = 0
    if state == S0_DATA_INIT:
        x_commands = []
        y_commands = []  
        theta_commands = []
        ##Dots per inch as specified by inkscape when creating drawing.
        dpi = 1016 
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
                ##X coordinate of HPGL command
                x_var = float(command[i])/dpi #inch
                x_commands.append(x_var)
                i = i + 1
                ##Y coordinate of HPGL command
                y_var = float(command[i])/dpi
                y_commands.append(y_var)          
                if x_var != 0:
                    ##Converted X/Y coordinate to rotational setpoint in revolutions
                    theta1 = math.atan(y_var/x_var) / (2*math.pi)
                else:
                    theta1 = 0
                i = i + 1
                radial = math.sqrt(x_var**2 + y_var**2)
                ##Converted X/Y coordinate to radial setpoint in revolutions
                theta2 = radial/(r*2*math.pi)
                q_theta_rot.put(theta1)
                q_theta_rad.put(theta2)
                q_servo.put(cur_command)
        
def stop_motors():
    '''!
    @brief Stops rotational and radial motors; used at the end of main.py program.
    '''
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
    '''!
    @brief Rotational motor task drives the motor to specified setpoint and repeats the process with new setpoints until there are none left
    @details First the rotational motor/encoder pins are initialized and created as objects along with a controller.
    Next, the encoder is zeroed and a timer is started for which a motor will be driven to a setpoint by a controller
    which constantly updates and sends duties to the motor based on position control. After 1 second another setpoint
    value is given to the controller for which the motor is driven again. This is repeated until there are no setpoint
    values left in the queue and the motor is stopped.
    '''
    state = 0
    if state == S0_INIT:
        start = True
        pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
        pinA0 = pyb.Pin(pyb.Pin.board.PA0)
        pinA1 = pyb.Pin(pyb.Pin.board.PA1)
        ##Rotational motor object created using motor driver file from previous lab
        motor_rot = motor_clephan_mcgrath.MotorDriver(pinC1, pinA0, pinA1, 5)
        
        pinC6 = pyb.Pin(pyb.Pin.board.PC6)
        pinC7 = pyb.Pin(pyb.Pin.board.PC7)
        ##Rotational encoder object created using encoder driver file from previous lab
        encoder_rot = encoder_clephan_mcgrath.Encoder(pinC6,pinC7,8)
        ##Current motor position
        current_position = 0
        ##Last motor position used to calculated difference between current and last for the next setpoint
        last_position = 0
        ##Rotational controller object created using controller file from previous lab
        controller_rot = control.ClosedLoop([.15,0,0], [-100,100], ticks_per_rev* current_position)
        state = S1_START
    while state != S4_STOP:

        if state == S1_START:
            #State 1 zeros encoder and starts initial and current timer
            encoder_rot.zero()
            startTime = utime.ticks_ms()
            t_cur = utime.ticks_ms()
            state = S2_DRIVE_MOTOR
            
        if state == S2_DRIVE_MOTOR:
            #State 2 updates encoder position for duty cycle to be calculated by controller and sent over to motor
            encoder_rot.update()
            t_cur = utime.ticks_ms()
            duty = controller_rot.update(encoder_rot.read(), startTime)
            motor_rot.set_duty_cycle(duty)
            if t_cur >= startTime+1000:
                state = S3_CHANGE_SETPOINT
        if state == S3_CHANGE_SETPOINT:
            #State 3 changes the setpoint of the motor with the next queue value from data collection
            startTime = t_cur
            if q_theta_rot.any():
                last_position = current_position
                current_position = q_theta_rot.get()
                ##Next rotational setpoint value in revolutions
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
    '''!
    @brief Radial motor task drives the motor to specified setpoint and repeats the process with new setpoints until there are none left
    @details First the radial motor/encoder pins are initialized and created as objects along with a controller.
    Next, the encoder is zeroed and a timer is started for which a motor will be driven to a setpoint by a controller
    which constantly updates and sends duties to the motor based on position control. After 1 second another setpoint
    value is given to the controller for which the motor is driven again. This is repeated until there are no setpoint
    values left in the queue and the motor is stopped.
    '''
    state = 0
    if state == S0_INIT:
        pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
        pinB4 = pyb.Pin(pyb.Pin.board.PB4)
        pinB5 = pyb.Pin(pyb.Pin.board.PB5)
        ##Radial motor object created using motor driver file from previous lab
        motor_rad = motor_clephan_mcgrath.MotorDriver(pinA10, pinB4, pinB5, 3)

        pinB6 = pyb.Pin(pyb.Pin.board.PB6)
        pinB7 = pyb.Pin(pyb.Pin.board.PB7)
        ##Radial encoder object created using encoder driver file from previous lab
        encoder_rad = encoder_clephan_mcgrath.Encoder(pinB6,pinB7,4)
        
        ##Current radial motor position
        current_rad = 0
        ##Last radial motor position used to calculated difference between current and last for the next setpoint
        last_rad = 0
        ##Radial controller object created using controller file from previous lab
        controller_rad = control.ClosedLoop([.11,0,0], [-100,100], ticks_per_rev*current_rad)
        state = S1_START
        
    while state != S4_STOP:
        if state == S1_START:
            #State 1 zeros encoder and starts initial and current timer
            encoder_rad.zero()
            startTime = utime.ticks_ms()
            t_cur = utime.ticks_ms()
            state = S2_DRIVE_MOTOR
            
        if state == S2_DRIVE_MOTOR:
            #State 2 updates encoder position for duty cycle to be calculated by controller and sent over to motor
            encoder_rad.update()
            t_cur = utime.ticks_ms()
            duty = controller_rad.update(encoder_rad.read(), startTime)
            motor_rad.set_duty_cycle(duty)
            print('Changing duty')
            if t_cur >= startTime+1000:
                state = S3_CHANGE_SETPOINT
        if state == S3_CHANGE_SETPOINT:
            #State 3 changes the setpoint of the motor with the next queue value from data collection
            startTime = t_cur                
            if q_theta_rad.any():
                last_rad = current_rad
                current_rad = q_theta_rad.get()
                ##Next radial setpoint value in revolutions
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
    '''!
    @brief Sends a PWM signal to the servo to make the pen go up or down based on whether the converted HPGL command is a 1 or 0
    '''
    state = 0
    if state == S0_SERVO_INIT:
        pinA7 = pyb.Pin(pyb.Pin.board.PA7,pyb.Pin.OUT_PP)
        pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
        ##Servo object created with driver file
        servo = servo_driver.ServoDriver(pinA10,pinA7,3)
        ##Current mode that is sent by q_servo
        curMode = 0
        state = S1_PEN_UP
    while q_servo.any():
        curMode = q_servo.get()
        if curMode == 0 and state == S2_PEN_DOWN:
            #Moves pen up
            servo.pen_up()
            state = S1_PEN_UP
        elif curMode == 1 and state == S1_PEN_UP:
            #Moves pen down
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