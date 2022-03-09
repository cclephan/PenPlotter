"""!
@file motor_clephan_mcgrath.py
This file contains the MotorDriver Class
@author Christian Clephan
@author Kyle McGrath
@date   02-Jan-2022
@copyright (c) 2022 released under CalPoly
"""
import pyb

class MotorDriver:
    '''! 
    This class implements a motor driver for an ME405 kit. 
    '''

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        '''! 
        Creates a motor driver by initializing GPIO
        pins and turning the motor off for safety. 
        @param en_pin enables the motor driver
        @param in1pin is the pin number associated with channel 2 of the motor
        @param in2pin is the pin number associated with channel 1 of the motor
        '''        
        print ('Creating a motor driver')
        en_pin.high()
        self.timX = pyb.Timer(timer, freq = 20000)
        self.ch1 = self.timX.channel(1,pyb.Timer.PWM, pin=in2pin)
        self.ch2 = self.timX.channel(2,pyb.Timer.PWM, pin=in1pin)

    def set_duty_cycle (self, duty):
        '''!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        '''
        if duty >= 0:
            if duty <= 100:
                self.ch2.pulse_width_percent(100)
                self.ch1.pulse_width_percent(100-duty)
            else:
                self.ch2.pulse_width_percent(100)
                self.ch1.pulse_width_percent(0)
        #if duty is negative then set the second channel to a specified duty (negative sign will make duty positive) and other to 0.
        elif duty < 0:
            if duty >= -100:
                self.ch1.pulse_width_percent(100)
                self.ch2.pulse_width_percent(100+duty)
            else:
                self.ch1.pulse_width_percent(100)
                self.ch2.pulse_width_percent(0)
        